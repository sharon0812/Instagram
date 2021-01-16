from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic  import ListView,DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, Comment, Like
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.contrib.auth.models import User
from users.models import Profile
from itertools import chain
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.

def follow_unfollow_profile(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)
        
        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
            
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('instaclone-index')
            
            

class PostListView(ListView):
    # model = Comment
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
   
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context.update({
            'comments': Comment.objects.order_by('created_on'),
            'profiles': Profile.objects.all().exclude(user=self.request.user)
            
        })
        return context

    def get_queryset(self):
        return Post.objects.order_by('-date_posted')
    
@login_required(login_url='/login/') 
def posts_of_following_profiles(request):
    user = request.user
    comments = Comment.objects.order_by('created_on'),
    profiles = Profile.objects.all().exclude(user=request.user)
    
    profile = Profile.objects.get(user=request.user)
    users = [user for user in profile.following.all()]
    posts = []
    qs = None
    for u in users:
        p = Profile.objects.all().filter(user=u)
        p_posts = Post.objects.all().filter(author__id__in=p)
        posts.append(p_posts)
    my_post = profile.profiles_posts()
    posts.append(my_post)
    if len(posts)>0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.date_posted)
    
    return render(request, 'index.html', {'posts':qs, 'comments':comments, 'profiles':profiles, 'profile':profile, 'user':user})

class PostDetailView(DetailView):
    model = Post
    
class ProfileDetailView(DeleteView):
    model = Profile
    template_name = 'instaclone/detail.html'
    
    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False
        context["follow"] = follow
        # context['posts'] = posts
        # context["post"] = Post.objects.filter(pk=pk)
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self,form):
        # self.object = form.save(commit=False)
        form.instance.author = self.request.user.profile
        # self.object.save()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form) 
    
    def test_func(self):
        post = self.get_object() 
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object() 
        if self.request.user == post.author:
            return True
        return False
    
    


@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = User.objects.filter(username__icontains = search_term)
        message = f"{search_term}"
        print(searched_users)
        profile_pic = User.objects.all()
        return render(request, 'instaclone/search.html', {'message':message, 'results':searched_users, 'profile_pic':profile_pic})
    else:
        message = "You haven't searched for any term"
        return render(request, 'instaclone/search.html', {'message':message})

def post_detail(request, slug):
    template_name = 'post_detail.html'
    # post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True) #retrieves all the approved comments from the database.
    new_comment = None

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)

            # Assign the current post to the comment
            new_comment.post = post

            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
    
def comment(request,post_id):
        current_user=request.user
        post = Post.objects.get(id=post_id)
        profile_owner = User.objects.get(username=current_user.username)
        comments = Comment.objects.filter(post=post)
        for comm  in comments:
            print(comm.comment)
            print(comm.author)
        if request.method == 'POST':
                form = CommentForm(request.POST, request.FILES)
                if form.is_valid():
                        comment = form.save(commit=False)
                        comment.post = post
                        comment.author = request.user
                        comment.save()
                return redirect('instaclone-index')
        else:
                form = CommentForm()
 
        return render(request, 'instaclone/comment.html',locals())
   
   
   
@csrf_exempt
def like_post(request, post_id):
    user = User.objects.get(pk=request.POST['user_id'])

    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
            
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)
        
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
                
                    
        like.save()       
    
    return JsonResponse({"likes":len(post_obj.liked.all())})
        

