from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm
from .models import Post


@login_required
def feed(request):

    posts = Post.objects.select_related(
        'author',
        'author__profile'
    ).order_by('-created_at')

    if request.method == 'POST':

        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('feed')

    else:
        form = PostForm()

    return render(
        request,
        'posts/feed.html',
        {
            'posts': posts,
            'form': form,
        }
    )


@login_required
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    if post.author != request.user:
        return redirect('feed')

    if request.method == 'POST':
        post.delete()

    return redirect('feed')