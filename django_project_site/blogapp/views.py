from django.views.generic import ListView, DetailView

from blogapp.models import Article


class ArticleListView(ListView):
    """List of all articles"""

    queryset = (
        Article.objects.select_related("author")
        .select_related("category")
        .prefetch_related("tags")
        .filter(pub_date__isnull=False)
        .order_by("-pub_date")
        .defer("content")
    )
    template_name = "blogapp/article_list.html"
    context_object_name = "articles"


class ArticleDetailView(DetailView):
    template_name = "blogapp/article_detail.html"
    context_object_name = "article"
    queryset = (
        Article.objects.select_related("author")
        .select_related("category")
        .prefetch_related("tags")
    )
