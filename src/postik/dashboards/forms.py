from django import forms

from posts.models import Card, Post


class CardForm(forms.ModelForm):
    title = forms.CharField(
        label='Название карты'
    )
    description = forms.CharField(
        label='Описание карты'
    )
    posts = forms.ModelMultipleChoiceField(
        queryset=Post.objects.all()
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
