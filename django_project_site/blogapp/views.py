from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Article


class ArticleListView(ListView):
    """List of all articles"""

    queryset = (
        Article.objects.select_related("author")
        .select_related("category")
        .prefetch_related("tags")
        .order_by("-pub_date")
    )
    template_name = "blogapp/article_list.html"
    context_object_name = "articles"
