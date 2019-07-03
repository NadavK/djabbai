import logging
from itertools import chain
from random import randint
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from reversion.signals import post_revision_commit
from parashot.models import Parasha
from users.managers import UserManager, ProfileManager

logger = logging.getLogger(__name__)

class Family(models.Model):
    parents = models.ManyToManyField('Profile', verbose_name='הורים', blank=True, related_name='family_of_parent')
    children = models.ManyToManyField('Profile', verbose_name='ילדים', blank=True, related_name='family_of_children')

    class Meta:
        verbose_name_plural = 'Families'

    def __str__(self):
        return self.display_name()

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

    #username is set in ui to first_name + '_' + last_name
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
    verification_code = models.IntegerField(blank=True, null=True, verbose_name='קוד אימות')     # Used to verify that a user can be created for an existing profile. Defined  in the User model to make it easier to pass the verification code as part of creating a new user (was not able to serialize a non-db field)
    profile_id = models.IntegerField(blank=True, null=True, verbose_name='מספר פורפיל')          # Specifies the target profile for create. Defined in the User model to make it easier to pass the profile as part of creating a new user (was not able to serialize a non-db field)

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

    default_family_to_add_children = models.ForeignKey(Family, null=True, blank=True, verbose_name='משפחה', help_text='ילדים חדשים יצורפו למשפחה זאת')
    #parents = models.ManyToManyField('Profile', verbose_name='הורים', blank=True, related_name='children')
    father_full_name = models.CharField(blank=True, max_length=200, verbose_name='אם אין קישור לאב, שם אב העברי')     # Only needed if father is empty

    dod_day = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='יארצייט - יום')                         # Yahrzeit Day
    dod_month = models.PositiveSmallIntegerField(blank=True, null=True, choices=MONTHS, verbose_name='יארצייט - חודש')      # Yahrzeit Month

    gender = models.CharField(blank=True, max_length=1, choices=PROFILE_GENDERS, verbose_name='מין')
    bar_mitzvahed = models.BooleanField(default=False, verbose_name='בוגר', help_text='מעל גיל 13')
    bar_mitzvah_parasha = models.ForeignKey(Parasha, blank=True, null=True, related_name='people_with_this_barmitzvah_parasha', verbose_name='פרשת בר-מצווה')

    user_notes = models.TextField(blank=True, verbose_name='הערות', help_text='הערות של המשתמש לגבאי')
    gabbai_notes = models.TextField(blank=True, verbose_name='הערות של הגבאי', help_text='(לא מוצג למשתמש)')
    verification_code = models.IntegerField(blank=True, null=True, verbose_name='קוד אימות')     # Used to verify that a user can be created for an existing profile
    #the verification_code must match either the spouse, one of the parents, or an existing profile

    phone = models.CharField(blank=True, max_length=20, verbose_name='טלפון')
    #email = models.CharField(blank=True, max_length=50, verbose_name='מייל')
    email = models.EmailField(blank=True, verbose_name='מייל')
    rcv_user_emails = models.BooleanField(default=True, verbose_name='מיילים אישיים', help_text='מיילים הקשורים לתפקוד המשתמש')
    rcv_admin_emails = models.BooleanField(default=False, verbose_name='מיילים ניהוליים', help_text='מיילים הקשורים לתפקוד הגבאי')
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
            return self.display_name
        else:           # If display name is empty, then so is first_name & last_name
            return self.full_name

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
            if not profile.verify_verification_code(instance.verification_code):
                raise ValidationError('Profile already exits for that name, but Verification Code is incorrect')
            if instance.profile_id and instance.profile_id != profile.pk:
                raise ValidationError('That name is already in-use by a different profile')
            instance.profile_id = profile.pk
            return
        except Profile.DoesNotExist:
            print('Profile.DoesNotExist')
            pass

        # If instance.verification_code was set, then check that a matching profile exists (objects will be updated in post_save)
        if instance.profile_id:
            try:
                profile = Profile.objects.get(pk=instance.profile_id)
                if not profile.verify_verification_code(instance.verification_code):
                    raise ValidationError('Verification Code does not match Profile ID')
            except Profile.DoesNotExist:
                raise ValidationError('Profile ID not found')
        elif instance.verification_code:
            try:
                print('has verification_code without profile_id')
                profile = Profile.objects.get(verification_code=instance.verification_code)
                if profile.profile_role == Profile.PROFILE_ROLE_INDEPENDENT:                    # This profile already has a user
                    raise ValidationError('The profile associated with the Verification Code is already signed-up (did you meant to sign-up a specific Profile ID?')
                instance.profile_id = profile.pk
            except Profile.DoesNotExist:
                raise ValidationError('Verification Code not matched')

    @receiver(post_save, sender=User)
    def create_update_user_profile(sender, instance, created, **kwargs):
        """
        This function is called when a new user is created/edited, so we create/update the linked profile
        """
        need_to_save_profile = False
        if created:     # Created means a new user was created - Check if a profile needs to be created
            if instance.profile_id:
                try:
                    instance.profile = Profile.objects.get(pk=instance.profile_id)
                    logger.debug('FOUND PROFILE verification_code %s on profile #%s', instance.verification_code, instance.profile.pk)
                    need_to_save_profile = True
                except Profile.DoesNotExist:  # So create a profile for this user
                    logger.debug('Profile ID %s not found ', instance.profile_id)
                    raise ValidationError('ProfileID not found')
            else:
                logger.debug('Creating new profile for user #%s', instance.pk)
                instance.profile = Profile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)      # setting instance.profile for continuation of this function that compares betweeen user and profile names

        #Check if profile names should be updated from user
        if instance.profile.first_name != instance.first_name or instance.profile.last_name != instance.last_name:
            logger.debug('User edited, updating profile:  %s  %s', instance.first_name, instance.last_name)
            instance.profile.first_name = instance.first_name
            instance.profile.last_name = instance.last_name
            #instance.profile.display_name = instance.username
            need_to_save_profile = True

        if need_to_save_profile:
            instance.profile.save()

    def generate_verification_code(self):
        self.verification_code = randint(100000, 999999)
        # Check that code is unique
        while Profile.objects.filter(verification_code=self.verification_code).exists():
            self.verification_code = randint(100000, 999999)

    def verify_verification_code(self, verification_code):
        return self.verify_verification_code_with_metadata(verification_code)[0]

    # returns a tuple: verification_code_bool, family, family_relation, verification_code_relation
    def verify_verification_code_with_metadata(self, verification_code):
        try:
            #family = Family.objects.get(parents__pk=self.pk)  # First check if user is a parent
            family = Family.objects.get(parents=self)  # First check if user is a parent
            family_relation = 'spouse'
        except Family.DoesNotExist:
            try:
                family = Family.objects.get(children=self)  # If not a parent, maybe a child?
                family_relation = 'child'
            except Family.DoesNotExist:
                return None, None, None, None

        verification_code_bool = False
        verification_code_relation = None
        if verification_code:
            # For a child, check if any of the parents' codes work
            # For a spouse, check if the (any) spouse's code work
            # And it can also match the current profile
            if str(self.verification_code) == str(verification_code):
                verification_code_bool = True
                verification_code_relation = 'self'
            if not verification_code_bool:
                # both spouse and children are verified with the parent's verification_code (it's the family's parents, not the profile's parents)
                verification_code_relation = 'parent'
                for parent in family.parents.all():
                    if verification_code and str(parent.verification_code) == str(verification_code):
                        verification_code_bool = True

        return verification_code_bool, family, family_relation, verification_code_relation

    # Returns related non-independent profiles (profiles that can be activated with this profile's verification_code)
    def related_non_independent_profiles(self):
        profiles = []
        verification_code_bool, family, family_relation, verification_code_relation = self.verify_verification_code_with_metadata(self.verification_code)
        if family:
            for profile in [self] if family_relation == 'child' else list(chain([self], family.children.all(), family.parents.all())):
                if profile.profile_role != Profile.PROFILE_ROLE_INDEPENDENT:
                    profiles.append(profile)

        return profiles

    def save(self, *args, **kwargs):
        if not self.full_name and not (self.first_name and self.last_name):
            raise ValidationError('Either Full-Name, or First & Last names must be set')

        # Verification-code is used when creating a new user to associate with an existing child/parent/spouse profile
        if not self.verification_code:
            self.generate_verification_code()

        super().save(*args, **kwargs)

        # kwargs_from_view is injected by the View during create to signify if self is a spouse or child
        if self.kwargs_from_view:
            if 'child_of' in self.kwargs_from_view:                                 # self is the child of parent
                parent = self.kwargs_from_view.pop('child_of')
                # Check if parent should be head of family
                if parent and not parent.head_of_household and parent.first_name and parent.last_name:  # profile with no first and last name is a non-member parent
                    parent.head_of_household = True
                    #parent.save()           # save is done by set_family()
                parent.set_family(child=self)
            elif 'spouse_of' in self.kwargs_from_view:                              # self and spouse are, um, spice
                spouse = self.kwargs_from_view.pop('spouse_of')
                # Check if spouse should be head of family
                if not spouse.head_of_household and spouse.male and spouse.first_name and spouse.last_name:  # profile with no first and last name is a non-member parent
                    spouse.head_of_household = True
                    #spouse.save()           # save is done by set_family()
                spouse.set_family(spouse=self)
            elif 'child' in self.kwargs_from_view:                                  # self is parent of child
                child = self.kwargs_from_view.pop('child')
                if child.parents:                                                   # Check if child already has a parent with a family, and if so, add this parent to the same family
                    self.default_family_to_add_children = child.parents[0].default_family_to_add_children
                self.set_family(child=child)
                child.parents[0].set_family(spouse=self)

        # Force Kiddush Duty (it's a M2M, so has to be added after saving self)
        if self. head_of_household and not self.duties.filter(pk=19).exists():
            self.duties.add(19)

    # Send admmin notifications on changes to profile
    @receiver(post_revision_commit)
    def on_revision_commit(revision, versions, **kwargs):
        from django.template.loader import render_to_string
        from pinax.notifications.models import queue
        from reversion.models import Version
        from reversion_compare.mixins import CompareMixin, CompareMethodsMixin

        class MyCompare(CompareMixin, CompareMethodsMixin):
            compare_exclude = ['bar_mitzvah_parasha', 'default_family_to_add_children', 'email', 'phone', 'verification_code', 'gabbai_notes', 'rcv_admin_emails', 'rcv_user_emails', 'head_of_household']

        try:
            # need the previous version of the main object (versions is a list of all changes to all affected-objects)
            previous_versions = (Version.objects.get_for_object(versions[0].object)).order_by("-pk")[1:2]
            diff, has_unfollowed_fields = MyCompare().compare(versions[0].object, previous_versions[0], versions[0])
            if (len(diff) == 0):
                return      # no changes, so don't need notification

            context = {
                'compare_data': diff,
                'version2': previous_versions[0],
                'user': versions[0].object.display_name_with_family
            }
            html = render_to_string('reversion-compare/compare_partial.html', context)

            #send to all users with rcv_admin_emails profiles
            for profile in Profile.objects.filter(rcv_admin_emails=True).select_related('user'):
                # notification library expects users (not profiles)
                profile.user.email = profile.email  # this project does not use the user model to maintain emails; need to add it temporarily for  notification to work
                queue([profile.user], 'profile_changed', {'message': 'עדכון פרופיל', 'from_user': context["user"], 'html': html})
        except Exception as e:
            logger.error("Error comparing revisions: %s", e)

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
        elif self.parents.filter(user__isnull=False).exists():      # Is a parent controlling this profile?
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
        return self.gender == self.PROFILE_GENDER_MALE

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
