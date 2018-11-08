from django.urls import path
from django.conf.urls import url
from bankApp import views as bankApp_views



urlpatterns = [
    path('', bankApp_views.index, name='index'),
    path('banks/', bankApp_views.autocomplete),
    path('city/', bankApp_views.cityautocomplete),
    url(r'^ifsc/$', bankApp_views.IfscView.as_view(), name='get_ifsc_page'),
    url(r'^ifsc/(?P<ifsc>\w+)/$', bankApp_views.IfscView.as_view(), name='get_ifsc_details'),
    url(r'^branches/$', bankApp_views.BranchesListView.as_view(), name='get_branch_page'),
    url(r'^branches/(?P<bank_id>\d+)/$', bankApp_views.BranchesListView.as_view(), name='get_branch_list'),
    url(r'^branches/(?P<bank_id>\d+)/(?P<city>\D+)/$', bankApp_views.BranchesListView.as_view(), name='get_branch_list_by_city'),
]
