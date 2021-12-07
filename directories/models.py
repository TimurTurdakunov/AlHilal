from django.db import models


class KatoRegion(models.Model):

    name = models.CharField(max_length=255)
    code = models.IntegerField()

    def __str__(self):
        return self.name


class KatoDistrict(models.Model):

    name = models.CharField(max_length=255)
    code = models.IntegerField()
    region = models.ForeignKey('KatoRegion', models.CASCADE)

    def __str__(self):
        return self.name


class KatoCommunity(models.Model):

    name = models.CharField(max_length=255)
    code = models.IntegerField()
    district = models.ForeignKey('KatoDistrict', models.CASCADE)

    def __str__(self):
        return self.name


class Country(models.Model):

    name = models.CharField(max_length=255)
    alpha2 = models.CharField(max_length=2)
    alpha3 = models.CharField(max_length=3)
    name_official_eng = models.CharField(max_length=255)
    name_official_rus = models.CharField(max_length=255)


class CardType(models.Model):

    name = models.CharField(max_length=255)


class TariffPlan(models.Model):

    name = models.CharField(max_length=255)


class OldCif(models.Model):

    cif = models.CharField(max_length=50)
