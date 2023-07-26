from django.db import models
from django.utils import timezone
from django.db.models import Count

class BlogPostManager(models.Manager):
    def top_reviewed_posts(self, num_posts=2):
        return self.all().order_by("-review_score")[:num_posts]

    def new_posts_on_current_date(self):
        date = timezone.now().date()
        return self.filter(
            created__year=date.year,
            created__month=date.month,
            created__day=date.day,
        ).count()


class ReviewManager(models.Manager):
    def most_targeted_posts(self, num_posts=2):
        return self.all().order_by("-review_score")[:num_posts]


class CategoryManager(models.Manager):
    def get_category_post_counts(self):
        dict_data = dict()
        for category in self.all():
            posts_count = category.blogpost_set.count()
            dict_data[category.category_name] = posts_count
        return dict_data


class PageVisitManager(models.Manager):
    def get_today_visits_count(self):
        current_date = timezone.now().date()
        today_visits_count = self.filter(timestamp__date=current_date).count()
        return today_visits_count


class ViewCountManager(models.Manager):
    def get_today_read_count(self):
        current_date = timezone.now().date()
        today_visits_count = self.filter(timestamp__date=current_date).count()
        return today_visits_count


class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(total_views=Count('blogpost__viewcount')).order_by('-total_views')

    def get_authors_with_highest_views(self):
        return self.get_queryset()[:3]


