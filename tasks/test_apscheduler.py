from apscheduler.schedulers.blocking import BlockingScheduler


class TaskType:
    """定时器触发类型"""
    DATE = 'date'
    '''特定时间只触发一次'''
    CRON = 'cron'
    '''固定时间触发，父级时间不定义可循环'''
    INTERVAL = 'interval'
    '''固定时间间隔触发'''


def my_task():
    # 执行你的任务
    print("任务执行中...")


scheduler = BlockingScheduler()
# 定义定时规则
scheduler.add_job(my_task, TaskType.INTERVAL, seconds=60)  # 每10秒执行一次

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass
