from django.urls import path
from django.contrib import admin
from lead import views as lead_views


urlpatterns = [
    path('leadbulk/', lead_views.LeadBulkCreate.as_view({'post': 'create'}), name='lead-bulkcreate'),
    path('leadnote/', lead_views.LeadNoteViewSet.as_view({'post': 'create','get': 'list'}), name='lead-note'),
    path('leadnoteupdate/<id>/', lead_views.LeadNoteViewSet.as_view({'put': 'update','get': 'retrieve'}), name='lead-noteupdate'),
    path('leadnoteview/<lead_id>/', lead_views.LeadNoteRetrieveView.as_view({'get': 'list'}), name='lead-noteview'),
    path('leadsourcecategory/', lead_views.LeadSourceViewSet1.as_view({'post': 'create','get': 'list'}), name='lead-sourcecategory'),
    path('leadsource/', lead_views.LeadSourceViewSet.as_view({'post': 'create','get': 'list'}), name='lead-source'),
    path('leadsourceview/', lead_views.LeadSourceViewSet.as_view({'get': 'list'}), name='lead-create'),
    path('leadsourceupdate/<id>/', lead_views.LeadSourceViewSet.as_view({'get': 'retrieve','put': 'update'}), name='leadsourceupdate'),
    path('leadsourcedelete/<id>/', lead_views.LeadSourceViewSet.as_view({'get': 'retrieve','delete': 'destroy'}), name='leadsourcedelete'),
    path('leadcreate/', lead_views.LeadCreateView.as_view({'post': 'create'}), name='lead-create1'),
    path('leadview/', lead_views.LeadRetrieveView.as_view({'get': 'list'}), name='lead-listview'),
    path('leadview/<int:id>/', lead_views.LeadRetrieveView.as_view({'get': 'retrieve'}), name='lead-view1'),
    path('leadupdate/<int:id>/', lead_views.LeadUpdateAPIView.as_view(), name='lead-update1'),
    path('leaddelete/<int:id>/', lead_views.LeadDestroyAPIView.as_view(), name='lead-delete1'),
    # path('leadsourcedelete/<int:id>/', lead_views.LeadsourceDestroyView.as_view(), name='leadsouce-delete'),




    # path('profilepic/', lead_views.ProfilePicView.as_view(), name=''),
    # path('leadimage/', lead_views.LeadImageViewSet.as_view({'post': 'create', 'get': 'list'}), name='lead-image'),
    # path('leadimageupdate/<id>', lead_views.LeadImageViewSet.as_view({'get': 'retrieve', 'put': 'update'}),
    #      name='lead-imageupdate'),
    # path('leadimagedelete/<id>', lead_views.LeadImageViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
    #      name='lead-imageupdate'),
    # path('leadcreate1/<int:id>/', LeadCreateView.as_view({'get': 'retrieve','put': 'partial_update'}), name='lead-update'),
    # path('leadsourcecategory/', LeadSourcecategoryView.as_view({'post': 'create','get': 'list'}), name='lead-create'),
    # path('admin/', LeadSourceView.as_view({'post': 'create'}), name='lead-create'),
    # path('admin/<int:pk>/', LeadSourceView.as_view({'get': 'retrieve'}), name='lead-create'),
    # path('', views.LeadView.as_view({'post': 'create', 'get': 'list'})),
    # path('<int:id>/', views.LeadView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy','put': 'partial_update'})),

    ###########################################################################################


    # path('leadcreate/', LeadCreate.as_view({'post': 'create'}), name='lead-create'),
    # path('leadview/', LeadRetrieveView.as_view({'get': 'list'}), name='lead-list'),
    # path('leadview/<int:id>/', LeadRetrieveView.as_view({'get': 'retrieve'}), name='lead-view'),
    # path('leadupdate/<int:id>/', LeadUpdateAPI.as_view(), name='lead-update'),
    # path('leaddelete/<int:id>/', LeadDestroyAPI.as_view(), name='lead-delete'),


]
