from django.urls import path

from blogapp.views import ArticleListView, ArticleDetailView, LatestArticlesFeed


app_name = "blogapp"

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="articles_list"),
    path("articles/<int:pk>", ArticleDetailView.as_view(), name="article_detail"),
    path("articles/latest/feed/", LatestArticlesFeed(), name="articles_feed"),
]
