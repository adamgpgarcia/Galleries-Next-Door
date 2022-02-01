from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


#the post model is for art action postings 
class PostModel(models.Model):
    title = models.CharField(max_length=240)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        max_length=144,
        upload_to='uploads/%Y/%m/%d/',
        null=False
    )
    image_description = models.CharField(
        max_length = 240,
        null=False
    )
    auction_at=models.IntegerField()

    current_bet = models.IntegerField(
        default = 0
    )
    current_bet_leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name ="bet_leader",
        null=True,
        blank=True
    )

    likes = models.ManyToManyField(
        User,
        related_name="art_post",
        blank=True
    )

    total_likes = models.IntegerField(
        default = 0
    )

    auction_start = models.DateTimeField(
        null=True,
        blank=True
    )

    #0 = listed #1 = auction #2 = sold
    current_state = models.IntegerField(
        default = 0
    )

    def __str__(self):          # uses self to label suggestions
        return str(self.id) + " - " + self.author.username                      #string method better method on models page


#the comment model allows users to leave comments on art posts 
class CommentModel(models.Model):
    comment = models.CharField(max_length=240)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now=True)
    title = models.ForeignKey(PostModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    def last_10_messages(self):
        return CommentModel.objects.order_by('-timestamp').all()[:10]
