from django.urls import path

from profileapp.views import ProfileCreateView, ProfileUpdateView

app_name = "profileapp" # 추후 함수 활용을 위해서 설정 해줌.

urlpatterns = [
    path('create/',ProfileCreateView.as_view(),name='create'),
    path('update/<int:pk>',ProfileUpdateView.as_view(),name='update'),
]