# pages/views.py
from rest_framework import viewsets
from .models import Page, Course
from .serializers import PageSerializer, CourseSerializer, CourseDetailSerializer

class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing pages.
    Provides `list` and `retrieve` actions.
    """
    # Use prefetch_related to optimize the query by fetching all related
    # content_pages in a single additional query.
    queryset = Page.objects.prefetch_related('content_pages').all().order_by('created_at')
    serializer_class = PageSerializer
    lookup_field = 'slug' # Use slug instead of ID for retrieving a single page

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving Courses.
    - `list` action provides a summary of courses.
    - `retrieve` action provides full details including modules, topics, etc.
    """
    # This is a highly optimized query to fetch all related data at once.
    queryset = Course.objects.prefetch_related(
        'modules__topics__content_items'
    ).all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer
