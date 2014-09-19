# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

from parties.models import Party


def index(request):
    popular_parties = Party.most_popular(10)
    context = {'popular_parties': popular_parties}
    return render(request, 'fulroster/index.html', context)
