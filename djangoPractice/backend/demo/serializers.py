from rest_framework import serializers
from .models import Demo
from django.contrib.auth.models import User
from .serializer1 import UserPublicSerializers
"""
Using HyperLinkedModelSerializer (it extend the ModelSerializer)
"""
# class UserSerializerHyperLinked(serializers.HyperlinkedModelSerializer):
#     demo = serializers.HyperlinkedRelatedField(many=True, view_name='demo-list', read_only=True)
#     class Meta:
#         model = User
#         fields = [
#             'id', 'username', 'demo', 'url'
#         ]

"""
Using the ModelSerializer
"""
class UserSerializers(serializers.HyperlinkedModelSerializer):
    # demo = serializers.PrimaryKeyRelatedField(many=True, queryset= Demo.objects.all())
    demo = serializers.HyperlinkedRelatedField(many=True, view_name='demo-details', read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username', 'demo'
        ]



class DemoSerializers(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    owner = UserPublicSerializers(source='user', read_only=True)
    # username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='demo-details', lookup_field='pk')
    class Meta:
        model = Demo
        fields = [
            'id',
            'owner',
            'title',
            'code',
            'language',
            'style',
            'url',
            'linenos'
        ]
    
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=True, max_length=150)
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.CharField(max_length=100, default='python')
    # style = serializers.CharField(max_length=100, default='friendly')


    # def create(self, validated_data):
    #     """
    #         Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     # return super().create(validated_data)
    #     return Demo.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     """
    #         Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.save()
    #     return instance