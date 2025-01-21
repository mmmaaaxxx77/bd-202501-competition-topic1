from django.utils import timezone
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Article
from .serializers import ArticleSerializer
import datetime


class ArticleListCreateView(APIView):
    """
    GET: 查詢文章列表 (可模糊查 title / content；預設當日)
    POST: 建立文章
    """

    @swagger_auto_schema(
        operation_description="文章列表查詢。可根據 query 進行標題或內文模糊查詢，並可設定 startDate, endDate 來過濾發文時間。若未指定，預設查詢當日。",
        manual_parameters=[
            openapi.Parameter(
                name="query",
                in_=openapi.IN_QUERY,
                description="模糊匹配 title 或 content",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="startDate",
                in_=openapi.IN_QUERY,
                description="起始日期 (YYYY-MM-DD)，若無則預設今天最小值",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="endDate",
                in_=openapi.IN_QUERY,
                description="結束日期 (YYYY-MM-DD)，若無則預設今天最大值",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: ArticleSerializer(many=True)},  # 回傳的型別描述
    )
    def get(self, request):
        query_string = request.GET.get("query", "")
        start_date = request.GET.get("startDate", "")
        end_date = request.GET.get("endDate", "")

        if not start_date and not end_date:
            today = timezone.now().date()
            start_date = datetime.datetime.combine(today, datetime.time.min)
            end_date = datetime.datetime.combine(today, datetime.time.max)
        else:
            if start_date:
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            else:
                start_date = datetime.datetime.min

            if end_date:
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                end_date = end_date.replace(hour=23, minute=59, second=59)
            else:
                end_date = datetime.datetime.max

        articles = Article.objects.filter(
            Q(title__icontains=query_string) | Q(content__icontains=query_string),
            posttime__range=(start_date, end_date),
        ).order_by("-created_at")

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="建立新文章",
        request_body=ArticleSerializer,  # 請求的資料格式
        responses={201: ArticleSerializer, 400: "Bad Request"},  # 回傳的成功資料格式
    )
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            article = serializer.save()
            return Response(
                ArticleSerializer(article).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleRetrieveUpdateDeleteView(APIView):
    """
    GET by id: 取得文章
    POST: 完整修改文章 (title, content)
    PATCH: 局部修改文章 (title 或 content)
    DELETE: 刪除文章
    """

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return None

    def get(self, request, pk):
        article = self.get_object(pk)
        if not article:
            return Response(
                {"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="建立新文章",
        request_body=ArticleSerializer,  # 請求的資料格式
        responses={201: ArticleSerializer, 400: "Bad Request"},  # 回傳的成功資料格式
    )
    def post(self, request, pk):
        article = self.get_object(pk)
        if not article:
            return Response(
                {"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND
            )

        data = {
            "title": request.data.get("title", article.title),
            "content": request.data.get("content", article.content),
            "posttime": article.posttime,  # 不改
        }
        serializer = ArticleSerializer(article, data=data, partial=False)
        if serializer.is_valid():
            updated_article = serializer.save()
            return Response(ArticleSerializer(updated_article).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="部分更新(title 或 content)",
        request_body=ArticleSerializer,
        responses={
            200: ArticleSerializer,
            404: "Article not found",
            400: "Bad Request",
        },
    )
    def patch(self, request, pk):
        article = self.get_object(pk)
        if not article:
            return Response(
                {"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            updated_article = serializer.save()
            return Response(ArticleSerializer(updated_article).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        if not article:
            return Response(
                {"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND
            )
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
