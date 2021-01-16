from django.test import TestCase
from .models import Profile, User
from instaclone.models import Post, Comment

# Create your tests here.

class ProfileTest(TestCase):

    def setUp(self):
        self.new_user = User(username='@Sharon', email='anyangosharon26@gmail.com', password='@june2021')
        self.new_user.save()
        self.new_profile = Profile(image='image.png',user=self.new_user)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile, Profile))

    def test_save_method(self):
        self.new_profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)>0)
    
    def test_delete_method(self):
        self.new_profile.save_profile()
        self.new_profile.delete_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)==0)
        

class ImageTest(TestCase):

    def setUp(self):
        self.new_user = User(username='@Sharon', email='anyangosharon26@gmail.com', password='@june2021')
        self.new_user.save()
        self.new_profile = Profile(image='image.png', following=self.new_user, user=self.new_user)
        self.new_profile.save()
        self.new_post = Post(title='Moringa', content="I like Moringa", author=self.new_user, image='moringa.jpg',  liked=0)
        
        # Creating a new follow and saving it
        self.new_like = Like(user=new_user, value='LIKE')
        self.new_like.save()
        
        self.new_post.liked.add(self.new_like)
        
    def test_instance(self):
        self.assertTrue(isinstance(self.new_post,Post))

    def test_save_post(self):
        self.new_post.save_post()
        post = Post.objects.all()
        self.assertTrue(len(post)>0)

    def test_delete_post(self):
        self.new_post.save_post()
        self.new_post.delete_post()
        post = Post.objects.all()
        self.assertTrue(len(post)==0)

class CommentsTest(TestCase):

    def setUp(self):
        self.new_user = User(username='@Sharon', email='anyangosharon26@gmail.com', password='@june2021')
        self.new_user.save()
        self.new_post = Post(itle='Moringa', content="I like Moringa", author=self.new_user, image='moringa.jpg',  liked=0)
        self.new_post.save()
        self.new_comment = Comment(comment='Moringa is amazing', author=self.new_user, post=self.new_post)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))

    def test_save_comment(self):
        self.new_comment.save_comment()
        comment = Comment.objects.all()
        self.assertTrue(len(comment)>0)

    def test_delete_comment(self):
        self.new_comment.save_comment() 
        self.new_comment.delete_comment()
        comment = Comment.objects.all()
        self.assertTrue(len(comment)==0)

    def tearDown(self):
        Profile.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()
