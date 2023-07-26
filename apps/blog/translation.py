from .models import BlogPost
from modeltranslation.translator import TranslationOptions, translator


class BlogPostTranslationOptions(TranslationOptions):
    fields = ("title",)


translator.register(BlogPost, BlogPostTranslationOptions)
