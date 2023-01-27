from django.shortcuts import render, get_object_or_404
from blog.models import Post, Comment
from blog.forms import CommentForm
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.




class StartingPage(ListView):
    template_name = "blog/index.html"
    model = Post
    context_object_name = "posts"
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(status=1).order_by('-updated_on')[:3]
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["saved_for_later"] = self.request.session.get("stored_posts")
        return context


class Posts(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "posts"
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(status=1).order_by('-updated_on')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context["saved_for_later"] = request.session.get("stored_posts")
        return context


class PostDetail(View):
    template_name = "blog/post-detail.html"
    model = Post
    
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
          is_saved_for_later = post_id in stored_posts
        else:
          is_saved_for_later = False

        return is_saved_for_later
    
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all(),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render( request, "blog/post-detail.html", context)
        
    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            post = Post.objects.get(slug=slug)
            comment.commented_post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug])) 
        
        context = {
            "post": post,
            "tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all(),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render( request, "blog/post-detail.html", context)
    
        
class ReadLaterView(View):
    # get of this class fetches all stored posts and presents them on separate page
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
          posts = Post.objects.filter(id__in=stored_posts)
          context["posts"] = posts
          context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    # post of this class add or removes a post to stored ones and returns on the same page
    # it came from
    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
          stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
          stored_posts.append(post_id)
        else:
          stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts
        
        url = request.META.get('HTTP_REFERER')
        if url:
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect("posts")
