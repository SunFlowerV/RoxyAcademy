from decimal import Decimal
from pathlib import PurePath

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from RoxyAcademyApp.models import Course


class CourseForm(forms.ModelForm):
    price = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'id': 'regularPrice-1',
            'form': 'course-create-form',
            'class': 'form-control',
            'min': '0',
            'step': '1',
        }),
    )

    class Meta:
        model = Course
        fields = (
            'title',
            'slug',
            'description',
            'difficulty',
            'is_free',
            'price',
            'thumbnail',
            'intro_video_file',
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'field-1',
                'form': 'course-create-form',
                'class': 'form-control',
                'placeholder': _('New Course'),
            }),
            'slug': forms.TextInput(attrs={
                'id': 'field-2',
                'form': 'course-create-form',
                'class': 'form-control',
                'placeholder': 'new-course',
            }),
            'description': forms.Textarea(attrs={
                'id': 'aboutCourse',
                'form': 'course-create-form',
                'class': 'form-control',
                'rows': 10,
            }),
            'difficulty': forms.Select(attrs={
                'id': 'field-4',
                'form': 'course-create-form',
                'class': 'w-100',
            }),
            'is_free': forms.CheckboxInput(attrs={
                'form': 'course-create-form',
                'class': 'form-check-input',
            }),
            'thumbnail': forms.FileInput(attrs={
                'id': 'createinputfile',
                'form': 'course-create-form',
                'class': 'inputfile',
                'accept': 'image/*',
            }),
            'intro_video_file': forms.FileInput(attrs={
                'id': 'introVideoFile',
                'form': 'course-create-form',
                'class': 'form-control',
                'accept': 'video/*',
            }),
        }
        labels = {
            'is_free': _('This Course is free for everyone.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['price'].required = False
        self.fields['difficulty'].choices = [
            (Course.DIFFICULTY_ALL_LEVELS, _('All Levels')),
            (Course.DIFFICULTY_BEGINNER, _('Beginner')),
            (Course.DIFFICULTY_INTERMEDIATE, _('Intermediate')),
            (Course.DIFFICULTY_ADVANCED, _('Advance')),
            (Course.DIFFICULTY_EXPERT, _('Expert')),
        ]
        if self.instance.pk and self.instance.price is not None:
            self.initial['price'] = int(self.instance.price)
        if not self.is_bound and self.instance._state.adding:
            self.initial['is_free'] = False

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('is_free'):
            cleaned_data['price'] = Decimal('0.00')
        else:
            price = cleaned_data.get('price')
            if price is None:
                self.add_error('price', _('Enter a price for a paid course.'))
            elif price <= 0:
                self.add_error('price', _('Price must be greater than zero for a paid course.'))
            else:
                cleaned_data['price'] = Decimal(price)
        return cleaned_data

    def clean_intro_video_file(self):
        video = self.cleaned_data.get('intro_video_file')
        allowed_extensions = {'.mp4', '.webm', '.ogg', '.ogv', '.mov', '.m4v', '.avi', '.mkv'}
        if video and PurePath(video.name).suffix.lower() not in allowed_extensions:
            raise ValidationError(_('Upload a video file in MP4, WebM, OGG, MOV, M4V, AVI, or MKV format.'))
        return video