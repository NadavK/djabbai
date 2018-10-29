from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.query import QuerySet
from django.contrib.auth.models import AbstractUser


class CaseInsensitiveUsernameQuerySet(QuerySet):
    # https://djangosnippets.org/snippets/305/
    def _filter_or_exclude(self, mapper, *args, **kwargs):
        # 'usernname' is the field in your Model whose lookups you want case-insensitive by default
        if 'username' in kwargs:
            kwargs['username__iexact'] = kwargs['username']
            del kwargs['username']
        return super(CaseInsensitiveUsernameQuerySet, self)._filter_or_exclude(mapper, *args, **kwargs)


class UserManager(DjangoUserManager):

    def get_queryset(self):
        #return CaseInsensitiveUsernameQuerySet(self.model)
        return CaseInsensitiveUsernameQuerySet(self.model).select_related('profile')

    def get_by_natural_key(self, username):
        # case-insensitive username login (https://code.djangoproject.com/ticket/2273)
        #case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        #return self.get(**{case_insensitive_username_field: username})
        return self.get(username__iexact=username)

    def create_user(self, **extra_fields):
        extra_fields['username'] = self.generate_username(extra_fields['first_name'], extra_fields['last_name'])
        #email = extra_fields.get('email')
        #password = extra_fields.get('password')
        #return super(UserManager, self).create_user(username, email, password, **extra_fields)
        return super(UserManager, self).create_user(**extra_fields)

    def XXXcreate_user(self, username, email=None, password=None, **extra_fields):
        username = self.generate_username(extra_fields['first_name'], extra_fields['last_name'])
        return super(UserManager, self).create_user(username, email, password, **extra_fields)

    def perform_create(self, validated_data):
        validated_data['username'] = self.generate_username(validated_data['first_name'], validated_data['last_name'])
        return super(UserManager, self).create_user(validated_data)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        username = self.generate_username(extra_fields['first_name'], extra_fields['last_name'])
        return super(UserManager, self).create_superuser(username, email, password, **extra_fields)

    def generate_username(self, first_name, last_name):
        username = first_name + '_' + last_name        # username is hard-coded to first+last names
        return username


class ProfileManager(QuerySet):
    #def get_queryset(self):
    #    return super(UserManager, self)._create_user(username, email, password, **extra_fields)


    #NO_PASSWORD = 'nohashedpassword'

    def _create_user(self, username, email, password, **extra_fields):
        return super(UserManager, self)._create_user(username, email, password, **extra_fields)

    def Xcheck_edit_permission(self, pk, target_user):
        try:
            user = self.get(pk=pk)
        except ObjectDoesNotExist:
            return False  # caller does not have 'permission' to access non-existent objects
        return user.can_edit(target_user)  # The user is allowed to update their own object or spouse/child objects

        #def create_user(self, first_name, last_name, email=None, password=None, **extra_fields):
    #    username = self._username_and_extras(first_name, last_name, email, password, extra_fields)
    #    return super(UserManager, self).create_user(username, email, password, **extra_fields)

    #def create_superuser(self, first_name, last_name, email=None, password=None, **extra_fields):
    #    username = self._username_and_extras(first_name, last_name, email, password, extra_fields)
    #    return super(UserManager, self).create_superuser(username, email, password, **extra_fields)
