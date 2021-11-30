"""
https://stackoverflow.com/questions/28036404/django-rest-framework-upload-image-the-submitted-data-was-not-a-file#28036805
"""
from rest_framework import serializers

class Base64Imagefield(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        # Six is a Python 2 and 3 compatibility library. TODO dont need maybe
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension,)
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64Imagefield, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        from imghdr import what
        extension = what(file_name, decoded_file)
        if extension == 'jpeg':
            extension = 'jpg'
        return extension