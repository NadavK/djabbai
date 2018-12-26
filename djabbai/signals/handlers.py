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

    # Only head-of-households require the Kiddush duty
    from users.models import Profile
    qs = Profile.duties.through.objects.filter(profile__head_of_household=False, duty__pk=19).delete()

    #Generate verification codes
    print('************************** Generating verification codes ************************************')
    from users.models import Profile
    #qs = Profile.objects.filter(verification_code__isnull=True)
    qs = Profile.objects.all()
    print('Generating verification code for profiles: ', qs.count())
    for p in qs:
        p.generate_verification_code()
        p.save()
    print('************************** Finished Generating verification codes ************************************')
