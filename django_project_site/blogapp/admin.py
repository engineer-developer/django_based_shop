from django.contrib import admin

from blogapp.models import Article, Author, Tag, Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "bio")
    list_display_links = ("name",)
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "content",
        "pub_date",
        "author",
        "category",
    )
    search_fields = ("title", "content", "category", "tags")
