from django import forms
from django.contrib.auth.models import User
from greeter.models import churchGoer, greeterID, greeterRecord, suggestion

class churchGoerForm(forms.ModelForm):
    class Meta:
        model = churchGoer

# class CategoryForm(forms.ModelForm):
    # name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # # An inline class to provide additional information on the form.
    # class Meta:
        # # Provide an association between the ModelForm and a model
        # model = Category

# class PageForm(forms.ModelForm):
    # title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    # url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # class Meta:
        # # Provide an association between the ModelForm and a model
        # model = Page

        # # What fields do we want to include in our form?
        # # This way we don't need every field in the model present.
        # # Some fields may allow NULL values, so we may not want to include them...
        # # Here, we are hiding the foreign key.
        # fields = ('title', 'url', 'views')
    # def clean(self):
        # cleaned_data = self.cleaned_data
        # url = cleaned_data.get('url')

        # # If url is not empty and doesn't start with 'http://', prepend 'http://'.
            # url = 'http://' + url
        # if url and not url.startswith('http://'):
            # cleaned_data['url'] = url
        # return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = greeterID
        fields = ('churchGoer',)
class greeterRecordForm(forms.ModelForm):
    class Meta:
        model = greeterRecord
        fields = ('flag',)
class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.setdefault('extra',())
        extra = kwargs.pop('extra')
        super(QuizForm, self).__init__(*args, **kwargs)
        self.fields['population'] = forms.MultipleChoiceField(choices=extra, widget=forms.RadioSelect)
    population = forms.MultipleChoiceField()
    Answer = forms.CharField(widget=forms.HiddenInput)

class SuggestionForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
        # greeter = kwargs.setdefault('greeter',())
        # greeter = kwargs.pop('greeter')
        # super(SuggestionForm, self).__init__(*args, **kwargs)
        # self.fields['greeterID'] = greeter
    category = forms.ModelMultipleChoiceField(queryset = suggestion.objects.all().values_list('category', flat=True), required=False)
    add_category = forms.CharField(max_length = 500,  required=False)
    #greeterID = forms.IntegerField(widget=forms.HiddenInput())
    
    class Meta:
        model = suggestion
        fields = ('category','add_category','subject', 'description', 'greeterID')

