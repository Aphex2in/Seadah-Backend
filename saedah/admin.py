from django import forms
from django.contrib import admin
from django.contrib.auth.models import Permission

from saedah.serializers import UserSerializer
from .models import Comments, DealPhotos, User, Deal

class CustomUserAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fullname', 'username', 'password', 'email', 'role', 'avatar']

    def save(self, commit=True):
        user = super().save(commit=False)
        user_serializer = UserSerializer(data=self.cleaned_data)  # Create a user using the serializer
        if user_serializer.is_valid():
            user = user_serializer.save()
            if commit:
                user.save()
            return user
        return None  # Return None if the serializer is not valid

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fullname', 'username', 'password', 'email', 'role', 'avatar']

class CustomDealsCreationForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['id', 'posted_by', 'title', 'description', 'expiry_date', 'tags', 'price', 'voucher', 'latitude', 'longitude']

class CustomDealsChangeForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['id', 'posted_by', 'title', 'description', 'expiry_date', 'tags', 'price', 'voucher', 'latitude', 'longitude']


class DealPhotosInline(admin.TabularInline):
    model = DealPhotos
    extra = 3  # Set the number of empty photo slots for each deal

class DealsAdmin(admin.ModelAdmin):
    add_form = CustomDealsCreationForm
    form = CustomDealsChangeForm
    inlines = [DealPhotosInline]  # Add the inline for DealPhotos
    
    list_display = ('id', 'posted_by', 'title', 'description', 'expiry_date', 'tags', 'price', 'voucher', 'latitude', 'longitude')
    search_fields = ('id',)
    list_filter = ('id',)
    ordering = ('id',)

class UserAdmin(admin.ModelAdmin):
    form = CustomUserAddForm

    list_display = ('username', 'email', 'role', 'fullname', 'avatar')
    search_fields = ('id','username', 'email', 'fullname')
    list_filter = ('role',)
    ordering = ('-date_joined',)
    
    

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_posted_by_username', 'deal_id', 'content', 'created_at')
    search_fields = ('id',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    def deal_id(self, obj):
        return obj.Deal_id.id  # Display the ID of the related Deal

    deal_id.short_description = 'Deal id'  # Set the custom column name

    def get_posted_by_username(self, obj):
        return obj.posted_by.username  # Display the username of the related user

    get_posted_by_username.short_description = 'Posted by'  # Set the custom column name

admin.site.register(User, UserAdmin)
admin.site.register(Deal, DealsAdmin)
admin.site.register(Comments, CommentsAdmin)