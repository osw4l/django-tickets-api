from django.contrib import admin
from .models import Ticket, TicketImage


admin.site.site_header = 'Tickets Admin'
admin.site.site_title = 'Tickets Admin'
admin.site.index_title = 'Tickets'

 
class TicketImageStackedInline(admin.StackedInline):
    model = TicketImage
    extra = 0
    readonly_fields = [
        'status',
        'image'
    ]

    def has_add_permission(self, request, obj):
        return False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'user',
        'status',
        'total_images'
    ]
    readonly_fields = [
        'status',
    ]
    inlines = (
        TicketImageStackedInline,   
    )
    search_fields = [
        'uuid'
    ]
    list_filter = [
        'user__username',
        'status'
    ]

    def has_change_permission(self, request, obj=None):
        return True
    
    def has_add_permission(self, request):
        return False
    