from django import forms
from core.models import Recipe
from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget


class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'image')
        
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


