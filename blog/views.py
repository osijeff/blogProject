from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm , CommentForm
from taggit.models import Tag
from django.db.models import Count


# Create your views here.
def post_list(request, tag_slug=None):
     object_list = Post.published.all()
     item = Post.published.get(id=3)
     editor= Post.objects.filter(id__in=[1, 2, 3, 5])
     tag = None
     if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
     paginator = Paginator(object_list, 3) # 3 posts in each page
     page = request.GET.get('page')
     try:
          posts = paginator.page(page)
     except PageNotAnInteger:
 # If page is not an integer deliver the first page
          posts = paginator.page(1)
     except EmptyPage:
 # If page is out of range deliver last page of results
          posts = paginator.page(paginator.num_pages)
     
     return render(request, 'post_lists.html', { 'page': page, 'posts': posts, 'tag': tag, 'item': item, 'editor': editor })
 


 
def post_detail(request, year, month, day, post):
     post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
     comments = post.comments.filter(active = True)
     new_comment = None
    
     if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
     else:
        comment_form = CommentForm()
        
        # similar Post
     post_tags_ids = post.tags.values_list('id', flat=True)
     similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
     similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
     return render(request,'pages/details.html',{'post': post, 'comments': comments,'new_comment': new_comment,'comment_form': comment_form, 'similar_posts': similar_posts})
 
class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'
    
    
    
# HANDLING FORM
def post_share(request, post_id):
    # retrieve post by id
    post= get_object_or_404(Post, id = post_id, status="published") 
    sent = False
    if request.method == 'POST':
        #Form was Submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title} " 
            message = f" Read {post.title} at {post_url} \n \n" f"{cd['name']} \'s comments: {cd['comments']}"
            send_mail(subject, message, 'aimuajeffrey@gmail.com', [cd['to']])
            sent =True
                    
    else:
        form = EmailPostForm()
    return render(request, 'pages/share.html', {'post':post, 'form':form, 'sent':sent})
