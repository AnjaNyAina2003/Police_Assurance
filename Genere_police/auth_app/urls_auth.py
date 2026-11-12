from django.urls import path

from .views import GetUserView, ListUsersView, LogoutView, RegisterView, LoginView, UploadUserPhotoView, UserView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', GetUserView.as_view()),
    path('user/<int:pk>', UserView.as_view()),
    path('user/<int:pk>/upload_photo', UploadUserPhotoView.as_view(), name="upload_user_photo"),
    path('listUser', ListUsersView.as_view()),
    path('logout', LogoutView.as_view()),
]