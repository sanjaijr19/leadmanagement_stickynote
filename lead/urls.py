from django.urls import path

from lead import views
from .views import (
    LeadView,
    LeadCreateView,
    LeadListView,
    LeadRetrieveView,
    LeadUpdateView,
    LeadDeleteView,
    LeadCategoryViewSet,
)

urlpatterns = [
    path('lead/', views.LeadView.as_view({'post': 'create', 'get': 'list'})),
    path('lead/<int:id>/', views.LeadView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('leadgetall/', LeadListView.as_view(), name='lead-list'),
    path('leadget/', LeadCategoryViewSet.as_view(), name='lead-li'),
    path('lead/create/', LeadCreateView.as_view(), name='lead-create'),
    path('lead/get/<int:id>/', LeadRetrieveView.as_view(), name='lead-detail'),
    path('lead/update/<int:id>/', LeadUpdateView.as_view(), name='lead-update'),
    path('lead/delete/<int:id>/', LeadDeleteView.as_view(), name='lead-delete'),
]
