from django.contrib.sitemaps import Sitemap

from shopapp.models import Product


class ShopSitemap(Sitemap):
    """Sitemap for shop"""

    changefreq = "never"
    priority = 0.5

    def items(self):
        return (
            Product.objects.select_related("created_by")
            .filter(archived=False)
            .defer("preview")
            .order_by("-created_at")
        )

    def lastmod(self, obj: Product):
        return obj.created_at
