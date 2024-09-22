from django.shortcuts import render
from user.models import Work

from django.db.models import Count


def explore(request):
    offset = int(request.GET.get('offset', 0))  # Get the offset (how many projects to skip)
    limit = 10  # Load 10 projects at a time

    # Get all works
    works = Work.objects.all()

    # Limit the works based on the offset and limit
    works = works[offset:offset + limit]

    # Calculate next offset
    next_offset = offset + limit

    # Get total projects count to check if more projects exist
    total_projects = Work.objects.count()

    return render(request, 'explore/explore.html', {
        'works': works,
        'next_offset': next_offset,
        'has_more': total_projects > next_offset
    })



# for sorting projects
def explore_projects(request):
    sort_option = request.GET.get('sort', 'newest')  # Default sorting
    offset = int(request.GET.get('offset', 0))  # Get the current offset
    limit = 10  # Number of projects to load

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

    # Apply offset and limit
    works = works[offset:offset + limit]

    # Calculate next offset
    next_offset = offset + limit

    # Get total projects count to check if more projects exist
    total_projects = Work.objects.count()

    # Determine if more projects are available
    has_more = total_projects > next_offset

    return render(request, 'explore/explore.html', {
        'works': works,
        'sort_option': sort_option,
        'next_offset': next_offset,  # Pass the next offset to the template
        'has_more': has_more  # Check if there are more projects to load
    })






