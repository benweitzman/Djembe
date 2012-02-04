from plugins.movies.models import *
from django.contrib import admin

admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Actor)
admin.site.register(MovieFormat)
admin.site.register(Edition)

