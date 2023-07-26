from bs4 import BeautifulSoup
import math
from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from .managers import (
    BlogPostManager,
    ReviewManager,
    CategoryManager,
    PageVisitManager,
    ViewCountManager, AuthorManager
)


class RequiredFields(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    email = models.EmailField()
    phone_number = PhoneField(blank=True, help_text="Contact phone number")

    class Meta:
        abstract = True


class Tag(models.Model):
    tag_name = models.TextField()

    def __str__(self):
        return self.tag_name


class Category(models.Model):
    category_name = models.CharField(max_length=100, blank=False)
    photo_of_category = models.ImageField(upload_to="images_of_categories", blank=False)
    objects = CategoryManager()

    def __str__(self):
        return self.category_name


class SocialMedia(models.Model):
    link = models.CharField(max_length=1000)
    photo_of_link = models.ImageField(upload_to="image_of_link", blank=False)
    social_media_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.social_media_name


class AuthorOccupation(models.Model):
    job_title = models.CharField(max_length=12)

    def __str__(self):
        return self.job_title


class Author(models.Model):
    name = models.TextField(default="Annonymous User")
    Address = models.CharField(max_length=300, blank=True, null=True)
    social_media_links = models.ManyToManyField(SocialMedia)
    occupation = models.ManyToManyField(AuthorOccupation)
    objects = AuthorManager()

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=False)
    created = models.DateField(auto_now=True)
    hashtag = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to="images_of_author_posts", blank=True)
    video = models.FileField(upload_to="videos_of_author_posts", blank=True)
    text = RichTextField(blank=True, null=False)
    objects = BlogPostManager()

    def __str__(self):
        return self.title

    @property
    def read_time(self):
        words_per_minute = 200
        soup = BeautifulSoup(self.text, "lxml")
        words = soup.get_text().split()
        word_count = len(words)
        read_time_in_minutes = math.ceil(word_count / words_per_minute)

        return f"{read_time_in_minutes} minutes"


class Comment(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    post_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.name


class Review(models.Model):
    review_score = models.IntegerField()
    post_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    objects = ReviewManager()

    def __str__(self):
        return self.post_id.title


class PageVisit(models.Model):
    device_id = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = PageVisitManager()

    def __str__(self):
        return f"{self.device_id}"


class ViewCount(models.Model):
    blog_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    objects = ViewCountManager()


class Contact(RequiredFields):
    name = models.CharField(max_length=40, default="Anonymous")
    email = models.EmailField()
    subject = models.CharField(max_length=400, blank=False, null=False)
    text = models.TextField()


    def __str__(self):
        return self.name


