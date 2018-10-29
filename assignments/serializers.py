from parashot.serializers import ParashaSerializer
from rest_framework import serializers
from .models import Duty, Shabbat, Assignment, Roster


class DutySerializer(serializers.ModelSerializer):
    class Meta:
        model = Duty
        fields = '__all__'
        #fields = ('name',)


class DutyShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duty
        fields = ('pk', 'url', 'category', 'name')


class AssignmentSerializer(serializers.ModelSerializer):
    #shabbat_id = serializers.ReadOnlyField(source='shabbat.id')
    #shabbat_parasha = serializers.ReadOnlyField(source='shabbat.parasha.name')
    #duty = DutySerializer()
    #duty = serializers.ReadOnlyField(source='shabbat.id')
    #duty_name = serializers.ReadOnlyField(source='duty.name')

    class Meta:
        model = Assignment
        #fields = '__all__'
        exclude = ('roster', )
        #fields = ('pk')


class AssignmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class RosterSerializer(serializers.ModelSerializer):
    duty = DutyShortSerializer()
    assignments = AssignmentSerializer(many=True)

    class Meta:
        model = Roster
        exclude = ('shabbat', 'profiles')


class RosterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roster
        fields = '__all__'


class ShabbatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shabbat
        fields = '__all__'


class ShabbatSerializer(serializers.ModelSerializer):
    #duties = DutySerializer(many=True, read_only=True)
    parasha = ParashaSerializer()
    roster = RosterSerializer(source='roster_set', many=True)
    date = serializers.DateField(source='dayt')

    class Meta:
        model = Shabbat
        fields = '__all__'
        fields = ('url', 'parasha', 'date', 'roster')

