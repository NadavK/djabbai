from django.apps import apps
from django.conf import settings
from django.utils.translation import ugettext_noop as _
from common.utils.threads import run_once


@run_once
def create_notice_types(sender, **kwargs):
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        print("Creating notification objects")
        NoticeType.create('profile_changed', _('Profile Changed'), _('A member changed their profile'))
    else:
        print("Skipping creation of NoticeTypes as notification app not found")

    # set the Site name (default is example.com)
    site = apps.get_model('sites', 'Site')
    site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={'domain': 'tzuri.myshul.nadalia.com', 'name': 'צורי'}
    )
