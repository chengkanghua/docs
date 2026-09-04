from django.shortcuts import render, HttpResponse


# Create your views here.
def article_year(request, year):
    # 查询所有文章
    # select * from article where year = year

    return HttpResponse(year + " article")


# def article_month(request, year,month):
#     # 查询所有文章
#     # select * from article where year = year
#
#     return HttpResponse(f" {year}年{month}月的文章")


def article_month(request, month, year):

    # 查询所有文章
    # select * from article where year = year

    return HttpResponse(f" {year}年{month}月的文章")
