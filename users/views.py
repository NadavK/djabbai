from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from djoser.views import UserCreateView
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import detail_route, api_view, throttle_classes, permission_classes
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework_jwt.settings import api_settings
import logging
logger = logging.getLogger(__name__)

from .models import Family, Profile
from .serializers import ProfileSerializer, FamilySerializer, UserCreateSerializer, ParentProfileSerializer


class CheckUserThrottle(UserRateThrottle):
    rate = '15/hour'


@api_view(['GET'])
@throttle_classes([CheckUserThrottle])
@permission_classes([AllowAny])
def check_user(request, first_name, last_name, verification_code=None):
    """
    Returns details needed for sign-up: does user exist? are they verified? who are the parents/spouse?
    """
    logger.error('CHECK %s %s %s', first_name, last_name, verification_code)
    try:
        profile = Profile.objects.get(first_name__iexact=first_name, last_name__iexact=last_name)    # Does a profile exist without a user?
    except Profile.DoesNotExist:
        logger.debug('No profile')
        return Response({'exists': False})

    if profile.profile_role==Profile.PROFILE_ROLE_INDEPENDENT:
        return Response({'exists': True, 'verified': True})

    # if not user.default_family_to_add_children:
    #     raise ViewDoesNotExist({"message": "This user is not verified, and does not have a default_family"})

    try:
        family = Family.objects.get(parents__pk=profile.pk)             # First check if user is a parent
        relation = 'spouse'
    except Family.DoesNotExist:
        try:
            family = Family.objects.get(children__pk=profile.pk)        # If not a parent, maybe a child?
            relation = 'child'
        except Family.DoesNotExist:
            # print('No family 1', Family.objects.all().count())
            # for family in Family.objects.all():
            #     print("'" + family.display_name() + "'")
            #     for parent in family.parents:
            #         print("'\t" + parent + "'")

            raise Http404

    verification_code_bool = (str(profile.verification_code) == str(verification_code))

    data = {'exists': True, 'family': family.display_name(), 'verified': False, 'relation': relation, 'verification_code': verification_code_bool}


    #if not user.default_family_to_add_children:
    #    raise ViewDoesNotExist({"message": "This user is not verified, and does not have a default_family"})
    #
    #data = {'family': user.default_family_to_add_children.display_name(), 'verified': False}


    return Response(data)

@api_view(['GET'])
@throttle_classes([CheckUserThrottle])
@permission_classes([AllowAny])
def check_verification_code(request, verification_code):
    """
    Returns details needed for sign-up: does user exist? are they verified? who are the parents/spouse?
    """
    logger.error('CHECK VERIFICATION CODE: %s', verification_code)
    try:
        profile = Profile.objects.get(verification_code__iexact=verification_code)
    except Profile.DoesNotExist:
        logger.debug('No profile for this verification_code')
        return Response({'exists': False, 'verification_code': False})

    if profile.profile_role==Profile.PROFILE_ROLE_INDEPENDENT:  # Independent users should sign-up with their password
        return Response({'exists': True, 'verification_code': False})       # This should not happen, since the verification_code should have been  cleared

    data = {'exists': True, 'first_name': profile.first_name, 'last_name': profile.last_name, 'full_name': profile.full_name, 'verified': False, 'verification_code': True}


    #if not user.default_family_to_add_children:
    #    raise ViewDoesNotExist({"message": "This user is not verified, and does not have a default_family"})
    #
    #data = {'family': user.default_family_to_add_children.display_name(), 'verified': False}


    return Response(data)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_profile(request):
    try:
        serializer = ProfileSerializer(request.user.profile, context={'request': request})
        return Response(status=200, data=serializer.data)
    except Exception as e:
        logger.error('Error: %s', e)
        raise Http404


class ProfileUpdatePermission(BasePermission):
    pk_name = 'pk'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:       # Anon cannot do anything
            return False

        #Other permissions are checked in get_queryset and specific retrieve in has_object_permission()
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:               # Superuser is g-d
            return True
        return obj.has_permission(request.user.profile)    # The user is allowed to update their own object or child-owned objects


class ThrottleMixin():
    # http://www.pedaldrivenprogramming.com/2017/05/throttling-django-rest-framwork-viewsets/
    def get_throttles(self):
        if self.request.method in ['POST']:
            self.throttle_scope = 'create'
        return super().get_throttles()


class MyUserCreateView(ThrottleMixin, UserCreateView):
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        #if request.data.get('verification_code'):
        #    print('REQUEST: ', request.data.get('verification_code'))
        #    args = request.data.get('verification_code')
        #    print('REQUEST: ', args)
        response = super().post(request, *args, **kwargs)
        if response.status_code != status.HTTP_201_CREATED:
            return response

        #Add the token to the response
        user = authenticate(username=response.data['username'], password=request.data['password'])
        if not user:
            logger.error('Registered new user but username or password incorrect: %s %s [%s]', response.data['first_name'], response.data['last_name'], response.data['username'])
            return response
        user.token = api_settings.JWT_ENCODE_HANDLER(api_settings.JWT_PAYLOAD_HANDLER(user))

        # Serialize
        response.data = UserCreateSerializer(user).data
        return response


class ProfileViewSet(ThrottleMixin, viewsets.ModelViewSet):
    """
    Manage profiles
    """
    queryset = Profile.objects.all().order_by('display_name')
    serializer_class = ProfileSerializer
    permission_classes = (ProfileUpdatePermission,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Profile.objects.all()

        return Profile.objects.filter(pk__in=self.request.user.profile.authorized_pks(write_permission=(self.request.method not in SAFE_METHODS)))

    def create(self, request, *args, **kwargs):
        # Use /api/v1/auth/register/
        raise MethodNotAllowed('POST', 'Create a new profile by creating a new user, or by adding a spouse or child')

    @detail_route(methods=['get'], url_name='spouseXX', url_path='spouseXX')
    def XXXspouse_get(self, request, pk=None):
        """
        Returns this user's spouse
        :param request:
        :param pk:
        :return:
        """
        try:
            family = self.queryset.get(pk=pk).default_family_to_add_children
            if not family:
                raise Http404
            spouses = family.parents.exclude(pk=pk)
            if not spouses:
                raise Http404
            serializer = self.serializer_class(spouses[0], many=False, context={'request': request})      #pick arbitrary first spouse. Why would there be more than one?
            return Response(serializer.data)
        except Family.DoesNotExist:
            raise Http404
        except Profile.DoesNotExist:
            raise Http404


class RelatedProfileUpdatePermission(ProfileUpdatePermission):
    pk_name = 'profile_pk'


class RelatedProfileViewSet(ProfileViewSet):
    permission_classes = (RelatedProfileUpdatePermission,)

    def get_queryset(self):
        parent_id = self.kwargs.get('profile_pk')
        nested_id = self.kwargs.get('pk')

        if nested_id:
            #Does logged-in user have permission for nested profile? (oo we need to check if parent has permission for nested profile? )
            nested = Profile.objects.get(pk=nested_id)
            if not self.request.user.is_superuser:
                if not nested.has_permission(self.request.user.profile, write_permission=(self.request.method not in SAFE_METHODS)):
                    return None
            return Profile.objects.filter(pk=nested_id)             # we don't filter on profile_pk, because the permission class will already check
        elif parent_id:
            #print('Parent:', parent_id, Profile.objects.get(pk=parent_id).display_name)
            return Profile.objects.filter(pk=parent_id)             # This request is for a list
        else:
            return None

    def get_throttles(self):
        if self.action in ['delete', 'validate']:
            self.throttle_user = 'foo.' + self.action
        return super().get_throttles()

    #@throttle_classes([CreateUserThrottle])
    # ProfileViewSet prevents creating new profiles, so call the grandfather class
    def create(self, request, profile_pk=None, *args, **kwargs):
        return super(ProfileViewSet, self).create(request, profile_pk, *args, **kwargs)

class SpouseProfileViewSet(RelatedProfileViewSet):
    """
    retrieve:
    Returns user's spouse per spouse_pk for the default family

    list:
    List arbitrary first spouse of default family (why would there be more than one?)

    create:
    Create a new spouse for this user

    update:
    Creating a user's spouse association - only allowed by superuser

    update/partial:
    Update a user's spouse

    delete:
    Delete a user's spouse association (not tested)
    """

    def list(self, request, profile_pk=None):
        family = self.queryset.get(pk=profile_pk).default_family_to_add_children
        if not family:
            raise Http404
        serializer = self.serializer_class(family.parents.exclude(pk=profile_pk), many=True, context={'request': request})  # TODO: consider returning spouse from all families, but limit editing to default family
        #serializer = self.serializer_class(self._get_spouse(profile_pk)[0], many=False)  # pick arbitrary first spouse. Why would there be more than one?
        return Response(serializer.data)

    def Xretrieve(self, request, profile_pk=None, pk=None):
        serializer = self.serializer_class(self._get_spouse(profile_pk, pk), many=False, context={'request': request})  # pick arbitrary first spouse. Why would there be more than one?
        return Response(serializer.data)

    #@throttle_classes([CreateUserThrottle])
    def create(self, request, profile_pk=None, *args, **kwargs):
        """
        Create a new user, and associate the new user as a spouse to the specified-user, creating a Family if none exists
        If specified-user is 0, uses the request-user
        :param request:
        :param user_pk:
        :return:
        """
        #print(profile_pk, request.user.pk, kwargs)
        #if not profile_pk:
        #    profile_pk = request.user.pk

        try:
            self.lookup_url_kwarg = 'profile_pk'
            profile = self.get_object()                                     # This calls has_object_permission
            if profile.spouse:
                raise serializers.ValidationError('Profile already has spouse')
        except Profile.DoesNotExist:
            raise serializers.ValidationError('Profile not found')
        try:
            self.request.data['display_name'] = self.request.data.get('first_name') + '_' + self.request.data.get('last_name')
        except:
            pass
        request.data['kwargs_from_view'] = {'spouse_of': profile}
        return super().create(request, profile_pk, *args, **kwargs)     # Create a profile for the spouse

    def update(self, request, profile_pk=None, pk=None, *args, **kwargs):
        """
        Associates a spouse to specified user, creating a Family if none exists
        :param request:
        :param profile_pk: the profile that the spouse should be associated with
        :param pk:  the spouse to associate with user_pk
        :return:
        """
        if kwargs.get('partial') == True:               # This is a PATCH request to update an existing spouse
            return super().update(request, profile_pk, pk, *args, **kwargs)
            #serializer = self.serializer_class(self._get_spouse(profile_pk)[pk], many=False)  # pick arbitrary first spouse. Why would there be more than one?
            #return Response(serializer.data)

        # Associate existing profile as spouse
        try:
            if not request.user.is_superuser:
                raise PermissionDenied({"message": "You don't have permission to associate existing users"})
            profile = self.queryset.get(pk=profile_pk)
            spouse = self.queryset.get(pk=pk)
            profile.set_family(spouse=spouse)                           # Associate profile with specified-profile as spouse
            return Response(status=status.HTTP_201_CREATED)
        except Profile.DoesNotExist:
            raise Http404


#class ChildProfileUpdatePermission(ProfileUpdatePermission):
#    pk_name = 'user_pk'


class ChildProfileViewSet(RelatedProfileViewSet):
    """
    retrieve:
    Returns user's child

    list:
    List all user's children

    create:
    Create a new child for this user

    update:
    Update a user's child - NOT ALLOWED. or allowed by admin?
    or is this creating a user's child association?

    delete:
    Delete a user's child association
    """
    #queryset = User.objects.all()  # .order_by('dayt')
    #serializer_class = ProfileSerializer

    # update_serializer_class = FamilyUpdateSerializer

    #def XXXget_permissions(self):
    #    if self.request.method in ['POST', 'PUT', 'PATCH']:
    #        self.permission_classes = [ChildProfileUpdatePermission, ]
    #    return super(ChildProfileViewSet, self).get_permissions()

    def _get_child(self, user_pk=None, child_pk=None):
        """
        Returns single child for child_pk, or list of children if None
        :param user_pk:
        :param child_pk:
        :return:
        """

        logger.debug('_get_child: %s/%s', user_pk, child_pk)

        try:
            children = []
            if child_pk:
                family = Family.objects.get(parents__pk=user_pk, children__pk=child_pk)
                return Profile.objects.get(pk=child_pk)       # once we ensured that the parent and child are of the same family, we can return the child
            else:
                families = Family.objects.filter(parents__pk=user_pk)
                from itertools import chain
                for family in families:
                    #print('Children: ', family.children.all())
                    children = family.children.all()          # TODO: Need to add children from all families
                    #children = list(children) + list(family.children.all())          # Need to add children from all families
            #children = Family.objects.filter(parents__pk=user_pk, children__pk=child_pk)
        except ObjectDoesNotExist:
            logger.error('_get_child returning 404')
            raise Http404
        #print('_get_child returning: ', children)
        return children

    def list(self, request, profile_pk=None):
        serializer = self.serializer_class(self._get_child(profile_pk), many=True, context={'request': request})
        return Response(serializer.data)

    def Xretrieve(self, request, profile_pk=None, pk=None):
        serializer = self.serializer_class(self._get_child(profile_pk, pk), many=False, context={'request': request})
        return Response(serializer.data)

    #@throttle_classes([CreateUserThrottle])
    def create(self, request, profile_pk=None, *args, **kwargs):
        """
        Create a new user, and associate the new user as a child to the specified-user, creating a Family if none exists
        If specified-user is 0, uses the request-user
        :param request:
        :param user_pk:
        :return:
        """
        #print(profile_pk, request.user.pk, kwargs)
        #if not profile_pk:
        #    profile_pk = request.user.pk

        try:
            self.lookup_url_kwarg = 'profile_pk'
            profile = self.get_object()                                     # This calls has_object_permission
        except Profile.DoesNotExist:
            raise serializers.ValidationError('Profile not found')
        try:
            self.request.data['display_name'] = self.request.data.get('first_name') + '_' + self.request.data.get('last_name')
        except:
            pass
        request.data['kwargs_from_view'] = {'child_of': profile}
        return super().create(request, profile_pk, *args, **kwargs)     # Create a profile for the child

    @detail_route(methods=['post'])
    def associate(self, request, user_pk=None, pk=None):
        """
        Associates a child to specified user, creating a Family if none exists
        :param request:
        :param user_pk:  the user that the child should be associated with
        :param pk:  the child to associate with user_pk
        :return:
        """

        logger.debug('***********************CREATE ASSOCIATION, user_pk, pk')

        if not request.user.is_superuser:
                raise PermissionDenied({"message": "You don't have permission to associate existing users"})
        user = self.queryset.get(pk=user_pk)
        child = self.queryset.get(pk=pk)
        if not user.default_family_to_add_children:
            user.default_family_to_add_children = Family.objects.create()
            user.default_family_to_add_children.parents.add(user)
        user.default_family_to_add_children.children.add(child)
        user.save()
        return Response(status=status.HTTP_201_CREATED)


class ParentProfileViewSet(RelatedProfileViewSet):
    """
    retrieve:
    Returns user's child

    list:
    List all user's children

    create:
    Create a new child for this user

    update:
    Update a user's child - NOT ALLOWED. or allowed by admin?
    or is this creating a user's child association?

    delete:
    Delete a user's child association
    """
    #queryset = User.objects.all()  # .order_by('dayt')
    #serializer_class = ProfileSerializer

    # update_serializer_class = FamilyUpdateSerializer
    serializer_class = ParentProfileSerializer

    def _get_parent(self, user_pk=None, parent_pk=None):
        """
        Returns single child for child_pk, or list of children if None
        :param user_pk:
        :param child_pk:
        :return:
        """

        logger.debug('_get_parent: %s/%s', user_pk, parent_pk)

        if parent_pk:
            try:
                return Profile.objects.get(pk=user_pk, father=parent_pk)
            except Profile.DoesNotExist:
                pass
            try:
                return Profile.objects.get(pk=user_pk, mother=parent_pk)
            except Profile.DoesNotExist:
                logger.error('_get_parent returning 404')
                raise Http404
        else:
            try:
                profile = Profile.objects.get(pk=user_pk)
                return [profile.father, profile.mother]
            except Profile.DoesNotExist:
                pass

    def list(self, request, profile_pk=None):
        serializer = self.serializer_class(self._get_parent(profile_pk), many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, profile_pk=None, *args, **kwargs):
        """
        Create a new user, and associate the new user as a child to the specified-user, creating a Family if none exists
        If specified-user is 0, uses the request-user
        :param request:
        :param user_pk:
        :return:
        """
        #print(profile_pk, request.user.pk, kwargs)
        #if not profile_pk:
        #    profile_pk = request.user.pk

        try:
            self.lookup_url_kwarg = 'profile_pk'
            profile = self.get_object()                                     # This calls has_object_permission
            #if profile.spouse:
            #    raise serializers.ValidationError('Profile already has father/mother')
        except Profile.DoesNotExist:
            raise serializers.ValidationError('Profile not found')
        try:
            self.request.data['display_name'] = self.request.data.get('first_name') + '_' + self.request.data.get('last_name')
        except:
            pass
        request.data['kwargs_from_view'] = {'child': profile}
        return super().create(request, profile_pk, *args, **kwargs)     # Create a profile for the parent
        #profile.parents.add(new_profile)


class FamilyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows assignments to be viewed or edited.
    """
    queryset = Family.objects.all()  # .order_by('dayt')
    serializer_class = FamilySerializer
    #update_serializer_class = FamilyUpdateSerializer

    #def get_permissions(self):
    #    if self.request.method == 'PUT':
    #        self.permission_classes = [FamilyUpdatePermission, ]
    #    return super(FamilyViewSet, self).get_permissions()

    def list(self, request, user_pk=None):
        queryset = self.queryset.filter(parents__id=user_pk)
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, user_pk=None):
        try:
            family = self.queryset.get(pk=pk, parents__id=user_pk)
            serializer = self.serializer_class(family, many=False, context={'request': request})
            return Response(serializer.data)
        except Family.DoesNotExist:
            raise Http404

    def create(self, request, pk=None, user_pk=None):
        request.data['user'] = user_pk
        return super(FamilyViewSet, self).create(request)

    def update(self, request, pk=None, user_pk=None):
        request.data['user'] = user_pk
        return super(FamilyViewSet, self).update(request)

