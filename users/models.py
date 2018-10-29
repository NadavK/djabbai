from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

from parashot.models import Parasha
from users.managers import UserManager, ProfileManager


class Family(models.Model):
    parents = models.ManyToManyField('Profile', verbose_name='הורים', blank=True, related_name='family_of_parent')
    children = models.ManyToManyField('Profile', verbose_name='ילדים', blank=True, related_name='family_of_children')

    class Meta:
        verbose_name_plural = 'Families'

    def __str__(self):
        return "%s (#%s)" % (self.display_name(), self.id)

    def display_name(self, force_all_last_names=False):
        names = ""
        family_name = ""
        for parent in self.parents.all():
            if force_all_last_names:
                names = names + parent.display_name_with_family + ' + '
            else:
                names = names + parent.display_name + ' & '
                if not family_name:
                    family_name = parent.last_name
                elif parent.last_name and family_name != parent.last_name:        # someone in the family has a different last name
                    return self.display_name(force_all_last_names=True)

        return names[:-3] + ('' if force_all_last_names else ' ' + family_name)


def username_validator(value):
    if len(value) == 0:
        raise ValidationError('Username cannot be blank')
    if value.startswith(' ') or value.endswith(' '):
        raise ValidationError('Username cannot start/end with white-space')

class User(AbstractUser):


    objects = UserManager()

    class Meta:
        ordering = ('username',)

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        blank=True,                # overwritten to add "blank=True" - username is calculated dynamically
    )

    first_name = models.CharField(_('first name'), max_length=30)       # overwritten to remove the "blank=True"
    last_name = models.CharField(_('last name'), max_length=30)         # overwritten to remove the "blank=True"
    verification_code = models.IntegerField(blank=True, null=True, verbose_name='קוד אימות')     # Used to verify that a user can be created for an existing profile

    REQUIRED_FIELDS = ['first_name', 'last_name']           # used by Django just for creating a superuser


class Profile(models.Model):
    objects = ProfileManager

    class Meta:
        ordering = ('_display_name',)
        #unique_together = (("first_name", "last_name"),)

    class ReportBuilder:
        exclude = ('gender',)  # Lists or tuple of excluded fields
        #fields = ()  # Explicitly allowed fields
        #extra = ()  # List extra fields (useful for methods)

    # There are three profile types that denotes role:
    PROFILE_ROLE_INDEPENDENT = 1       # An INDEPENDENT profile can have duties, and cannot be edited by others
    PROFILE_ROLE_CONTROLLED = 2        # A CONTROLLED profile can have duties, and can be edited by an INDEPENDENT (typically a parent). Note that a parent's child can be a INDEPENDENT (and not a CONTROLLED), in which case the parents can no longer edit the profile
    PROFILE_ROLE_META = 3              # Needed to store an INDEPENDENT's parent's details, and can be edited by the INDEPENDENT. Note that an INDEPENDENT's parent can themselves be an INDEPENDENT (and not a META), in which case the the INDEPENDENT (son) cannot edit the profile

    PROFILE_GENDER_MALE = 'm'
    PROFILE_GENDER_FEMALE = 'f'
    PROFILE_GENDERS = (
        (PROFILE_GENDER_MALE, 'Male'),
        (PROFILE_GENDER_FEMALE, 'Female'),
    )

    PROFILE_TITLE_COHEN = 'cohen'
    PROFILE_TITLE_LEVI = 'levi'
    PROFILE_TITLE_YISRAEL = 'yisrael'
    PROFILE_TITLES = (
        (PROFILE_TITLE_COHEN, 'Cohen'),
        (PROFILE_TITLE_LEVI, 'Levi'),
        (PROFILE_TITLE_YISRAEL, 'Yisrael'),
    )

    MONTH_TISHREI = 1
    MONTH_MARCHESHVAN = 2
    MONTH_KISLEV = 3
    MONTH_TEVET = 4
    MONTH_SHVAT = 5
    MONTH_ADAR1 = 6
    MONTH_ADAR2 = 7
    MONTH_NISAN = 8
    MONTH_IYAR = 9
    MONTH_SIVAN = 10
    MONTH_TAMUZ = 11
    MONTH_AV = 12
    MONTH_ELUL = 13
    MONTHS = (
        (MONTH_TISHREI, 'תִּשׁרִי'),
        (MONTH_MARCHESHVAN, 'מַרְחֶשְׁוָן'),
        (MONTH_KISLEV, 'כִּסְלֵו'),
        (MONTH_TEVET, 'טֵבֵת'),
        (MONTH_SHVAT, 'שְׁבָט'),
        (MONTH_ADAR1, 'אֲדָר א׳'),
        (MONTH_ADAR2, 'אֲדָר ב׳'),
        (MONTH_NISAN, 'נִיסָן'),
        (MONTH_IYAR, 'אִיָּר'),
        (MONTH_SIVAN, 'סִיוָן‬'),
        (MONTH_TAMUZ, 'תַּמּוּז'),
        (MONTH_AV, 'אָב'),
        (MONTH_ELUL, 'אֱלוּל'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, blank=True, null=True)

    first_name = models.CharField(blank=True, verbose_name=_('שם פרטי'), max_length=30)         # First and last names are already defined in User, but we need them for Profiles without a User instance (set to blank for grandparents that don't need first/last names)
    last_name = models.CharField(blank=True, verbose_name=_('שם משפחה'), max_length=30)         # (allow blank for grandparents that don't need first/last names)
    _display_name = models.CharField(blank=True, max_length=30)      #, unique=True             # After initial creation, can only be changed by Gabbai
    full_name = models.CharField(blank=True, max_length=200, verbose_name='שם עברי ללא שם האב')
    title = models.CharField(blank=True, max_length=7, choices=PROFILE_TITLES, default=PROFILE_TITLE_YISRAEL, verbose_name='כהן, לוי, ישראל')

    duties = models.ManyToManyField('assignments.Duty', verbose_name='תפקידים', related_name='+', limit_choices_to={'applicable_for_profile': True}, blank=True)       # '+' == no related name

    default_family_to_add_children = models.ForeignKey(Family, null=True, blank=True, verbose_name='משפחה', help_text='ילדים חדשים יוצרפו למשפחה הזאת')
    #parents = models.ManyToManyField('Profile', verbose_name='הורים', blank=True, related_name='children')
    father_full_name = models.CharField(blank=True, max_length=200, verbose_name='אם אין קישור לאב, שם אב העברי')     # Only needed if father is empty

    dod_day = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='יארצייט - יום')                         # Yahrzeit Day
    dod_month = models.PositiveSmallIntegerField(blank=True, null=True, choices=MONTHS, verbose_name='יארצייט - חודש')      # Yahrzeit Month

    gender = models.CharField(blank=True, max_length=1, choices=PROFILE_GENDERS, verbose_name='זכר')
    bar_mitzvahed = models.BooleanField(default=True, verbose_name='בוגר', help_text='מעל גיל 13')
    bar_mitzvah_parasha = models.ForeignKey(Parasha, blank=True, null=True, related_name='people_with_this_barmitzvah_parasha', verbose_name='פרשת בר-מצווה')

    user_notes = models.TextField(blank=True, verbose_name='הערות של המשתמש')
    gabbai_notes = models.TextField(blank=True, verbose_name='הערות של הגבאי(לא מוצג למשתמש)')
    verification_code = models.IntegerField(blank=True, null=True, verbose_name='קוד אימות')     # Used to verify that a user can be created for an existing profile

    phone = models.CharField(blank=True, max_length=20, verbose_name='טלפון')
    email = models.CharField(blank=True, max_length=50, verbose_name='מייל')
    head_of_household = models.BooleanField(default=False, verbose_name='ראש משפחה', help_text='לסינון הדפסת רשימות')
    _kwargs_from_view = None

    @property
    def kwargs_from_view(self):
        return self._kwargs_from_view

    @kwargs_from_view.setter
    def kwargs_from_view(self, value):
        self._kwargs_from_view = value

    """
    List of prayer types
    """
    # kabalat_shabbat = models.NullBooleanField(blank=True, null=True, default=None, verbose_name='קבלת שבת')
    # maariv = models.NullBooleanField(blank=True, null=True, default=None, verbose_name='ערבית')
    # yigdal = models.NullBooleanField(blank=True, null=True, default=None, verbose_name='יגדל')
    # shaharit = models.NullBooleanField(blank=True, null=True, default=None, verbose_name='שחרית')
    # musaf = models.NullBooleanField(blank=True, null=True, default=None, verbose_name='מוסף')
    # anim_zmirot = models.NullBooleanField(blank=True, null=True, default=None, verbose_name='אנעים זמירות')

    # short_readings = models.NullBooleanField(blank=True, null=True, default=None, verbose_name='קריאות קצרות')
    # med_readings = models.NullBooleanField(blank=True, null=True, default=None, verbose_name='קריאות בינוניות')
    # long_readings = models.NullBooleanField(blank=True, null=True, default=None, verbose_name='קריאות ארוכות')
    # dvar_torah = models.NullBooleanField(blank=True, null=True, default=None, verbose_name='דבר תורה')

    #sms/push

    def __str__(self):
        if self.display_name:
            return "%s (#%s)" % (self.display_name, self.id)
        else:           # If display name is empty, then so is first_name & last_name
            return "%s (#%s)" % (self.full_name, self.id)

    def _display_name_helper(self, with_family=False):
        if self._display_name:
            return self._display_name
        elif self.first_name:
            return self.first_name + (' ' + self.last_name if with_family else '')
        else:
            return self.full_name

    @property
    def display_name(self):
        return self._display_name_helper()

    @property
    def display_name_with_family(self):
        return self._display_name_helper(True)

    @receiver(pre_save, sender=User)
    def pre_save_user(sender, instance, *args, **kwargs):
        # Nothing to check if user already exists (was checked when user was first created)
        if instance.pk:
            return

        # If a profile already exists for new user, then check that verification_code matches (for creating a user for a child or spouse)
        try:
            profile = Profile.objects.get(first_name=instance.first_name, last_name=instance.last_name)
            if instance.verification_code != profile.verification_code:
                raise ValidationError('Profile already exits. Set correct Verification Code')
            return
        except Profile.DoesNotExist:
            pass

        # If instance.verification_code was set, then override existing profile name (give child opportunity to 'fix' their name
        if instance.verification_code:
            try:
                profile = Profile.objects.get(verification_code=instance.verification_code)
                if profile.first_name:
                    profile.first_name=instance.first_name
                if profile.last_name:
                    profile.last_name=instance.last_name
                profile.save()
            except Profile.DoesNotExist:
                raise ValidationError('Profile not found for Verification Code')

    @receiver(post_save, sender=User)
    def create_update_user_profile(sender, instance, created, **kwargs):
        """
        This function called when a new user is created, so we create a linked profile
        """
        if created:     # Created means a new record was created - Add
            #Check if a profile already exists
            try:
                profile=Profile.objects.get(first_name=instance.first_name, last_name=instance.last_name)
                profile.user = instance
                profile.save()
                logger.debug('FOUND PROFILE verification_code %s', instance.verification_code)
            except Profile.DoesNotExist:    # So create a profile for this user
                Profile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)
        else:           # This is edit
            if instance.profile.first_name != instance.first_name or instance.profile.last_name != instance.last_name:
                logger.debug('User edited, updating profile:  %s  %s', instance.first_name, instance.last_name)
                instance.profile.first_name = instance.first_name
                instance.profile.last_name = instance.last_name
                #instance.profile.display_name = instance.username
                instance.profile.save()

    def save(self, *args, **kwargs):
        if not self.full_name and not (self.first_name and self.last_name):
            raise ValidationError('Either Full-Name, or First & Last names must be set')

        super().save(*args, **kwargs)

        # kwargs_from_view is injected by the View during create to signify if self is a spouse or child
        if self.kwargs_from_view:
            if 'child_of' in self.kwargs_from_view:
                associated_parent = self.kwargs_from_view.pop('child_of')           # self is the child of parent
                associated_parent.set_family(child=self)
            elif 'spouse_of' in self.kwargs_from_view:
                associated_spouse = self.kwargs_from_view.pop('spouse_of')          # self and spouse are, um, spice
                associated_spouse.set_family(spouse=self)
            elif 'child' in self.kwargs_from_view:
                child = self.kwargs_from_view.pop('child')                          # self is parent of child
                if child.parents:                                                   # Check if child already has a parent with a family, and if so, add this parent to the same family
                    self.default_family_to_add_children = child.parents[0].default_family_to_add_children
                self.set_family(child=child)
                child.parents[0].set_family(spouse=self)

        # Maybe we can move these to pres_save?
        if not self.user and not self.verification_code:
            self.verification_code = randint(10000, 99999)    # Will be used in the future to verify that a user can be created for this profile. TODO: Should really check that code is unique
            self.save()
            return

        if self.user and self.verification_code:
            self.verification_code = None                   # User exists, time to remove the verification code
            self.save()
            return

        #Force Kiddush Duty (it's a M2M, so has to be added after saving self)
        if not self.duties.filter(pk=19).exists():
            self.duties.add(19)

    @property
    def father(self):
        if self.parents:
            return self.parents.filter(gender=self.PROFILE_GENDER_MALE).first()

    @property
    def mother(self):
        if self.parents:
            return self.parents.filter(gender=self.PROFILE_GENDER_FEMALE).first()

    @property
    def profile_role(self):
        """
        Can be: Member, Child, or Father.
        """
        if self.user:
            return self.PROFILE_ROLE_INDEPENDENT                    # typically a parent, or a child that has their own account
        elif self.parents.filter(user__isnull=False).exists():       # Is a parent controlling this profile?
            return self.PROFILE_ROLE_CONTROLLED                     # a parent is an INDEPENDENT, so this is a CONTROLLED (child)
        else:
            return self.PROFILE_ROLE_META                           # must be the father of an INDEPENDENT, but we don't actually check

    @property
    def spouse(self):
        if not self.default_family_to_add_children:
            return None
        try:
            return self.default_family_to_add_children.parents.exclude(pk=self.pk).get()
        except Profile.DoesNotExist:
            return None

    @property
    def parents(self):
        family = self.family_of_children.first()          # Can a child exist in more than one family?
        if family:
            return family.parents.all()
        return Profile.objects.none()

    @property
    def children(self):
        children = []
        for family in self.family_of_parent.all():
            children += family.children.all()
        return children

    @property
    def male(self):
        return self.gender != self.PROFILE_GENDER_FEMALE

    def set_family(self, spouse=None, child=None):
        if not self.default_family_to_add_children:
            logger.debug('Creating default family for %s', self)
            self.default_family_to_add_children = Family.objects.create()
            logger.debug('self.default_family_to_add_children: %s', self.default_family_to_add_children)
            self.default_family_to_add_children.save()
            self.default_family_to_add_children.parents.add(self)
            logger.debug('self.default_family_to_add_children: %s', self.default_family_to_add_children)
            self.default_family_to_add_children.save()
            logger.debug('Created family count: %s', Family.objects.all().count())
            self.save()
        if spouse:
            logger.debug('Creating default family for %s', spouse)
            self.default_family_to_add_children.parents.add(spouse)
            spouse.default_family_to_add_children = self.default_family_to_add_children
            spouse.save()
        if child:
            self.default_family_to_add_children.children.add(child)
            # Add direct .father and .mother
            #for parent in self.default_family_to_add_children.parents.all():
            #    child.parents.add(parent)
            # child.save()

    def has_permission(self, requesting_profile_pk=None, write_permission=False):
        """
        Returns true if requesting_profile_pk can edit self (is self, spouse or parent)
        :param requesting_profile_pk: The profile that is asking access to self
        :return: Boolean
        """

        # An INDEPENDENT role cannot be edited by another profile (but can be viewed)
        if (self.profile_role == self.PROFILE_ROLE_INDEPENDENT) and write_permission:
            return False

        requesting_profile = None
        if isinstance(requesting_profile_pk, Profile):
            requesting_profile = requesting_profile_pk
            int_requesting_profile_pk = requesting_profile_pk.pk
        else:
            try:
                int_requesting_profile_pk = int(requesting_profile_pk)
            except:
                raise Exception('Invalid user id')

        if self.pk == int_requesting_profile_pk:        # Self has permission to themselves
            return True

        try:
            if not requesting_profile:
                requesting_profile = Profile.objects.get(pk=int_requesting_profile_pk)
        except Exception as e:
            raise Exception('has_permission: Cannot find profile id #%d. %s' % (int_requesting_profile_pk, e))

        # If the role is META, then check if it is a parent of self or spouse
        if self.profile_role == self.PROFILE_ROLE_META:
            if requesting_profile.parents.filter(pk=self.pk).exists():
                return True
            if requesting_profile.spouse and requesting_profile.spouse.parents.filter(pk=self.pk).exists():
                return True

        # Check for children or spouse (we already know requesting_profile is not INDEPENDENT if write_permission is True)
        for family in requesting_profile.family_of_parent.all():
            if family.children.filter(pk=self.pk).exists() or family.parents.filter(pk=self.pk).exists():
                return True

        return False

    def authorized_pks(self, write_permission=False):
        pks = [self.pk,]
        parents = self.parents
        if self.spouse:
            if not write_permission or (self.spouse.profile_role != self.PROFILE_ROLE_INDEPENDENT):
                pks.append(self.spouse.pk)
                parents |= self.spouse.parents
        for parent in parents:
            #pks.append(self.parents.all().values_list('pk', flat=True))       #this returns a queryset?!?
            if not write_permission or (parent.profile_role != self.PROFILE_ROLE_INDEPENDENT):      # child cannot write to independent parent
                pks.append(parent.pk)

        for family in self.family_of_parent.all():
            #pks.append(family.children.all().values_list('pk', flat=True))       #this returns a queryset?!?
            for child in family.children.all():
                if not write_permission or (child.profile_role != self.PROFILE_ROLE_INDEPENDENT):  # parent cannot write to independent child
                    pks.append(child.pk)

        return pks

    def get_father_name_title(self):
        if self.father and self.father.full_name:
            return self.father.full_name, self.father.title
        else:
            return self.father_full_name, self.title

    def get_full_aliya_name(self):           # TODO: move to Profile model class
        def get_son_or_daughter_midfix(user):
            return ' בן ' if user.male else ' בת '

        def postfix_user_type(name, user_type):
            if user_type == Profile.PROFILE_TITLE_COHEN:
                name = name + " הכהן"
            elif user_type == Profile.PROFILE_TITLE_LEVI:
                name = name + " הלוי"
            return name

        full_name = self.full_name

        father_full_name, title = self.get_father_name_title()
        if father_full_name:
            full_name = full_name + get_son_or_daughter_midfix(self) + father_full_name
        return postfix_user_type(full_name, title)
