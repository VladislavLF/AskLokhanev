from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from app.models import Profile, Answer, Question
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


User = get_user_model()


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Enter your login',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'
        }),
        strip=False
    )

    error_messages = {
        'invalid_login': "Incorrect credentials. Please try again.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'aria-describedby': 'usernameHelp'})
        self.fields['password'].widget.attrs.update({'aria-describedby': 'passwordHelp'})


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(
        label="Login",
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Enter your login'
        }),
        help_text="Required field. No more than 150 characters. Only letters, numbers, and @/./+/-/_."
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Enter your email'
        })
    )
    name = forms.CharField(
        label="Nickname",
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Enter your nickname'
        }),
        help_text="Required field. No more than 150 characters. Only letters, numbers, and @/./+/-/_."
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Enter your password'
        }),
        help_text="The password must be at least 8 characters long."
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Repeat password'
        })
    )
    avatar = forms.ImageField(
        label="Avatar",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control mb-2'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this login already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email is already registered.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            validate_password(password1)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "The passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            avatar = self.cleaned_data.get('avatar')
            if avatar == None:
                avatar = 'avatars/default.png'
            Profile.objects.create(
                user=user,
                name=self.cleaned_data.get('name'),
                avatar=avatar
            )
        return user


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={
        'class': 'form-control mb-2',
        'placeholder': 'Enter your login'
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control mb-2',
        'placeholder': 'Enter your email'
    }))
    name = forms.CharField(label="Nickname", widget=forms.TextInput(attrs={
        'class': 'form-control mb-2',
        'placeholder': 'Enter your nickname'
    }))
    avatar = forms.ImageField(
        label="Avatar",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control mb-2'
        })
    )

    class Meta:
        model = Profile
        fields = ['username', 'email', 'name', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.email = self.cleaned_data['email']
        profile.user.username = self.cleaned_data['username']
        profile.name = self.cleaned_data['name']
        profile.avatar = self.cleaned_data['avatar']
        if commit:
            profile.user.save()
            profile.save()
        return profile


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Enter your answer...',
                'id': 'answer-textarea'
            }),
        }
        labels = {
            'text': 'Your Answer'
        }
        help_texts = {
            'text': 'Minimum 20 characters'
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 20:
            raise forms.ValidationError("The answer must contain at least 20 characters.")
        return text


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=200,
        required=False,
        help_text="Enter tags separated by commas"
    )

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

    def clean_tags(self):
        tags_string = self.cleaned_data['tags']
        tag_list = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
        if len(tag_list) > 3:
            raise forms.ValidationError("Maximum 3 tags.")
        return tag_list
