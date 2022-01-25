from django.contrib import admin

from . import models

# Register your models here have to register all new models
admin.site.register(models.PostModel)          #makes suggestion show up on admin page
admin.site.register(models.CommentModel)        #makes comment model show up on admin page
