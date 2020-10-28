from . import serializers


class NewTimerSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    return_address = serializers.CharField(required=True)
    action_date = serializers.DateTimeField(required=False)
    interval = serializers.IntegerField(required=True)
    param = serializers.CharField(required=False)


class StopTimerSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    signature = serializers.CharField(required=True)
