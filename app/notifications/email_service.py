"""
SMTP email notifications using Flask-Mail.
"""

import logging
from flask import current_app
from flask_mail import Message

from app.extensions.mail import mail

logger = logging.getLogger(__name__)


def _is_mail_configured():
    """Return True when required SMTP settings are present."""
    return bool(
        current_app.config.get('MAIL_SERVER')
        and current_app.config.get('MAIL_USERNAME')
        and current_app.config.get('MAIL_PASSWORD')
    )


def _send_email(recipient, subject, html_body):
    """Send an HTML email. Failures are logged and do not raise."""
    if not recipient:
        logger.warning('Email not sent: recipient is missing')
        return False

    if not _is_mail_configured():
        logger.warning('Email not sent: MAIL_SERVER, MAIL_USERNAME, or MAIL_PASSWORD is not configured')
        return False

    try:
        message = Message(
            subject=subject,
            recipients=[recipient],
            html=html_body,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
        )
        mail.send(message)
        logger.info('Email sent to %s with subject: %s', recipient, subject)
        return True
    except Exception as exc:
        logger.exception('Failed to send email to %s: %s', recipient, exc)
        return False


def _password_reset_html(user_name, reset_token):
    return f"""
    <html>
      <body>
        <h2>Password Reset Request</h2>
        <p>Hello {user_name},</p>
        <p>We received a request to reset your password. Use the token below:</p>
        <p><strong>{reset_token}</strong></p>
        <p>Send this token to <code>POST /auth/reset-password</code> with your new password.</p>
        <p>If you did not request this, you can ignore this email.</p>
      </body>
    </html>
    """


def _shipment_created_html(user_name, shipment):
    return f"""
    <html>
      <body>
        <h2>Shipment Created</h2>
        <p>Hello {user_name},</p>
        <p>Your shipment has been created successfully.</p>
        <ul>
          <li><strong>Tracking ID:</strong> {shipment.tracking_id}</li>
          <li><strong>Status:</strong> {shipment.status}</li>
          <li><strong>Receiver:</strong> {shipment.receiver_name}</li>
          <li><strong>Delivery Address:</strong> {shipment.delivery_address}</li>
        </ul>
        <p>Thank you for using our logistics service.</p>
      </body>
    </html>
    """


def _shipment_delivered_html(user_name, shipment):
    return f"""
    <html>
      <body>
        <h2>Shipment Delivered</h2>
        <p>Hello {user_name},</p>
        <p>Your shipment <strong>{shipment.tracking_id}</strong> has been delivered.</p>
        <ul>
          <li><strong>Receiver:</strong> {shipment.receiver_name}</li>
          <li><strong>Delivery Address:</strong> {shipment.delivery_address}</li>
        </ul>
        <p>Thank you for choosing our logistics service.</p>
      </body>
    </html>
    """


def send_password_reset_email(user, reset_token):
    """Send a password reset email to the user."""
    html_body = _password_reset_html(user.name, reset_token)
    return _send_email(
        recipient=user.email,
        subject='Password Reset Request',
        html_body=html_body,
    )


def send_shipment_created_email(user, shipment):
    """Send a shipment created confirmation email to the customer."""
    html_body = _shipment_created_html(user.name, shipment)
    return _send_email(
        recipient=user.email,
        subject=f'Shipment Created - {shipment.tracking_id}',
        html_body=html_body,
    )


def send_shipment_delivered_email(user, shipment):
    """Send a shipment delivered notification email to the customer."""
    html_body = _shipment_delivered_html(user.name, shipment)
    return _send_email(
        recipient=user.email,
        subject=f'Shipment Delivered - {shipment.tracking_id}',
        html_body=html_body,
    )
