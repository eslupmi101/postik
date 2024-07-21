from django import forms
from emoji import is_emoji

from .constants import MAX_POST_PRICE, MIN_POST_PRICE
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
        min_length=5,
        max_length=32,
        widget=forms.TextInput(attrs={'maxlength': 32}),
        required=False,
    )
    description = forms.CharField(
        label='Описание',
        help_text='До 255 символов',
        max_length=255,
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 40, 'maxlength': 255}),
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
        help_text='От 5 до 32 символов',
        min_length=5,
        max_length=32,
        widget=forms.TextInput(attrs={'maxlength': 32}),
        required=False
    )
    description = forms.CharField(
        label='Описание',
        help_text='До 255 символов',
        max_length=255,
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 40, 'maxlength': 255}),
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

    def save(self, commit=True):
        card = super().save(commit=False)
        if self.cleaned_data.get('image'):
            card.image = self.cleaned_data['image']
        if self.cleaned_data.get('title'):
            card.title = self.cleaned_data['title']
        if self.cleaned_data.get('description'):
            card.description = self.cleaned_data['description']
        if self.cleaned_data.get('price'):
            card.price = self.cleaned_data['price']
        if commit:
            card.save()
        return card
