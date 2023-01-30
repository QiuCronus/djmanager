from django.contrib import admin

admin.site.site_header = 'IM管理后台'
admin.site.site_title = 'IM管理后台'
admin.site.index_title = 'IM管理后台'

from dashboards.models import Node


@admin.action(description="激活节点")
def enable_nodes(model, request, queryset):
    queryset.update(enabled=Node.VALID)


@admin.action(description="禁用节点")
def disable_selected_nodes(model, request, queryset):
    queryset.update(enabled=Node.BAN)


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = [
        "category", "domain", "hostname", "label",
        "cpu", "disk", "memory", "alive_account_count", "pending_task_count",
        "enabled", "updated_at"
    ]
    list_display_links = ["hostname", "label", ]

    fields = (
        "category", "domain",
        "hostname", "label",
        "cpu", "disk", "memory",
        "alive_account_count", "pending_task_count",
        "accounts", "tasks", "updated_ts",
        "enabled",
    )

    readonly_fields = [
        "category", "domain", "hostname", "label",
        "accounts", "tasks", "updated_ts",
    ]

    list_filter = [
        "category", "domain", "label", "enabled"
    ]

    search_fields = ["hostname", "label", "enabled"]

    actions = [
        enable_nodes,
        disable_selected_nodes
    ]
