import base64
import pickle
import logging
import sys
import time
import traceback
import threading
from django.apps import AppConfig
from django.db import connection
from django.db.models.signals import post_migrate
from djabbai.signals import handlers
from common.utils.threads import run_in_separate_thread, run_once
from ilock import ILock

logger = logging.getLogger(__name__)

class DjabbaiAppConfig(AppConfig):
    name = 'djabbai'
    verbose_name = 'Djabbai'

    @run_once
    def ready(self):
        logger.info('Starting app, thread #%s', threading.get_ident())

        # Perform one-time DB changes
        post_migrate.connect(handlers.create_notice_types)  # don't send self, as post_migrate is not called for apps without models

        #Start a thread to send notifications
        self.send_notifications_loop()

    # @run_once Doesn't work across processes
    @run_in_separate_thread
    def send_notifications_loop(self):
        logger.info('Starting notifications thread, #%s', threading.get_ident())
        while self.send_all():  # Since more than one Django process can be started, we want that the thread that fails to obtain the lock will be closed
            # sleep is done within send_all()
            pass
        # The thread that didn't obtain the lock also did not open a connection, but it's still a good practice...
        connection.close()

    # copied from venv\Lib\site-packages\pinax\notifications\engine.py - changed to remove non-functioning thread-locking
    # returns False if failed to obtain lock
    def send_all(*args):
        try:
            with ILock('send_all_notifications_lock', 0.01):
                time.sleep(10)  # although more appropriate in the calling function, the sleep here ensures that the second process times-out on the ILock, and closes the thread
                from django.contrib.sites.models import Site
                from django.contrib.auth import get_user_model
                from django.core.mail import mail_admins
                from pinax.notifications.models import NoticeQueueBatch
                from pinax.notifications.signals import emitted_notices
                from pinax.notifications import models as notification

                batches, sent, sent_actual = 0, 0, 0
                start_time = time.time()

                try:
                    for queued_batch in NoticeQueueBatch.objects.all():
                        notices = pickle.loads(base64.b64decode(queued_batch.pickled_data))
                        for user, label, extra_context, sender in notices:
                            try:
                                user = get_user_model().objects.get(pk=user)
                                logger.info("emitting notice {0} to {1}".format(label, user))
                                # call this once per user to be atomic and allow for logging to
                                # accurately show how long each takes.
                                if notification.send_now([user], label, extra_context, sender):
                                    sent_actual += 1
                            except get_user_model().DoesNotExist:
                                # Ignore deleted users, just warn about them
                                logger.info(
                                    "not emitting notice {0} to user {1} since it does not exist".format(
                                        label,
                                        user)
                                )
                            sent += 1
                        queued_batch.delete()
                        batches += 1
                    emitted_notices.send(
                        sender=NoticeQueueBatch,
                        batches=batches,
                        sent=sent,
                        sent_actual=sent_actual,
                        run_time="%.2f seconds" % (time.time() - start_time)
                    )
                except Exception:  # pylint: disable-msg=W0703
                    # get the exception
                    _, e, _ = sys.exc_info()
                    # email people
                    current_site = Site.objects.get_current()
                    subject = "[{0} emit_notices] {1}".format(current_site.name, e)
                    message = "\n".join(
                        traceback.format_exception(*sys.exc_info())  # pylint: disable-msg=W0142
                    )
                    mail_admins(subject, message, fail_silently=True)
                    # log it as critical
                    logger.error("Exception: {0}".format(e))

                if sent > 0:
                    logger.info("{0} batches, {1} sent".format(batches, sent, ))
                    logger.info("done in {0:.2f} seconds".format(time.time() - start_time))
                return True
        except Exception as e:
            logger.error("send_all Exception (thread #%s): %s", threading.get_ident(), e)
            return False
