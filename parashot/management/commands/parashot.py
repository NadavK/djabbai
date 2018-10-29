from django.core.management.base import BaseCommand, CommandError

from common.jewish_dates.parasha import getTorahSections
#from ...models import Parasha, Segment

class Command(BaseCommand):
    help = 'Creates Parashot for the specified year'

    def add_arguments(self, parser):
        parser.add_argument('hebrewYear', nargs=1, type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--diaspora',
            action='store_true',
            dest='diaspora',
            default=False,
            help='Set to True for diaspora',
        )

    def handle(self, *args, **options):
        for month in range(1, 8):
            for day in range(1, 30):
                self.stdout.write('%s/%s (day/month): %s' % (day, month, getTorahSections(month, day, options['hebrewYear'][0], options['diaspora'])))

        return
        for poll_id in options['poll_id']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
