from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'', views.TestAPI, basename='testapi')
urlpatterns = router.urls