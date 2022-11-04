from django.shortcuts import render, redirect
from .forms import *
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
@login_required
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles' : articles,
    }
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect(request.GET.get("next") or 'articles:index')
    else:
        article_form = ArticleForm()

    context = {
        'article_form' : article_form
    }

    return render(request, 'articles/create.html', context)

@login_required
def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    recomment_form = ReCommentForm()
    article.hitCount += 1
    article.save()
    comments = article.comment_set.filter(parent_comment=None)
    context = {
        'article' : article,
        'comment_form' : comment_form,
        'comments' : comments, #애초에 Null 값 제거
        'recomment_form' : recomment_form,
        'hitCount': article.hitCount,
    }
   
    return render(request, 'articles/detail.html', context)

@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)

    if request.user == article.user:
        if request.method == 'POST':
            article_form = ArticleForm(request.POST, request.FILES, instance=article)

            if article_form.is_valid():
                article_form.save()
                return redirect("articles:detail", article.pk)
        else:
            article_form = ArticleForm(instance=article)
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/update.html', context)

    else:
        messages.warning(request, '작성자만 수정할 수 있습니다.')
        return redirect('articles:detail', article.pk)

@login_required
def delete(request, pk):
    Article.objects.get(id=pk).delete()
    return redirect('articles:index')


dic = {'0':'zero', '1':'one', '2':'two', '3':'three', '4':'four', '5':'five', '6':'six', '7':'seven', '8':'eight', '9':'nine'}
# 댓글
@login_required
def comments_create(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            temp = ''
            for i in str(comment.pk):
                temp += dic[i]
            comment.text = temp
            comment.save()
            return redirect('articles:detail', article.pk)

@login_required
def comments_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('articles:detail', article_pk)

# 대댓글
@login_required
def recomments_create(request, article_pk, comment_pk):
    # 현재 article 저장
    article = Article.objects.get(pk=article_pk)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            recomment = comment_form.save(commit=False)
            recomment.article = article
            recomment.user = request.user
            recomment.parent_comment_id = comment_pk
            temp = ''
            for i in str(comment_pk):
                temp += dic[i]
            recomment.text = temp
            recomment.save()

            return redirect('articles:detail', article.pk)

@login_required
def recomments_delete(request, article_pk, recomment_pk):
    recomment = Comment.objects.get(pk=recomment_pk)
    recomment.delete()
    return redirect('articles:detail', article_pk)

# # 대댓글 출력
# def reply(request, comment_pk):
#     temp = Comment.objects.filter(parent_comment_id=comment_pk)
#     arr = []
#     for i in temp:
#         arr.append((i.user.username, i.content))
#     return JsonResponse({'content': arr})

# 좋아요
@login_required
def like_article(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        user = article.user
        user.celsius -= 0.1
        user.celsius = round(user.celsius, 1)
        user.save()
    else:
        article.like_users.add(request.user)
        user = article.user
        user.celsius += 0.1
        user.celsius = round(user.celsius, 1)
        user.save()
    return redirect('articles:detail', pk)

# 싫어요
@login_required
def unlike_article(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user in article.unlike_users.all():
        article.unlike_users.remove(request.user)
        user = article.user
        user.celsius += 0.1
        user.celsius = round(user.celsius, 1)
        user.save()
    else:
        article.unlike_users.add(request.user)
        user = article.user
        user.celsius -= 0.1
        user.celsius = round(user.celsius, 1)
        user.save()
    return redirect('articles:detail', pk)


# 검색 기능
def search(request):
    search = request.GET.get("search")

    if search:
        search_result = Article.objects.filter(title__contains=search)
    context = {
        'search_result': search_result,
    }
    return render(request, 'articles/index.html', context)