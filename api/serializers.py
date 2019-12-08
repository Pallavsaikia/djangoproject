from django.contrib.auth.models import User
from dashboard_app.models import Query, Answer
from rest_framework import serializers
from helper.CustomResponse import CustomResponse


class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        ]

    def save(self):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        password = self.validated_data['password']
        if password != "":
            user.set_password(password)
            user.save()
            return user
        else:
            error = CustomResponse(success=False, error={'password': 'Password field cant be empty'})
            raise serializers.ValidationError(error.get_response)


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class QuerySerializers(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = [
            'question'
        ]

    def save(self, user):
        query = Query(
            question=self.validated_data['question'],
            asked_by=user
        )
        query.save()


class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'reply',
            'replied_to'
        ]

    def save(self, user):
        answer = Answer(
            reply=self.validated_data['reply'],
            replied_to=self.validated_data['replied_to'],
            replied_by=user,

        )
        query = Query.objects.get(id=self.data['replied_to'])
        if not query.closed:
            answer.save()
        else:
            error = CustomResponse(success=False, error={'thread': 'thread is closed'})
            raise serializers.ValidationError(error.get_response)


class USerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
        )
        read_only_fields = ('replied_to',)


class ASerializer(serializers.ModelSerializer):
    replied_by = USerializer()
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Answer
        fields = (
            'id',
            'reply',
            'replied_to',
            'replied_by'
        )
        read_only_fields = ('replied_to',)


class QSerializer(serializers.ModelSerializer):
    answers = ASerializer(many=True)

    class Meta:
        model = Query
        fields = (
            'id',
            'question',
            'answers'
        )
