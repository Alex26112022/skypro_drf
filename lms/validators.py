from rest_framework import serializers


class InYoutube:
    """ Проверяет, что ссылка на видео относится к youtube.com """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        print(value['video'])
        if 'youtube.com' not in value['video']:
            message = f'Недопустимое значение в поле {self.field}!'
            raise serializers.ValidationError(message)
