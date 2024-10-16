from rest_framework.routers import DefaultRouter
from notes.views import NoteViewSet, UserViewSet
from django.urls import include, path


router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls'))
]
