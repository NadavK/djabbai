from rest_framework import serializers
from .models import Parasha, Segment


class ParashaSerializer(serializers.ModelSerializer):
    #readings2 = ShabbatToTorahSegmentSerializer(many=True, read_only=True)
    class Meta:
        model = Parasha
        fields = '__all__'
        #fields = ('dayt', 'readings', 'readings2')


class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = '__all__'
        #fields = ('start_pos', 'end_pos', 'total_psukim')
