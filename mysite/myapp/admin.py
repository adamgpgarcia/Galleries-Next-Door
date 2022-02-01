from django.contrib import admin

from . import models

# Register models here to have them show up in admin page
admin.site.register(models.PostModel)          #makes suggestion show up on admin page
admin.site.register(models.CommentModel)        #makes comment model show up on admin page
