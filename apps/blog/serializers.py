from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPostModel, CategoryModel, TagModel, ReviewModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        password = validated_data.get("password")
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostModel
        fields = "__all__"


class ReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = "__all__"


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = "__all__"


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        dict_data = dict()
        for i in CategoryModel.objects.all():
            posts_count = BlogPostModel.objects.filter(category_id=i.id).count()
            dict_data[f"{i.category_name}"] = f"{posts_count}"
        representation["Categories count"] = dict_data
        return representation


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostModel
        fields = ['author', 'category', 'title', 'date_time', 'view_count', 'hashtag', 'image', 'video', 'text']