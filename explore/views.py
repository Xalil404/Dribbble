from django.shortcuts import render
from user.models import Work

def explore(request):
    works = Work.objects.all()
    return render(request, 'explore/explore.html', {'works': works})
