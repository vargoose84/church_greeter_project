from django.contrib import admin
from greeter.models import churchGoer, greeterID, greeterRecord, suggestion

class ChurchGoerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'occupation')
class greeterRecordAdmin(admin.ModelAdmin):
    list_display = ('trainerID','churchGoer','flag')
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'subject', 'greeterID')
admin.site.register(suggestion  ,SuggestionAdmin)
admin.site.register(churchGoer,ChurchGoerAdmin)
admin.site.register(greeterID)
admin.site.register(greeterRecord,greeterRecordAdmin)
# admin.site.register(churchGoer)
