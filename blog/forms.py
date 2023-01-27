from django import forms
from blog.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["commented_post", "created_on"]
        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email",
            "content": "Your Comment"
        }
