from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    following = models.ManyToManyField(User, related_name='following', blank=True, symmetrical=False)
    created = models.DateTimeField(auto_now_add=True)
    

    def profiles_posts(self):
        return self.post_set.all()
    
    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()
        
    def __str__(self):
        return f'{self.user} Profile'

    class Meta:
        ordering = ('-created',)

def save(self, **kwargs):
    #save method for images
    super().save()
    
    img = Image.open(self.image.path)
    # method for resizing images
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)
        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
