from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Parasha, Segment
from .serializers import ParashaSerializer, SegmentSerializer


class ParashaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows parashas to be viewed or edited.
    """
    queryset = Parasha.objects.all() #.order_by('dayt')
    serializer_class = ParashaSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class SegmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows parasha-segments to be viewed or edited.
    """
    queryset = Segment.objects.all() #.order_by('pk')
    serializer_class = SegmentSerializer
