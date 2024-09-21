from django.shortcuts import render
from user.models import Work

from django.db.models import Count

def explore(request):
    works = Work.objects.all()
    return render(request, 'explore/explore.html', {'works': works})


# for sorting projects
def explore_projects(request):
    sort_option = request.GET.get('sort', 'newest')  # Default sorting

    if sort_option == 'most_liked':
        works = Work.objects.annotate(like_count=Count('liked_works')).order_by('-like_count')
    elif sort_option == 'least_liked':
        works = Work.objects.annotate(like_count=Count('liked_works')).order_by('like_count')
    elif sort_option == 'most_viewed':
        works = Work.objects.annotate(view_count=Count('project_views')).order_by('-view_count')
    elif sort_option == 'least_viewed':
        works = Work.objects.annotate(view_count=Count('project_views')).order_by('view_count')
    elif sort_option == 'oldest':
        works = Work.objects.order_by('created_at')
    else:  # Default to newest
        works = Work.objects.order_by('-created_at')

    return render(request, 'explore/explore.html', {'works': works})


