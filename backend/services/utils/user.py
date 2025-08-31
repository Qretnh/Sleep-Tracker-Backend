from backend.db.models import User


def format_user_notifications(user: User) -> User:
    """Форматирует поля morning_notification и evening_notification в 'HH:MM'."""
    if user.morning_notification:
        user.morning_notification = user.morning_notification.strftime("%H:%M")
    if user.evening_notification:
        user.evening_notification = user.evening_notification.strftime("%H:%M")
    return user
