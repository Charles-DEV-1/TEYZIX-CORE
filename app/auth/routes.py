"""
Authentication Routes Module
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.middleware.auth_middleware import auth_required
from app.auth.service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_service = AuthService()


def _json_response(success: bool, message: str, data=None, status_code: int = 200):
    response = {'success': success, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    summary: Create a new user account
    description: No authentication required. Password must meet complexity requirements.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
          properties:
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: john@example.com
            password:
              type: string
              example: SecurePass1!
            role:
              type: string
              enum: [customer, delivery_agent, admin]
              example: customer
    responses:
      201:
        description: Registration successful
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Registration successful
            data:
              type: object
              properties:
                user:
                  type: object
      400:
        description: Validation error (invalid email, weak password, email already registered)
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Email already registered
    """
    payload = request.get_json(silent=True) or {}
    name = payload.get('name')
    email = payload.get('email')
    password = payload.get('password')
    role = payload.get('role', 'customer')

    try:
        result = auth_service.register(name=name, email=email, password=password, role=role)
        return _json_response(True, 'Registration successful', result, 201)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=400)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login
    ---
    tags:
      - Auth
    summary: Authenticate and receive JWT tokens
    description: No authentication required.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: john@example.com
            password:
              type: string
              example: SecurePass1!
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Login successful
            data:
              type: object
              properties:
                access_token:
                  type: string
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                refresh_token:
                  type: string
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                user:
                  type: object
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Invalid credentials
    """
    payload = request.get_json(silent=True) or {}
    email = payload.get('email')
    password = payload.get('password')

    try:
        result = auth_service.login(email=email, password=password)
        return _json_response(True, 'Login successful', result)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=401)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """
    Refresh access token
    ---
    tags:
      - Auth
    summary: Issue a new access token using a refresh token
    description: Requires a valid refresh token in the Authorization header.
    security:
      - RefreshToken: []
    responses:
      200:
        description: Token refreshed successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Token refreshed successfully
            data:
              type: object
              properties:
                access_token:
                  type: string
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      401:
        description: Invalid, expired, or revoked refresh token
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Refresh token is invalid or expired
    """
    user_id = get_jwt_identity()
    jwt_payload = get_jwt()
    refresh_jti = jwt_payload.get('jti')

    try:
        access_token = auth_service.refresh_access_token(user_id=user_id, refresh_jti=refresh_jti)
        return _json_response(True, 'Token refreshed successfully', {'access_token': access_token})
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=401)


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout
    ---
    tags:
      - Auth
    summary: Revoke the current access token
    description: Optionally pass refresh_token in body to revoke it as well.
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            refresh_token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    responses:
      200:
        description: Logout successful
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Logout successful
      400:
        description: Invalid refresh token
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Invalid refresh token
      401:
        description: Missing or invalid access token
    """
    jwt_payload = get_jwt()
    access_jti = jwt_payload.get('jti')
    payload = request.get_json(silent=True) or {}
    refresh_token = payload.get('refresh_token')

    try:
        result = auth_service.logout(access_jti=access_jti, refresh_token=refresh_token)
        return _json_response(True, result.get('message', 'Logout successful'))
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=400)


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Request password reset
    ---
    tags:
      - Auth
    summary: Generate a password reset token
    description: No authentication required.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
          properties:
            email:
              type: string
              example: john@example.com
    responses:
      200:
        description: Reset token generated
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Password reset token generated
            data:
              type: object
              properties:
                reset_token:
                  type: string
                  example: xYz123AbC...
                expires_at:
                  type: string
                  example: '2026-06-14T13:00:00'
      400:
        description: Invalid email or user not found
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: User not found
    """
    payload = request.get_json(silent=True) or {}
    email = payload.get('email')

    try:
        result = auth_service.request_password_reset(email=email)
        return _json_response(True, 'Password reset token generated', result)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=400)


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password
    ---
    tags:
      - Auth
    summary: Reset password using a reset token
    description: No authentication required.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - token
            - password
          properties:
            token:
              type: string
              example: xYz123AbC...
            password:
              type: string
              example: NewSecurePass1!
    responses:
      200:
        description: Password reset successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Password reset successfully
      400:
        description: Invalid token or weak password
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Reset token is invalid or expired
    """
    payload = request.get_json(silent=True) or {}
    token = payload.get('token')
    password = payload.get('password')

    try:
        result = auth_service.reset_password(reset_token=token, new_password=password)
        return _json_response(True, result.get('message', 'Password reset successfully'))
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=400)


@auth_bp.route('/me', methods=['GET'])
@auth_required
def get_current_user(current_user):
    """
    Get current user
    ---
    tags:
      - Auth
    summary: Return the authenticated user's profile
    security:
      - Bearer: []
    responses:
      200:
        description: User data retrieved
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: User data retrieved
            data:
              type: object
              properties:
                user:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: John Doe
                    email:
                      type: string
                      example: john@example.com
                    role:
                      type: string
                      example: customer
      401:
        description: Missing, invalid, or revoked access token
    """
    return _json_response(True, 'User data retrieved', {'user': current_user.to_dict()})
