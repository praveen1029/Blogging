from django.urls import path
from . import views


urlpatterns = [

    path("register/",views.UserRegisterAPI.as_view(),name='user_registeration'),
    path("register/admin/",views.AdminRegisterAPI.as_view(),name='admin_registeration'),

    path("create/blog/",views.ListCreateBlogsAPI.as_view(),name='create_blog'),
    path("list/my/blogs/",views.ListCreateBlogsAPI.as_view(),name='list_my_blog'),
    path("retrieve/blogs/<int:id>/",views.RetrieveUpdateDestroyBlogAPI.as_view(),name='retrieve_blog'),
    path("update/my/blogs/<int:id>/",views.RetrieveUpdateDestroyBlogAPI.as_view(),name='update_my_blog'),
    path("delete/my/blogs/<int:id>/",views.RetrieveUpdateDestroyBlogAPI.as_view(),name='delete_my_blog'),

    path("add/comment/",views.CreateCommentAPI.as_view(),name='create_comment'),
    path("update/my/comment/<int:id>/",views.UpdateMyCommentAPI.as_view(),name='update_my_comment'),
    path("delete/my/comment/<int:id>/",views.DeleteMyCommentAPI.as_view(),name='delete_my_comment'),

    path("list/blogs/",views.ListAllBlogsAPI.as_view(),name='list_blog'),
    path("delete/blogs/<int:pk>/",views.AdminDeleteBlogAPI.as_view(),name='admin_delete_blog'),
    path("list/comments/<int:id>/",views.AdminListCommentsAPI.as_view(),name='admin_list_comment'),
    path("delete/comments/<int:pk>/",views.AdminDeleteCommentsAPI.as_view(),name='admin_delete_comments'),
     
    path("logout/",views.LogoutAPI.as_view(),name='logout')
]
