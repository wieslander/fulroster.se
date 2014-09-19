import collections
import csv
import StringIO

import requests
from django.core.management.base import BaseCommand, CommandError

from parties.models import Party, VoteEntry

ELECTION_RESULTS_URL = 'http://www.val.se/val/val2014/handskrivna/handskrivna.skv'

CSV_FIELDS = ('election_type county county_name municipality municipality_name '
              'circle circle_name district district_name party_name vote_count')

VoteEntryRow = collections.namedtuple('VoteEntryRow', CSV_FIELDS)

class Command(BaseCommand):
    args = ''
    help = 'Imports hand-written votes from val.se'

    def handle(self, *args, **options):
        csv_text = requests.get(ELECTION_RESULTS_URL).text.encode('utf-8')
        csv_buffer = StringIO.StringIO(csv_text)
        dialect = csv.Sniffer().sniff(csv_text)
        reader = csv.reader(csv_buffer, dialect)

        # Ignore header
        reader.next()

        for row in reader:
            row[-1] = int(row[-1])
            row = VoteEntryRow(*row)
            VoteEntry.import_csv_row(row)

        # Update total vote count
        for party in Party.objects.all():
            party.total_votes = party.get_total_votes()
            party.save()
