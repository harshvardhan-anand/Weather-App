from django import forms
from mainapp.resources import utility

# we will not apply drop down in for cities as total cities are 20820 which takes time and gives bad experiance instead we will just give text area for city.

# initial parameter is used to provide initial default value
# choices are the dropdown select options
# ChoiceField are used to create dropdown menu
class UserParam(forms.Form):
    '''
    Front-end setup
    '''
    R = utility.Resources()
    city_name = forms.CharField(label='City Name')
    unit = forms.ChoiceField(label='Unit', 
                                choices=R.unit_choice,
                                initial='celsius')
    language = forms.ChoiceField(label='Language', 
                                choices=R.lang_choice,
                                initial='en')
    tz = forms.ChoiceField(label='Time Zone',
                            choices=R.timezone,
                            initial='IST')

    # https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
    # https://stackoverflow.com/a/5827669/11121579 or
    # https://stackoverflow.com/a/5827671/11121579 or
    # https://docs.djangoproject.com/en/3.0/ref/forms/widgets/#styling-widget-instances

    # addding css to form    
    city_name.widget.attrs.update(
        {
            'id':'cityname',  # modifing default ID
            'class':'your class',
            'required':True
        }
    )

    unit.widget.attrs.update(
        {
            'id':'unit',
            'class':'your class'
        }
    )

    language.widget.attrs.update(
        {
            'id':'language',
            'class':'your class'
        }
    )

    tz.widget.attrs.update({
        'id':'tz',
        'class':'your class'
    })