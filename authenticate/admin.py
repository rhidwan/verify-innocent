from django.contrib import admin

# the module name is app_name.models
from .models import Authentication, BlacklistIP

@admin.register(Authentication)
class AuthenticationAdmin(admin.ModelAdmin):
    list_display = ('product', 'authenticated', 'authentication_time', 'ip_address' )
    empty_value_display = '-'

    def product(self, obj):
        return obj.unique_str
    
    def authentication_time(self, obj):
        return obj.hit_count


@admin.register(BlacklistIP)
class BlacklistIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'request_count', 'blocked')

    def request_count(self, obj):
        return obj.hit_count