from datetime import date, datetime, timedelta

from backend.services.db.sleep_log import get_sleep_logs


async def get_time_sleep_dashboard(session, user_id):
    week_ago = datetime.now().date() - timedelta(weeks=1)
    logs = await get_sleep_logs(
        session, user_id, start_date=week_ago, end_date=datetime.now().date()
    )

    sleep_durations = []
    for log in logs:
        bedtime_dt = datetime.combine(log.date, log.bedtime)
        wake_dt = datetime.combine(log.date, log.wake_time)

        if wake_dt < bedtime_dt:
            wake_dt += timedelta(days=1)

        sleep_durations.append(wake_dt - bedtime_dt)

    return sleep_durations
