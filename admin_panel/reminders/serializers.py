from rest_framework import serializers
from .models import Event  # або твоя модель, якщо називається інакше

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate_user_id(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("user_id має бути цілим числом")
        return value

    def validate_date(self, value):
        import datetime
        if value < datetime.date.today():
            raise serializers.ValidationError("Дата не може бути в минулому")
        return value

    def validate(self, data):
        required_fields = ['text', 'location', 'link']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError({field: "Це поле є обов’язковим"})
        return data
