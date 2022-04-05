from rest_framework import serializers
from translator.models import Translator, Contributor


class TranslatorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Translator


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Contributor
