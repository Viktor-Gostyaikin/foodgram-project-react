''' Common widget classes for project. '''

from django import forms


class ColorInput(forms.TextInput):
    ''' Widget class for HTML5 color input. '''
    input_type = 'color'


class PasswordInput(forms.TextInput):
    '''
    Widget class for password input with a button to view the value.
    '''
    input_type = 'password'

    class Media:
        css = {
            'all': ('widgets/password/css/password-view.css',)
        }
        js = ('widgets/password/js/password-view.js',)


class DragableImageInput(forms.FileInput):
    '''
    Widget class for file input with drag&drop area.
    '''
    def __init__(self, attrs=None):
        default_attrs = {
            'accept': 'image/jpg, image/jpeg, image/bmp, image/gif, image/png'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    class Media:
        css = {
            'all': (
                'widgets/drag-area/css/drag-area.css',
            )
        }
        js = (
            'widgets/drag-area/js/drag-area.js',
        )
