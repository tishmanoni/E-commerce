from .models import Review, Contact, MailList
from django import forms


from django import forms
class EmailPostForm(forms.Form):
    name= forms.CharField(max_length=25)
    name= forms.CharField(max_length=25)
    email= forms.EmailField()
    Message = forms.CharField(required=False, widget=forms.Textarea)

class SearchForm(forms.Form):
    query = forms.CharField(label='Search')

class TrackOrderForm(forms.Form):
    query = forms.CharField(label='Track Order(Input your oder Id)')

SIZE_CHOICES = (

        ('S', 'Small'),
        ('L', 'Large')
    )




class VariationForm(forms.Form):
    size = forms.TypedChoiceField(required=True, choices=SIZE_CHOICES , widget=forms.RadioSelect, label="Size:")
  

class ContactForm(forms.Form):
    name= forms.CharField(max_length=500, label="Name")
    email= forms.EmailField(max_length=500, label="Email")
    comment= forms.CharField(label='',widget=forms.Textarea(
                        attrs={'placeholder': 'Enter your comment here'}))
    
class MailForm(forms.ModelForm):
    class Meta:
        model = MailList
        fields = ('email',)
    