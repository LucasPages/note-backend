from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from notes.urls import router as notes_router
from users.urls import router as users_router


router = DefaultRouter()
router.registry.extend(notes_router.registry)
router.registry.extend(users_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/', include('auth.urls')),
]
