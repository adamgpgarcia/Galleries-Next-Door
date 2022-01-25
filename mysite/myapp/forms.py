from django import forms
#from django.core.validators import validate_slug
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models

def must_be_caps(value):
    if not value.isupper():
        raise forms.ValidationError("Not all uppercase")
    return value

def must_be_bob(value):
    if not value.startswith("bob"):
        raise forms.ValidationError("Must start with bob")
    return value

def must_be_unique(value):
    user = User.objects.filter(email=value)
    if len(user) > 0:
        raise forms.ValidationError("Email Already Exists")
    return value

class PostForm(forms.Form):
    title = forms.CharField(
        label='Title of Art',
        required=True,
        max_length=240,

    )
    image = forms.ImageField(
        label="Image File",
        required=True
    )
    image_description=forms.CharField(
        label="Description",
        max_length=240,
        required=False
    )
    auction_at=forms.IntegerField(
        label="Likes Required to Start Auction",
        max_value = 1000,
        min_value = 1
    )


    def save(self, request):
        post_instance = models.PostModel()
        post_instance.author = request.user
        post_instance.title = self.cleaned_data["title"]
        post_instance.image = self.cleaned_data["image"]
        post_instance.image_description = self.cleaned_data["image_description"]
        post_instance.auction_at = self.cleaned_data["auction_at"]
        post_instance.save()


class PostUpdateForm(forms.Form):
    title = forms.CharField(
        label='Title of Art',
        required=False,
        max_length=240,
    )
    image = forms.ImageField(
        label="Image File",
        required=False
    )
    image_description=forms.CharField(
        label="Description",
        max_length=240,
        required=False
    )
    auction_at=forms.IntegerField(
        label="Likes Required to Start Auction",
        max_value = 1000,
        min_value = 1
    )

    def save(self, request):

        post = models.PostModel.objects.get(id=request.id)
        print("title", post.title)

        post_instance = models.PostModel()

        post_instance.title = form.cleaned_data["title"]
        post_instance.image = form.cleaned_data["image"]
        post_instance.image = form.cleaned_data["image"]
        post_instance.image_description = form.cleaned_data["image_description"]
        post_instance.auction_at = form.cleaned_data["auction_at"]
        post_instance.save()


class CommentForm(forms.Form):
    comment = forms.CharField(
        label='Comment',
        required=True,
        max_length=240,
        #validators= [must_be_caps, must_be_bob],    #validate_slug,
    )

    def save(self, request, sugg_id):
        post_instance = models.PostModel.objects.get(id=sugg_id)
        comment_instance = models.CommentModel()
        comment_instance.suggestion = post_instance
        comment_instance.comment = self.cleaned_data["comment"]
        comment_instance.author = request.user
        comment_instance.save()
        return comment_instance



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
        )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
