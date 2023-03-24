from .models import Blogs, Comments
from rest_framework.views import APIView
from rest_framework import generics, status
from .serializers import UserRegisterSerializer, AdminRegisterSerializer, BlogsSerializer, BlogsCommentsSerializer, CommentsSerializer
from django.core.mail import EmailMessage
from rest_framework.response import Response
from django.template.loader import get_template
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


# Create your views here.

# Register API
class UserRegisterAPI(APIView):
    permission_classes = [AllowAny, ]
    def post(self,request,format=None):
        serializer=UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            account=serializer.save()
        
            subject='Welcome'
            html_content=get_template('user.html').render({'user_name':account.name})
            from_email=settings.EMAIL_HOST_USER

            msg = EmailMessage(subject, html_content, from_email, [account.email])
            msg.content_subtype = "html" 
            msg.send()
            return Response("Registeration Successfull Check your Mail")
        else:
            data=serializer.errors
            return Response(data)
        

# Admin user register API
class AdminRegisterAPI(APIView):
    permission_classes = [IsAdminUser, ]
    def post(self,request,format=None):
        serializer=AdminRegisterSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()

            subject='Welcome'
            html_content=get_template('admin.html').render({'user_name':account.name})
            from_email=settings.EMAIL_HOST_USER

            msg = EmailMessage(subject, html_content, from_email, [account.email])
            msg.content_subtype = "html" 
            msg.send()
            return Response("Registeration Successfull Check your Mail")
        else:
            data=serializer.errors
            return Response(data)
        

# API for creating Blogs and listing blogs created by the user
class ListCreateBlogsAPI(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=BlogsSerializer

    # create
    def post(self, request, *args, **kwargs):
        author = self.request.user
        title = request.data['title']
        content = request.data['content']
        try:
            Blogs.objects.create(author=author,title=title,content=content)
            return Response("New blog Created!")
        except:
            return Response("Sorry blog name cannot be same, There is already a blog with the same name.")
    
    # list
    def get(self, *args, **kwargs):
        my_blog = Blogs.objects.filter(author=self.request.user)
        if not my_blog:
            return Response("You have not created a blog yet.")
        serializer = BlogsSerializer(my_blog, many=True)
        return Response(serializer.data)   
    

# API for retrieve, update and delete blogs created by the user
class RetrieveUpdateDestroyBlogAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # retrieve
    def get(self, request, *args, **kwargs):
        blog_id = self.kwargs['id']
        my_blog = Blogs.objects.filter(id=blog_id)
        if not my_blog:
            return Response("Invalid Blog ID!")
        serializer = BlogsCommentsSerializer(my_blog, many=True)
        return Response(serializer.data)  

    # update
    def put(self, request, *args, **kwargs):
        blog_id = self.kwargs['id']
        title = request.data['title']
        content = request.data['content']
        try:
            my_blog = Blogs.objects.get(id=blog_id,author=self.request.user)  
            my_blog.title = title
            my_blog.content = content
            my_blog.save()
            serializer = BlogsSerializer(my_blog)

        except Blogs.DoesNotExist:
            return Response("Invalid Blog ID!. you can only update your own Blog.")

        except:
            return Response("Sorry blog name cannot be same, There is already a blog with the same name.")
    
        return Response(serializer.data)

    #delete
    def delete(self, request, *args, **kwargs):
        blog_id = self.kwargs['id']
        author = self.request.user
        try:
            Blogs.objects.get(author=author,id=blog_id).delete()
        except:
            return Response("Invalid Blog ID!. you can only Delete your own Blog.")
        
        return Response("Your Blog is deleted Successfully!")


# API for listing all Blogs
class ListAllBlogsAPI(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer


# API for creating comment
class CreateCommentAPI(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CommentsSerializer
    def post(self, request, *args, **kwargs):
        author = self.request.user
        blog = request.data['blog']
        comment = request.data['comment']
        comment_data = Comments.objects.filter(blog=blog)
        if comment_data:
            return Response("You cannot comment as you have already commented under this blog.")
        try:
            blog_data = Blogs.objects.get(id=blog)
        except:
            return Response("Sorry Invalid blog ID!") 
        Comments.objects.create(author=author,blog=blog_data,comment=comment)
        return Response({"blog":blog_data.title , "comment":comment})
    

# API for updating comment
class UpdateMyCommentAPI(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        comment_id = self.kwargs['id']
        comment = request.data['comment']
        try:
            my_comment = Comments.objects.get(id=comment_id,author=self.request.user)  

        except Comments.DoesNotExist:
            return Response("Invalid comment ID!. you can only update your own Comment.")

        my_comment.comment = comment
        my_comment.save()
        serializer = CommentsSerializer(my_comment)
        return Response(serializer.data)
    

# API for deleting comment
class DeleteMyCommentAPI(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        comment_id = self.kwargs['id']
        try:
            Comments.objects.get(author=self.request.user, id=comment_id).delete()
        except:
            return Response("Invalid Comment ID!. you can only Delete your own Comment.")
        
        return Response("Your Comment is deleted Successfully!")
    

# API for deleteing any blog(for admin user)
class AdminDeleteBlogAPI(generics.DestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset = Blogs.objects.all()


# API for listing all comments(for admin user)
class AdminListCommentsAPI(generics.ListAPIView):
    permission_classes=[IsAdminUser]
    def get(self, request, *args, **kwargs):
        blog_id = self.kwargs['id']
        comment_data = Comments.objects.filter(blog=blog_id)
        serializer = CommentsSerializer(comment_data,many=True)
        return Response(serializer.data)


# APIfor deleting comments(for admin user) 
class AdminDeleteCommentsAPI(generics.DestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset = Comments.objects.all()


# API for logout
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)