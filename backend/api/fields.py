''' Fields for API. '''

from drf_extra_fields.fields import Base64ImageField


class Base64ImageFieldRelativePath(Base64ImageField):
    ''' Base64ImageField with relative path in representattion. '''
    def to_representation(self, file):
        if self.represent_in_base64:
            return super().to_representation(file)
        else:
            if not file:
                return None
            use_url = getattr(self, 'use_url', True)
            if use_url:
                try:
                    return file.url
                except AttributeError:
                    return None
            return file.name
