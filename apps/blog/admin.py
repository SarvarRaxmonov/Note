from django.contrib import admin
from .models import (
    Author,
    Tag,
    Category,
    SocialMedia,
    AuthorOccupation,
    BlogPost,
    Comment,
    Review,
    Contact,
    ViewCount
)


admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(SocialMedia)
admin.site.register(AuthorOccupation)
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Contact)
admin.site.register(ViewCount)

