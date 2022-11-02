from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
    
    context = {
        'article' : article,
        'comment_form' : comment_form,
        'comments' : article.comment_set.all()
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

            return redirect('articles:detail', article.pk)

@login_required
def comments_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('articles:detail', article_pk)

# 대댓글
@login_required
def recomments_create(request, article_pk, comment_pk):
    # 현재 article과 대댓글 달 부모 comment를 저장
    article = Article.objects.get(pk=article_pk)
    comment = Comment.objects.get(pk=comment_pk)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.parent_comment_id = comment_pk
            comment.save()

            return redirect('articles:detail', article.pk)

# 좋아요
@login_required
def like_article(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
    return redirect('articles:detail', pk)