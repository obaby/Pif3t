from django.contrib import admin

# Register your models here.
from .models import *


# Register your models here.

class IFTTTTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'create', 'id', 'describe', 'type_id')


class ThatActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'create', 'id', 'describe', 'action_type','http_url')


class IfThisAdmin(admin.ModelAdmin):
    list_display = ('name','if_type', 'parent', 'create', 'id', 'describe', 'condition_type', 'key_words', 'no_action_response_text')


admin.site.register(IFTTTType, IFTTTTypeAdmin)
admin.site.register(ThatAction, ThatActionAdmin)
admin.site.register(IfThis, IfThisAdmin)

admin.site.site_title = "Pif3t 管理后台"
admin.site.site_header = "Pif3t 管理后台"
