from django.contrib import admin

from .models import Title, Category, Genre
from .models import User, Review, Comment

admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)

admin.site.register(Review)
admin.site.register(Comment)

admin.site.register(User)
