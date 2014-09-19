import collections

from autoslug.fields import AutoSlugField
from django.db import models

from parties.realparties import is_registered_party

ELECTION_TYPES = [
    ('R', 'Riksdag'),
    ('L', 'Landsting'),
    ('K', 'Kommun')
]

class Party(models.Model):
    # Denormalize total votes for performance reasons.
    # It's the responsibility of the importvotes management
    # command to keep the total vote count up to date.
    total_votes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    name = models.TextField(unique=True)
    slug = AutoSlugField(populate_from='name', blank=True)

    class Meta:
        ordering = ['-views', 'total_votes', 'slug']

    @staticmethod
    def most_popular(max_results=None):
        parties = Party.objects.all()
        if max_results:
            return parties[:max_results]
        else:
            return parties

    def stats(self):
        if not hasattr(self, '_stats'):
            votes_by_type = collections.Counter()
            votes_by_municipality = collections.Counter()
            self._stats = {
                'total_votes': self.total_votes,
                'votes_by_type': votes_by_type,
            }

            for entry in self.vote_entries.all():
                votes_by_type[entry.election_type] += entry.vote_count
                municipality_name = entry.election_district.municipality.name
                votes_by_municipality[municipality_name] += entry.vote_count

            self._stats['votes_by_municipality'] = votes_by_municipality.most_common()
        return self._stats

    def get_total_votes(self):
        vote_entries = self.vote_entries.all()
        return sum(e.vote_count for e in vote_entries)

    def votes_by_election_type(self):
        vote_entries = self.vote_entries.all()
        votes_by_type = collections.Counter()

        for entry in vote_entries:
            votes_by_type[entry.election_type] += entry.vote_count

        return votes_by_type

class County(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')

class Municipality(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')
    county = models.ForeignKey(County)

class ElectionDistrict(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    municipality = models.ForeignKey(Municipality)

class VoteEntry(models.Model):
    election_type = models.CharField(max_length=1, choices=ELECTION_TYPES)
    party = models.ForeignKey(Party, related_name='vote_entries')
    election_district = models.ForeignKey(ElectionDistrict)
    vote_count = models.IntegerField()

    @staticmethod
    def import_csv_row(row):
        if is_registered_party(row.party_name):
            return
        party, _ = Party.objects.get_or_create(name=row.party_name)
        county, _ = County.objects.get_or_create(name=row.county_name)
        municipality, _ = Municipality.objects.get_or_create(name=row.municipality_name,
                                                             county=county)
        district, _ = ElectionDistrict.objects.get_or_create(name=row.district_name,
                                                             municipality=municipality)
        entry, _ = VoteEntry.objects.get_or_create(election_type=row.election_type,
                                                   party=party, election_district=district,
                                                   defaults={'vote_count': int(row.vote_count)})

        if row.vote_count != entry.vote_count:
            entry.vote_count = row.vote_count
            entry.save()
