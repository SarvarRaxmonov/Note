from django_filters import FilterSet
from .models import BlogPost


class BlogPostFilter(FilterSet):
    class Meta:
        model = BlogPost
        fields = {
            "category__id": ["exact"],
        }
