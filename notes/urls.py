from rest_framework.routers import DefaultRouter
from notes.views import NoteViewSet, TagViewSet
from django.urls import include, path


router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]
