from django.db import models
from parashot.managers import ParashaManager


class Parasha(models.Model):
    objects = ParashaManager()
    """
    List of parashot
    """
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk']
        verbose_name_plural = 'Parashot'


class Segment(models.Model):
    """
    List of parasha segments (aliyot)
    """
    SEGMENT_RISHON = 1
    SEGMENT_SHENI = 2
    SEGMENT_SHLISHI = 3
    SEGMENT_RVII = 4
    SEGMENT_HAMISHI = 5
    SEGMENT_SHISHI = 6
    SEGMENT_SHVII = 7
    SEGMENT_HAFTORAH = 8
    SEGMENT_TYPES = (
        (SEGMENT_RISHON, 'ראשון'),
        (SEGMENT_SHENI, 'שני'),
        (SEGMENT_SHLISHI, 'שלישי'),
        (SEGMENT_RVII, 'רביעי'),
        (SEGMENT_HAMISHI, 'חמישי'),
        (SEGMENT_SHISHI, 'שישי'),
        (SEGMENT_SHVII, 'שביעי'),
        (SEGMENT_HAFTORAH, 'הפטרה'),
    )
    parasha = models.ForeignKey(Parasha, related_name='segments')
    segment_type = models.IntegerField(choices=SEGMENT_TYPES)
    start_pos = models.CharField(max_length=6)
    end_pos = models.CharField(max_length=6)
    total_psukim = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return "%s/%s (#%s)" % (self.parasha.name, self.segment_type, self.id)
