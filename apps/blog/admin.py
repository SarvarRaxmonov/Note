from django.contrib import admin
from .models import (
    AuthorModel,
    TagModel,
    CategoryModel,
    SocialMediaModel,
    AuthorOccupationModel,
    BlogPostModel,
    CommentModel,
    ReviewModel,
    ContactModel,
)


admin.site.register(AuthorModel)
admin.site.register(TagModel)
admin.site.register(CategoryModel)
admin.site.register(SocialMediaModel)
admin.site.register(AuthorOccupationModel)
admin.site.register(BlogPostModel)
admin.site.register(CommentModel)
admin.site.register(ReviewModel)
admin.site.register(ContactModel)
