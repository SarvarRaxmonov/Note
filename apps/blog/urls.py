from rest_framework import routers
from django.urls import path
from .views import LoginView, RegisterView, BlogPostViewSet, BlogPostDetailViewset, AuthorViewset, ContactListCreateView

# BlogListCreateView, BlogDetailView
router = routers.DefaultRouter()

urlpatterns = [
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("main/", BlogPostViewSet.as_view({"get": "list"}), name="main"),
    path('blogpost/<int:pk>/', BlogPostDetailViewset.as_view({'get': 'retrieve'}), name='blogpost-detail'),
    path('author/<int:pk>/', AuthorViewset.as_view({'get': 'retrieve'}), name='author-detail'),
    path('contacts/', ContactListCreateView.as_view(), name='contact-list-create'),

]




