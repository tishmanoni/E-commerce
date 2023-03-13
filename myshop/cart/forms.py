from django import forms
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 4)]
Size_choice = (
        
        ("None", "None"),
        ('S', 'Small'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ("39", "39"),
        ("40", "40"),
        ("41", "41"),
        ("42", "42")
        

)
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    override = forms.BooleanField(required=False, initial=False,widget=forms.HiddenInput)
    size_cloth = forms.TypedChoiceField(required=False, choices=Size_choice,  label="Size:", initial='ms')
class CartSizeAddProductForm(forms.Form):
        size_cloth = forms.TypedChoiceField(required=False, choices=Size_choice,  label="Size:", initial='ms')
   
