import logging

logger = logging.getLogger("loanhub.notifications")

class NotificationService:
    @staticmethod
    def send_status_update(email: str, application_number: str, new_status: str, message: str = ""):
        logger.info(f"[NOTIF] Status alert to {email} for loan {application_number}: status is now {new_status}. {message}")

    @staticmethod
    def send_sanction_notification(email: str, application_number: str, amount: float):
        logger.info(f"[NOTIF] Sanction letter generated for {application_number}. Amount sanctioned: {amount}. Sent to {email}.")
