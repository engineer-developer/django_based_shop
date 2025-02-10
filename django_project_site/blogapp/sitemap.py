from django.contrib.sitemaps import Sitemap

from blogapp.models import Article


class BlogSitemap(Sitemap):
    """Sitemap for Blog"""

    changefreq = "never"
    priority = 0.5

    def items(self):
        return (
            Article.objects.select_related("author")
            .select_related("category")
            .prefetch_related("tags")
            .filter(pub_date__isnull=False)
            .order_by("-pub_date")
            .defer("content")[:5]
        )

    def lastmod(self, obj: Article):
        return obj.pub_date
