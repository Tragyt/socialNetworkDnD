from django.forms import ModelForm, FileField, FileInput, CharField, Textarea

from campaigns.models import Post


class NewPostForm(ModelForm):
    body = CharField(widget=Textarea(attrs={"class": "form-control", "rows": "3"}), required=False)
    img = FileField(widget=FileInput(), required=False)

    class Meta:
        model = Post
        fields = ("title", "body", "img")
