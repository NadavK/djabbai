from users.models import User
import logging
logger = logging.getLogger(__name__)

class NoUsernameModelBackend_NOT_IN_USE:
    def authenticate(self, first_name=None, last_name=None, password=None):
        logger.error('LOGIN: %s %s %s', first_name, last_name, password)
        try:
            user = User.objects.get(first_name=first_name, last_name=last_name)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        logger.debug('get_user: %s', user_id)
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
