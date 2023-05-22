import logging
from datetime import datetime, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from different_news.utils import update_news

from different_news.models import News


logger = logging.getLogger(__name__)


def update_news_job():
    print('Происходит обновление новостей')
    update_news()


def remove_old_news_job():
    print('Удаляем старые новости')
    # news = News.objects.all()
    # threshold = 5
    # for each in news:
    #     if each.date < datetime.now() - timedelta(days=threshold):
    #         each.delete()

# The `close_old_connections` decorator ensures that database connections, that have
# become unusable or are obsolete, are closed before and after your job has run. You
# should use it to wrap any jobs that you schedule that access the Django database in
# any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the
    database. It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical job execution
    records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            update_news_job,
            trigger=CronTrigger(hour="*/2"),  # Every 2 hours
            id="upd_news",
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added job 'upd_news'.")

        scheduler.add_job(
            remove_old_news_job,
            trigger=CronTrigger(hour="*/2"),  # Every 2 hours
            id="remove_news",
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added job 'remove_news'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
