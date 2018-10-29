from collections import OrderedDict

from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers
import logging
logger = logging.getLogger(__name__)

from assignments.models import Duty
from .models import User, Family, Profile


''' Add JWT Token to Djoser's Serializer '''
class UserCreateSerializer(DjoserUserCreateSerializer):
    token = serializers.CharField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(many=False, read_only=True, source='profile')       # Make the id the profile-id, to be compatible with get-profile-detail
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True, source='id')          # Set user as the user-id, to be compatible with get-profile-detail
    verification_code = serializers.IntegerField(required=False)

    class Meta(DjoserUserCreateSerializer.Meta):
        fields = DjoserUserCreateSerializer.Meta.fields + ('token', 'id', 'user', 'verification_code')

class FatherFullnameFieldSerializer(serializers.Field):
    #father_full_name is unique since the value can be contained in object.father
    #father_full_name only has a value when the object.father is empty.
    #But when exposing self without exposing object.father (this happens when object is a son, so it includes son.father, but not son.father.father), then object.father.father_full_name should expose object.father.father.full_name
    def to_representation(self, object): # this would have the same as body as in a SerializerMethodField
        return object.get_father_name_title()[0]
    def to_internal_value(self, data):
        return {'father_full_name': data}

class ProfileSerializerBase(serializers.ModelSerializer):
    full_aliya_name = serializers.SerializerMethodField(source='get_full_aliya_name')
    father_full_name = FatherFullnameFieldSerializer(required=False, source='*')
    read_only = serializers.SerializerMethodField(read_only=True, source='get_read_only')
    display_name = serializers.SerializerMethodField(read_only=True, source='display_name')

    class Meta:
        model = Profile
        #fields = '__all__'
        exclude = 'gabbai_notes', '_display_name'
        #fields = 'full_aliya_name', 'father', 'user', 'first_name', 'last_name', 'display_name', 'duties', 'default_family_to_add_children', 'full_name', 'title', 'parents', 'dod_day', 'dod_month', 'gender', 'bar_mitzvahed', 'dob', 'bar_mitzvah_parasha'

        #extra_kwargs = {'password': {'write_only': True}, 'first_name': {'required': False}, 'last_name': {'required': False}, 'display_name': {'required': False}, 'parents': {'required': False}, 'father': {'required': False}}
        #extra_kwargs = {'full_aliya_name': {'required': True}}
        extra_kwargs = {'display_name': {'required': False}}

    def get_full_aliya_name(self, object):
        try:
            return object.get_full_aliya_name()
        except Exception as e:
            logger.error('Error: %s', e)

    def get_read_only(self, object):
        if hasattr(self, "context"):
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                # the logic below is a subset of object.has_permission, but serializer can be called before child/spouse/parent family is created which makes that call fail
                return object!=request.user.profile and object.profile_role == Profile.PROFILE_ROLE_INDEPENDENT
        logger.error('Error: missing context forget_read_only')
        return True

    def get_display_name(self, object):
        return object.display_name_with_family

    def get_parents(self, object):
        return object.parents

    # filter the null (and empty) values and creates a new dictionary
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # https://stackoverflow.com/questions/27015931/remove-null-fields-from-django-rest-framework-response
        return OrderedDict(list(filter(lambda x: x[1], ret.items())))

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        internal_value["kwargs_from_view"] = data.get('kwargs_from_view')
        return internal_value

class SpouseProfileSerializer(ProfileSerializerBase):
    #father = ProfileSerializerBase(allow_null=True, required=False)
    #mother = ProfileSerializerBase(allow_null=True, required=False)
    parents = ProfileSerializerBase(many=True, allow_null=True, required=False, read_only=True)

    def create(self, validated_data):
        logger.error('create spouse: %s', validated_data)

    def update(self, instance, validated_data):
        logger.error('updating spouse: %s', validated_data)


class ParentProfileSerializer(ProfileSerializerBase):
    class Meta(ProfileSerializerBase.Meta):
        exclude = ProfileSerializerBase.Meta.exclude + ('first_name', 'last_name')


class ProfileSerializer(ProfileSerializerBase):
    parents = ProfileSerializerBase(many=True, allow_null=True, required=False, read_only=True)
    spouse = SpouseProfileSerializer(allow_null=True, required=False, read_only=True)
    children = ProfileSerializerBase(many=True, required=False, read_only=True)
    father_full_name = None

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'
        #exclude = ('user_permissions', )
        #extra_kwargs = {'password': {'write_only': True}}

