from django import forms
from emoji import is_emoji

from .constants import (
    MIN_LENGTH_CARD_TITLE,
    MAX_LENGTH_CARD_TITLE,
    MAX_LENGTH_CARD_DESCRIPTION,
    MIN_LENGTH_POST_TITLE,
    MAX_LENGTH_POST_DESCRIPTION,
    MIN_POST_PRICE,
    MAX_POST_PRICE,
    MAX_LENGTH_POST_TITLE
)
from .models import Card, Post


class CardForm(forms.ModelForm):
    image = forms.ImageField(
        label='Изображение',
        allow_empty_file=False,
        help_text='Введите квадратную картинку',
        required=False
    )
    title = forms.CharField(
        label='Название',
        help_text='От 5 до 32 символов',
        min_length=MIN_LENGTH_CARD_TITLE,
        max_length=MAX_LENGTH_CARD_TITLE,
        widget=forms.TextInput(attrs={'maxlength': MAX_LENGTH_CARD_TITLE}),
        required=False,
    )
    description = forms.CharField(
        label='Описание',
        help_text=f'До {MAX_LENGTH_CARD_DESCRIPTION} символов',
        max_length=MAX_LENGTH_CARD_DESCRIPTION,
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40, 'maxlength': MAX_LENGTH_CARD_DESCRIPTION}),
        required=False
    )

    title.widget.attrs.update({
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
    })
    description.widget.attrs.update({
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
    })

    class Meta:
        model = Card
        fields = ['image', 'title', 'description']


class PostForm(forms.ModelForm):
    image = forms.CharField(
        label='Лого поста',
        required=False
    )
    title = forms.CharField(
        label='Название',
        help_text=f'От {MIN_LENGTH_POST_TITLE} до {MAX_LENGTH_POST_TITLE} символов',
        min_length=MIN_LENGTH_POST_TITLE,
        max_length=MAX_LENGTH_POST_TITLE,
        widget=forms.TextInput(attrs={'maxlength': MAX_LENGTH_POST_TITLE}),
        required=False
    )
    description = forms.CharField(
        label='Описание',
        help_text=f'До {MAX_LENGTH_POST_DESCRIPTION} символов',
        max_length=MAX_LENGTH_POST_DESCRIPTION,
        widget=forms.Textarea(attrs={'rows': 8, 'cols': 40, 'maxlength': MAX_LENGTH_POST_DESCRIPTION}),
        required=False
    )
    price = forms.IntegerField(
        label='Цена',
        help_text='введите цену до 100 000',
        min_value=MIN_POST_PRICE,
        max_value=MAX_POST_PRICE,
        required=False
    )

    title.widget.attrs.update({
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-2/3 p-2.5'
    })
    description.widget.attrs.update({
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
    })
    price.widget.attrs.update({
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-1/3 md:w-1/4 p-2.5'
    })

    class Meta:
        model = Post
        fields = ['image', 'title', 'description', 'price']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not is_emoji(image):
            raise forms.ValidationError('The image field must contain only one emoji.')
        return image
