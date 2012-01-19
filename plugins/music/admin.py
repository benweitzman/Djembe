from plugins.music.models import *
from django.contrib import admin
#from ajax_select import make_ajax_form
#from ajax_select.admin import AjaxSelectAdmin
admin.site.register(AlbumFormat)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Release)
admin.site.register(Label)
admin.site.register(TagCount)
