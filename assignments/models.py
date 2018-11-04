import reversion
from django.db import models
from parashot.models import Parasha
from users.models import Profile


class Duty(models.Model):
    """
    List of tafkidim types
    """
    category = models.CharField(max_length=30)
    name = models.CharField(max_length=30, unique=True)
    order_id = models.IntegerField(unique=True)

    applicable_for_profile = models.BooleanField(default=True)                   # Users can select this role in their profile
    not_applicable_for_roster = models.BooleanField(default=False)               # This is just a profile duty, and cannot be used in the duty-roster
    applicable_for_adults = models.BooleanField(default=True)
    applicable_for_children = models.BooleanField(default=False)                 # A child in this context is meant to be under bar-mitzvah

    applicable_for_shabbat = models.BooleanField(default=True)
    applicable_for_hag = models.BooleanField(default=False)
    applicable_for_mevarchim = models.BooleanField(default=False)
    #relevent_for_roshhodesh = models.BooleanField(default=False)

    class Meta:
        unique_together = (('category', 'name'),)
        ordering = ['order_id']
        verbose_name_plural = 'Duties'

    def __str__(self):
        #return "%s-%s" % (self.category, self.name)
        return self.name


class Shabbat(models.Model):
    """
    A specific shabbat/hag
    """
    dayt = models.DateField(unique=True, blank=False, null=False, verbose_name='תאריך')     # intentional mispelling to overcome reserved word
    parasha = models.ForeignKey(Parasha, related_name='shabbats', verbose_name='פרשה')
    duties = models.ManyToManyField(Duty, through='Roster', verbose_name='תפקידים')#, related_name='Shabbats')

    class Meta:
        verbose_name_plural = 'Shabbatot'

    def __str__(self):
        return "%s %s (#%s)" % (self.dayt, self.parasha, self.id)


class Roster(models.Model):
    shabbat = models.ForeignKey(Shabbat) #, related_name='roster')
    duty = models.ForeignKey(Duty, verbose_name='תפקידים', limit_choices_to={'not_applicable_for_roster': False}) #, related_name='roster')
    profiles = models.ManyToManyField(Profile, through='Assignment', verbose_name='תפקידים')#, related_name='Shabbats')

    def __str__(self):
        #return "Assignment (#%s): %s>%s/%s" % (self.id, self.get_tafkid_display(), self.user, self.get_status_display())
        return "%s>%s (#%s)" % (self.duty.name, self.profiless.count(), self.id)

    class Meta:
        unique_together = (('duty', 'shabbat'),)
        ordering = ['shabbat__pk']


@reversion.register()
class Assignment(models.Model):

    STATUS_OFFERED = 'OFFERED'
    STATUS_CONFIRMED = 'CONFIRMED'
    STATUS_POSTPONED = 'POSTPONED'
    STATUS_REFUSAL = 'REFUSAL'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_TYPES = (
        (STATUS_OFFERED, 'הוצע'),
        (STATUS_CONFIRMED, 'אושר'),
        (STATUS_POSTPONED, 'נדחה'),      # User asked to be assigned at a different date
        (STATUS_REFUSAL, 'ויתור'),       # User skips assignment
        (STATUS_CANCELLED, 'בוטל'),      # Cancelled by Gabbai
    )

    OFFER_TYPE_REGULAR = 'REGULAR'
    OFFER_TYPE_STANDIN = 'STANDIN'
    OFFER_TYPE_SPECIAL = 'SPECIAL'
    OFFER_TYPES = (
        (OFFER_TYPE_REGULAR, 'רגיל'),
        (OFFER_TYPE_STANDIN, 'מחליף'),  # Gabbai requested last-minute replacement - Is not counted as a 'turn'
        (OFFER_TYPE_SPECIAL, 'מיוחד'),  # Simcha - Is not counted as a 'turn'
    )

    roster = models.ForeignKey(Roster, related_name='assignments')
    profile = models.ForeignKey(Profile, related_name='assignments')
    status = models.CharField(max_length=10, choices=STATUS_TYPES, default=STATUS_OFFERED)
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES, default=OFFER_TYPE_REGULAR)

    class Meta:
        unique_together = (('roster', 'profile'),)        # User cannot be duplicated in same assignment-list
        ordering = ['pk']

    def __str__(self):
        #return "Assignment (#%s): %s>%s/%s" % (self.id, self.get_tafkid_display(), self.user, self.get_status_display())
        return "%s>%s/%s (#%s)" % (self.roster, self.profile, self.get_status_display(), self.id)
