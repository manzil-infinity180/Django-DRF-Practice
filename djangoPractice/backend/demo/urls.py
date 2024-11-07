from django.urls import path, include
from demo import views
from demo.views import UserViewSet, DemoViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'demo', views.DemoViewSet, basename='demo')
router.register(r'user', views.UserViewSet, basename='user')



demo_list = DemoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
demo_details = DemoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get':'list'
})

user_details = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    # path('demo/<int:pk>/', views.DemoViewDetail.as_view()),
    # path('demo/<int:pk>/', views.DemoDetailsMixin.as_view()),
    path('demo/<int:pk>/', views.DemoDetailsGenerics.as_view(), name='demo-details'),
    # path('demo/<int:pk>/', demo_details, name='demo-details'),
    # path('demo/', views.DemoViewList.as_view())
    # path('demo/', views.DemoListMixin.as_view(), name='demo-list'),
    path('demo/', demo_list, name='demo-list'),
    # path('demo/', views.DemoListGenerics.as_view()),
    # path('users/', views.UserList.as_view(), name='users-list'),
    path('users/', user_list, name='users-list'),
    # path('users/<int:pk>/', views.UserDetails.as_view(), name='user-details'),
    path('users/<int:pk>/', user_details, name='user-details'),
    path('', views.api_root),
    path('demo/<int:pk>/highlight/', views.DemoHighlighted.as_view()),
    # path('', include(router.urls))
]


