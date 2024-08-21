from rest_framework import serializers


class InYoutube:
    """ Проверяет, что ссылка на видео относится к youtube.com """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'youtube.com' not in value.get('video'):
            message = f'Недопустимое значение в поле {self.field}!'
            raise serializers.ValidationError(message)
