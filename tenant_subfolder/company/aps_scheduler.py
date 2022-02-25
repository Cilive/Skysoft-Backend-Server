from apscheduler.schedulers.background import BackgroundScheduler
from .session_close import close_sessions


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(close_sessions,   trigger='interval',seconds=10)
    scheduler.add_job(close_sessions,  trigger='cron', hour='23', minute='51')
    scheduler.start()