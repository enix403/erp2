# from django.contrib import admin




# from django.apps import apps
# from django.contrib.admin.sites import AlreadyRegistered

# app_models = apps.get_app_config('salary').get_models()
# for model in app_models:
#     try:
#         admin.site.register(model)
#     except AlreadyRegistered:
#         pass


# from django.contrib.sessions.models import Session


# class SessionAdmin(admin.ModelAdmin):
#     def _session_data(self, obj):
#         return obj.get_decoded()
#     list_display = ['session_key', '_session_data', 'expire_date']


# admin.site.register(Session, SessionAdmin)
