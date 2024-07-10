import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, MailingLog

logger = logging.getLogger(__name__)


def my_job():
    """
    Функция для отправки рассылок клиентам.
    Проверяет все активные рассылки и отправляет их, если они готовы к отправке.
    """
    error = None
    last_attempt = None
    log_status = None

    mailings = Mailing.objects.all().filter(is_active=False, status='created')
    try:
        for mailing in mailings:
            if mailing.periodicity == 'once_day':
                if mailing.start_mailing >= timezone.now() or mailing.next_mailing >= timezone.now():
                    send_mail(
                        subject=mailing.message.title,
                        message=mailing.message.message,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=mailing.recipients,
                    )
                    last_attempt = timezone.now()
                    log_status = 'successful'

            elif mailing.periodicity == 'once_week':
                if mailing.start_mailing >= timezone.now() or mailing.next_mailing >= timezone.now():
                    send_mail(
                        subject=mailing.message.title,
                        message=mailing.message.message,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=mailing.recipients,
                    )
                    last_attempt = timezone.now()
                    log_status = 'successful'

            elif mailing.periodicity == 'once_month':
                if mailing.start_mailing >= timezone.now() or mailing.next_mailing >= timezone.now():
                    send_mail(
                        subject=mailing.message.title,
                        message=mailing.message.message,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=mailing.recipients,
                    )
                    last_attempt = timezone.now()
                    log_status = 'successful'

                    mailing.status = 'executing'
                    mailing.is_active = True
                    mailing.save()

            elif mailing.end_mailing >= timezone.now():
                mailing.is_active = False
                Mailing.periodicity = 'finished'
                mailing.save()

    except Exception as e:
        last_attempt = timezone.now()
        log_status = 'not_successful'
        error = f'{e}'
        print("Ошибка при отправке письма: {}".format(e))
    finally:
        log = MailingLog(last_attempt=last_attempt, status=log_status, server_response=error)
        log.save()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

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


# Функция старта периодических задач
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_job, 'interval', seconds=120)
    scheduler.start()
