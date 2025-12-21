# backend/ops/admin.py
from django.contrib import admin

from ops import models

from ops.utils.dt import format_dt_jst



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name")



@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")



@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "pack_g")



@admin.register(models.DepartmentItemAssignment)
class DepartmentItemAssignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "department", "item")



@admin.register(models.DepartmentItemAssignmentComponent)
class DepartmentItemAssignmentComponentAdmin(admin.ModelAdmin):
    list_display = ("id", "parent_department_item_assignment", "child_department_item_assignment", "child_units_per_parent_unit")



@admin.register(models.OrderHeader)
class OrderHeaderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "ordered_at_local", "pickup_at_local")

    def ordered_at_local(self, obj):
        return format_dt_jst(obj.ordered_at)

    def pickup_at_local(self, obj):
        return format_dt_jst(obj.pickup_at)



@admin.register(models.OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ("id", "order_header", "product_item", "quantity_units")



@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display =\
    (
        "id",
        "assignment",
        "pickup_at_local",
        "required_units",
        "started_at_local",
        "finished_at_local",
    )

    def pickup_at_local(self, obj):
        return format_dt_jst(obj.pickup_at)

    def started_at_local(self, obj):
        return "-" if obj.started_at is None else format_dt_jst(obj.started_at)

    def finished_at_local(self, obj):
        return "-" if obj.finished_at is None else format_dt_jst(obj.finished_at)



@admin.register(models.TaskPlan)
class TaskPlanAdmin(admin.ModelAdmin):
    list_display =\
    (
        "id",
        "task",
        "planned_started_at",
        "planned_finished_at",
        "is_feasible",
    )
