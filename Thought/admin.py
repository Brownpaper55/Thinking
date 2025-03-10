from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Thoughts

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
class UserAdmin(admin.ModelAdmin):
    model = User
    #just display username field 
    fields = ['username']
    inlines = [ProfileInline]

#unregister user 
admin.site.unregister(User)
#re-register user
admin.site.register(User, UserAdmin)
admin.site.register(Thoughts)


