from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('problems', views.ProblemViewSet, basename='problems')
router.register('tags', views.TagViewSet, basename='tags')
router.register('companies', views.CompanyViewSet, basename='companies')
router.register('statuses', views.StatusViewSet, basename='statuses')

app_name = 'api'
urlpatterns = router.urls
