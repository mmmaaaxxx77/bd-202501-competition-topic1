from django.urls import path
from .views import (
    ArticleListCreateView,
    ArticleRetrieveUpdateDeleteView,
)

urlpatterns = [
    path("articles/", ArticleListCreateView.as_view(), name="article-list-create"),
    path(
        "articles/<uuid:pk>/",
        ArticleRetrieveUpdateDeleteView.as_view(),
        name="article-detail",
    ),
]
