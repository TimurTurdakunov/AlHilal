from rest_framework import serializers
from directories.models import *


class KatoRegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = KatoRegion
        fields = ['id', 'name', 'code']


class KatoDistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = KatoDistrict
        fields = ['id', 'name', 'code']


class KatoCommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = KatoCommunity
        fields = ['id', 'name', 'code']


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ['id', 'name', 'alpha2', 'alpha3', 'name_official_eng', 'name_official_rus']


class CardTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardType
        fields = ['id', 'name']


class TariffPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = TariffPlan
        fields = ['id', 'name']