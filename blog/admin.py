from django.contrib import admin
from .models import User, Blogs, Comments

# Register your models here.

admin.site.register(User)
admin.site.register(Blogs)
admin.site.register(Comments)
