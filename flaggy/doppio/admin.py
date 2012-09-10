from django.contrib import admin
from doppio.models import User, CheckIn, Follow, FollowPending

admin.site.register(User)
admin.site.register(CheckIn)
admin.site.register(Follow)
admin.site.register(FollowPending)