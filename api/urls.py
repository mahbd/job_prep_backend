from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('problems', views.ProblemViewSet, basename='problems')

urlpatterns = router.urls
