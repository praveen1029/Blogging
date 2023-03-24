from rest_framework import serializers
from .models import User, Blogs, Comments

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','email','phone','password']
        
    def save(self):
        reg=User(
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
        )
        password=self.validated_data['password']        
        reg.set_password(password)
        reg.save()
        return reg
    

class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','email','phone','password']
        
    def save(self):
        reg=User(
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            is_staff = True,
            is_superuser = True
        )
        password=self.validated_data['password']        
        reg.set_password(password)
        reg.save()
        return reg


class BlogsSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author')
    class Meta:
        model = Blogs
        exclude= ['author']


class CommentsSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author')
    blog_name = serializers.CharField(source='blog')
    class Meta:
        model = Comments
        exclude= ['author','blog']  


class BlogsCommentsSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author')
    comment_set = serializers.SerializerMethodField()
    class Meta:
        model = Blogs
        fields = ['id','author_name','title','content','comment_set']

    def get_comment_set(elf,obj):
            blog_comment = Comments.objects.filter(blog=obj)
            serializer = CommentsAuthorTitleSerializer(blog_comment,many=True)
            return serializer.data 


class CommentsAuthorTitleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author')
    class Meta:
        model = Comments
        fields = ['author_name','comment']  