from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
class Friend(models.Model):
    to_user = models.ManyToManyField(User)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user', null=True)

    @classmethod
    def send_friend_request(cls, from_user, new_friend):
        friend, created = cls.objects.get_or_create(
            from_user=from_user
        )
        friend.to_user.add(new_friend)

    # @classmethod
    # def cancel_friend_request(cls, from_user, new_friend):

    # @classmethod
    # def accept_friend_request(cls, from_user, new_friend):
        
    @classmethod
    def delete_friend(cls, from_user, new_friend):
        friend, created = cls.objects.get_or_create(
            from_user=from_user
        )
        friend.to_user.remove(new_friend)
