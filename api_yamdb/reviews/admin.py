from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'category',
        'description',
        'year',
    )
    search_fields = ('name', 'category', 'genre', 'year')
    list_filter = ('genre', 'name', 'category')
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name', 'slug')
    list_filter = ('slug', 'name')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name', 'slug')
    list_filter = ('slug', 'name')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'score',
        'author',
        'text',
        'pub_date'
    )
    search_fields = ('title', 'autor')
    list_filter = ('score', 'title', 'author')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review',
        'author',
        'text',
        'pub_date'
    )
    search_fields = ('review', 'autor')
    list_filter = ('author', 'review', 'pub_date')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)

admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
