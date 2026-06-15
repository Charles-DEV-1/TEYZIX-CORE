"""
Authentication Service Module

PURPOSE:
    Implement authentication business logic.
    Handle user authentication, password management, and token operations.
"""

from datetime import datetime
from typing import Optional
from flask import current_app
from flask_jwt_extended import decode_token
from app.extensions import db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.password_reset_token import PasswordResetToken
from app.auth.utils import (
    is_valid_email,
    is_strong_password,
    validate_role,
    hash_password,
    verify_password,
    generate_tokens,
    generate_access_token,
    generate_reset_token,
)


def _redis():
    from app.extensions.redis import redis_client
    return redis_client


class AuthService:
    """Service class for handling authentication operations."""

    def register(self, name: str, email: str, password: str, role: str = 'customer'):
        """Register a new user without issuing authentication tokens."""
        normalized_email = (email or '').strip().lower()
        normalized_name = (name or '').strip()

        if not normalized_name:
            raise ValueError('Name is required')
        if not is_valid_email(normalized_email):
            raise ValueError('Invalid email address')
        if not is_strong_password(password):
            raise ValueError('Password does not meet complexity requirements')
        if not validate_role(role):
            raise ValueError('Invalid role')

        if User.query.filter_by(email=normalized_email).first():
            raise ValueError('Email already registered')

        user = User(
            name=normalized_name,
            email=normalized_email,
            password_hash=hash_password(password),
            role=role,
        )

        db.session.add(user)
        db.session.commit()

        return {
            'user': user.to_dict(),
        }

    def login(self, email: str, password: str):
        """Authenticate user and issue new access and refresh tokens."""
        normalized_email = (email or '').strip().lower()
        if not is_valid_email(normalized_email):
            raise ValueError('Invalid credentials')

        user = User.query.filter_by(email=normalized_email).first()
        if not user or not user.is_active:
            raise ValueError('Invalid credentials')
        if not verify_password(user.password_hash, password):
            raise ValueError('Invalid credentials')

        access_token, refresh_token = generate_tokens(user)
        refresh_jti = decode_token(refresh_token).get('jti')
        self._store_refresh_token(user.id, refresh_token)
        self._track_access_token(refresh_jti, access_token)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict(),
        }

    def refresh_access_token(self, user_id: int, refresh_jti: str):
        """Issue a new access token for a valid refresh token."""
        try:
            lookup_user_id = int(user_id)
        except (TypeError, ValueError):
            lookup_user_id = user_id

        token = RefreshToken.query.filter_by(token_jti=refresh_jti, user_id=lookup_user_id).first()
        if not token or token.is_expired():
            raise ValueError('Refresh token is invalid or expired')
        if self._is_token_revoked(refresh_jti):
            raise ValueError('Refresh token has been revoked')

        user = User.query.get(user_id)
        if not user or not user.is_active:
            raise ValueError('User not found')

        self._revoke_previous_access_token(refresh_jti)
        access_token = generate_access_token(user)
        self._track_access_token(refresh_jti, access_token)
        return access_token

    def logout(self, access_jti: str, refresh_token: Optional[str] = None):
        """Revoke the current token and optionally revoke the refresh token."""
        self._revoke_jwt(access_jti, current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])

        if refresh_token:
            decoded = decode_token(refresh_token)
            if decoded.get('type') != 'refresh':
                raise ValueError('Invalid refresh token')

            refresh_jti = decoded.get('jti')
            expires_at = datetime.utcfromtimestamp(decoded.get('exp'))
            self._revoke_jwt(refresh_jti, expires_at - datetime.utcnow())
            self._clear_access_session(refresh_jti)

            record = RefreshToken.query.filter_by(token_jti=refresh_jti).first()
            if record:
                db.session.delete(record)
                db.session.commit()

        return {'success': True, 'message': 'Logout successful'}

    def request_password_reset(self, email: str):
        """Create and store a password reset token for a user."""
        normalized_email = (email or '').strip().lower()
        if not is_valid_email(normalized_email):
            raise ValueError('Invalid email address')

        user = User.query.filter_by(email=normalized_email).first()
        if not user or not user.is_active:
            raise ValueError('User not found')

        token = generate_reset_token()
        expires_at = datetime.utcnow() + current_app.config.get('PASSWORD_RESET_TOKEN_EXPIRES', current_app.config['JWT_REFRESH_TOKEN_EXPIRES'] / 7)
        reset_record = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at,
        )

        db.session.add(reset_record)
        db.session.commit()

        return {
            'message': 'Password reset token created',
            'reset_token': token,
            'expires_at': expires_at.isoformat(),
        }

    def reset_password(self, reset_token: str, new_password: str):
        """Validate a password reset token and update the user's password."""
        if not is_strong_password(new_password):
            raise ValueError('Password does not meet complexity requirements')

        record = PasswordResetToken.query.filter_by(token=reset_token).first()
        if not record or not record.is_valid():
            raise ValueError('Reset token is invalid or expired')

        user = record.user
        user.password_hash = hash_password(new_password)
        record.used = True
        db.session.commit()

        return {'success': True, 'message': 'Password reset successfully'}

    def get_current_user(self, user_id: int) -> User:
        """Fetch the currently authenticated user."""
        user = User.query.get(user_id)
        if not user or not user.is_active:
            raise ValueError('User not found')
        return user

    def _store_refresh_token(self, user_id: int, refresh_token: str) -> RefreshToken:
        decoded = decode_token(refresh_token)
        token_jti = decoded.get('jti')
        expires_at = datetime.utcfromtimestamp(decoded.get('exp'))

        refresh_record = RefreshToken(
            user_id=user_id,
            token_jti=token_jti,
            expires_at=expires_at,
        )
        db.session.add(refresh_record)
        db.session.commit()
        return refresh_record

    def _revoke_jwt(self, jti: str, ttl) -> None:
        redis_client = _redis()
        if redis_client is None or not jti:
            return
        ttl_seconds = int(ttl.total_seconds()) if hasattr(ttl, 'total_seconds') else int(ttl)
        if ttl_seconds <= 0:
            ttl_seconds = 1
        redis_client.setex(f'jwt_blocklist:{jti}', ttl_seconds, 'true')

    def _track_access_token(self, refresh_jti: str, access_token: str) -> None:
        """Store the current access token JTI linked to a refresh session."""
        redis_client = _redis()
        if redis_client is None or not refresh_jti:
            return
        decoded = decode_token(access_token)
        access_jti = decoded.get('jti')
        if not access_jti:
            return
        ttl_seconds = int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds())
        redis_client.setex(f'access_session:{refresh_jti}', ttl_seconds, access_jti)

    def _revoke_previous_access_token(self, refresh_jti: str) -> None:
        """Blocklist the previous access token when issuing a new one."""
        redis_client = _redis()
        if redis_client is None or not refresh_jti:
            return
        old_access_jti = redis_client.get(f'access_session:{refresh_jti}')
        if old_access_jti:
            self._revoke_jwt(old_access_jti, current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])

    def _clear_access_session(self, refresh_jti: str) -> None:
        redis_client = _redis()
        if redis_client is None or not refresh_jti:
            return
        redis_client.delete(f'access_session:{refresh_jti}')

    def _is_token_revoked(self, token_jti: str) -> bool:
        redis_client = _redis()
        if redis_client is None or not token_jti:
            return False
        return redis_client.exists(f'jwt_blocklist:{token_jti}') == 1
