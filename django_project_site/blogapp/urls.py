from django.urls import path

from blogapp.views import ArticleListView


app_name = "blogapp"

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="articles_list"),
]
