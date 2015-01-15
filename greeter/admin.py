from django.contrib import admin
from greeter.models import churchGoer, greeterID, greeterRecord

class ChurchGoerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'occupation')
class greeterRecordAdmin(admin.ModelAdmin):
    list_display = ('trainerid','churchGoer','flag')

admin.site.register(churchGoer,ChurchGoerAdmin)
admin.site.register(greeterID)
admin.site.register(greeterRecord,greeterRecordAdmin)
# admin.site.register(churchGoer)
