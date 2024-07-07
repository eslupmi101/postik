from django import forms

from posts.models import Card, Post
from posts.constants import MAX_POST_PRICE


class CardForm(forms.ModelForm):
    title = forms.CharField(
        label='Название карты'
    )
    description = forms.CharField(
        label='Описание карты'
    )

    class Meta:
        model = Card
        fields = ['title', 'description', 'image', 'posts']

    def clean_posts(self):
        data = self.cleaned_data['posts']
        for post in data:
            if post.user != self.user:
                raise forms.ValidationError(
                    f'Невалидный пост {id}'
                )

        return data

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=32
    )
    description = forms.CharField(
        max_length=255,
        required=False
    )
    price = forms.IntegerField(
        min_value=0,
        max_value=MAX_POST_PRICE
    )

    class Meta:
        model = Post
        fields = ['image', 'title', 'description', 'price']
