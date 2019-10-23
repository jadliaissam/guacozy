from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_admin_listfilter_dropdown.filters import DropdownFilter
from rules.contrib.admin import ObjectPermissionsModelAdmin

from backend.models import TicketLog, Connection
from users.models import User


@admin.register(TicketLog)
class TicketLogAdmin(ObjectPermissionsModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def uri(self, obj):
        return "{}://{}:{}".format(obj.connection_protocol, obj.connection_host, obj.connection_port)

    def connection_link(self, obj):
        try:
            link = reverse("admin:backend_connection_change", args=[obj.connection.id])
            return format_html('<a href="{}">{}</a>', link, obj.connection.name)
        except Connection.DoesNotExist:
            return format_html("<strike>{}</strike>", obj.connection_name)

    connection_link.short_description = "Connection"

    def user_link(self, obj):
        try:
            link = reverse("admin:users_user_change", args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', link, obj.user.username)
        except User.DoesNotExist:
            return format_html("<strike>{}</strike>", obj.username)

    user_link.short_description = "User"

    def author_link(self, obj):
        try:
            link = reverse("admin:users_user_change", args=[obj.author.id])
            return format_html(
                '<a href="{}">{}</a>',
                link,
                obj.author.username if obj.author_username != obj.username else "self")
        except User.DoesNotExist:
            return format_html(
                "<strike>{}</strike>",
                obj.author_username if obj.author_username != obj.username else "self")

    author_link.short_description = "Author"

    def ticketid_short(self, obj):
        shortid = obj.ticketid.__str__()[0:8]
        return format_html('<a href="{}">{}</a>', "?q=" + shortid, shortid)

    ticketid_short.short_description = "Ticket"

    def sessionid_short(self, obj):
        shortid = obj.sessionid.__str__()[0:8]
        return format_html('<a href="{}">{}</a>', "?q=" + shortid, shortid)

    sessionid_short.short_description = "Session"

    # list_display = [field.name for field in TicketLog._meta.get_fields()]
    list_display = [
        'id',
        'date',
        'action',
        'user_link',
        'author_link',
        'connection_link',
        'uri',
        'ticketid_short',
        'sessionid_short',
        'shared',
    ]

    list_filter = (
        'action',
        ('username', DropdownFilter),
        ('author_username', DropdownFilter),
        ('connection_name', DropdownFilter),
        ('shared', admin.BooleanFieldListFilter),
    )

    search_fields = ['username', 'full_name',
                     'author_username', 'author_full_name',
                     'connection_name', 'connection_host',
                     'ticketid', 'sessionid'
                     ]
    readonly_fields = [field.name for field in TicketLog._meta.get_fields()]