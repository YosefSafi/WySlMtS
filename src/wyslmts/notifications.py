from plyer import notification

def send_notification(title: str, message: str):
    """
    Send a desktop notification.
    """
    try:
        notification.notify(
            title=f"WySlMtS: {title}",
            message=message,
            app_name="WySlMtS",
            timeout=10
        )
    except Exception:
        # Silently fail if notifications aren't supported
        pass
