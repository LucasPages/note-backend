from rest_framework.routers import DefaultRouter
from notes.views import NoteViewSet
from django.urls import include, path


router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')


urlpatterns = [
    path('', include(router.urls)),
]
