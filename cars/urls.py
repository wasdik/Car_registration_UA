from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('brands/', views.BrandsView.as_view(), name='brands_list'),
    path('brands/<int:pk>/', views.BrandsDetailView.as_view(),
         name='brand_detail'),
    path('models/<int:pk>/', views.ModelsDetailView.as_view(),
         name='model_detail'),
    path('records/', views.RecordsView.as_view(), name='records_list'),
    path('records/<int:pk>/', views.RecordsDetailView.as_view(),
         name='record_detail'),
    path('load-data/', views.load_data, name='load_data'),
]
