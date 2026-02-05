from django.urls import path
from . import views

app_name = 'work_orders'

urlpatterns = [  
    path('register/', views.register_work_order, name='register_work_order'),
    path('list/', views.work_order_list, name='work_order_list'),
    path('detail/<int:pk>/', views.work_order_detail, name='work_order_detail'),
    path('delete/<int:pk>/', views.delete_work_order, name='delete_work_order'),
    path('edit/<int:pk>/', views.edit_work_order, name='edit_work_order'),  # 編集用URL
    path('export_csv/', views.export_work_orders_csv, name='export_work_orders_csv'),  # CSVダウンロード用URL
    path('export_progress_csv/', views.export_workorderprogress_csv, name='export_workorderprogress_csv'),  # CSVダウンロード用URL
]
