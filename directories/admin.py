from django.contrib import admin
from directories.models import *
# Register your models here.
admin.site.register(KatoRegion)
admin.site.register(KatoDistrict)
admin.site.register(KatoCommunity)
admin.site.register(Country)
admin.site.register(CardType)
admin.site.register(TariffPlan)
admin.site.register(OldCif)