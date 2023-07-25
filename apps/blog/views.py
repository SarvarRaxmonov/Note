from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework import viewsets
from .models import BlogPostModel, ReviewModel, CategoryModel
from .serializers import BlogPostSerializer, ReviewModelSerializer, CategoryModelSerializer, TagModelSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPostModel.objects.all()
    serializer_class = BlogPostSerializer


    def list(self, request, *args, **kwargs):
        most_recent_posts = self.queryset.order_by('-date_time')
        most_targetted_posts = ReviewModel.objects.all().order_by('-review_score')[:2]
        categories = CategoryModel.objects.all()

        post = self.get_serializer(most_recent_posts, many=True)
        targetted_posts = ReviewModelSerializer(most_targetted_posts, many=True)
        category_counts = CategoryModelSerializer(categories, many=True)

        return Response({'targetted_posts':targetted_posts.data,
                         'category_counts':category_counts.data[0]["Categories count"],
                         'post':post.data})

