from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse

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
    """Detail of a single article"""

    template_name = "blogapp/article_detail.html"
    context_object_name = "article"
    queryset = (
        Article.objects.select_related("author")
        .select_related("category")
        .prefetch_related("tags")
    )


class LatestArticlesFeed(Feed):
    """ Returns latest articles feed (RSS) """

    title = "Blog articles (latest)"
    description = "Updates on changes and additions blog articles"
    link = reverse_lazy("blogapp:articles_list")

    def items(self):
        return (
            Article.objects.select_related("author")
            .select_related("category")
            .prefetch_related("tags")
            .filter(pub_date__isnull=False)
            .order_by("-pub_date")
            .defer("content")[:5]
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]

    def item_link(self, item: Article):
        return reverse("blogapp:article_detail", kwargs={"pk": item.pk})
