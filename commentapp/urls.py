from django.urls import path

from commentapp.views import CommentCreateView, CommentDetailView, CommentDeleteView

app_name = 'commentapp'

urlpatterns = [

    path('create/',CommentCreateView.as_view(),name='create'),
    path('detail/',CommentDetailView.as_view(),name='detail'),
    path('delete/<int:pk>',CommentDeleteView.as_view(),name='delete'),

]