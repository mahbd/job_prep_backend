from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

router = routers.DefaultRouter()
router.register('problems', views.ProblemViewSet, basename='problems')
router.register('tags', views.TagViewSet, basename='tags')
router.register('companies', views.CompanyViewSet, basename='companies')
router.register('statuses', views.StatusViewSet, basename='statuses')
router.register('users', views.UserViewSet, basename='users')

app_name = 'api'
urlpatterns = router.urls + [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
