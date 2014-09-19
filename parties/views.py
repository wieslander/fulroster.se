from difflib import get_close_matches
import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from parties.models import Party

def entries(request):
    parties = Party.objects.all()
    context = {'parties': parties}
    return render(request, 'parties/entries.html', context)

def show(request, id, slug):
    party = get_object_or_404(Party, pk=id)
    party.views += 1
    party.save()
    
    parties_by_name = {p.name: p for p in  Party.objects.all()
                       if p.pk != party.pk}
    similar_names = get_close_matches(party.name, parties_by_name.keys(),
                                      n=10, cutoff=0.6)
    similar_parties = [parties_by_name[name] for name in similar_names]
    context = {'party': party,
               'stats': party.stats(),
               'similar_parties': similar_parties}
    return render(request, 'parties/show.html', context)
