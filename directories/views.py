from django.shortcuts import render
from django.core import serializers
from rest_framework.response import Response
from directories.models import *
from directories.serializers import *
from rest_framework.views import APIView
from directories.services import services


class KatoRegionsView(APIView):

    def get(self, pk):
        queryset = KatoRegion.objects.filter(region=pk)
        serializer = KatoRegionSerializer(queryset, many=True)
        return Response(serializer.data)


class KatoDistrictView(APIView):

    def get(self, pk):
        queryset = KatoDistrict.objects.filter(region=pk)
        serializer = KatoDistrictSerializer(queryset, many=True)
        return Response(serializer.data)


class KatoCommunityView(APIView):

    def get(self, pk):
        queryset = KatoCommunity.objects.filter(region=pk)
        serializer = KatoCommunitySerializer(queryset, many=True)
        return Response(serializer.data)


class CountryView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Country.objects.all()
        serializer = CountrySerializer(queryset, many=True)
        return Response(serializer.data)


class CardTypeView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = CardType.objects.all()
        serializer = CardTypeSerializer(queryset, many=True)
        return Response(serializer.data)


class TariffPlanView(APIView):

    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = TariffPlan.objects.all()
        serializer = TariffPlanSerializer(queryset, many=True)
        return Response(serializer.data)


