from django.contrib import admin

from billogram.discountservice import models


@admin.register(models.DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DiscountRule)
class DiscountRuleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DiscountCodeUsage)
class DiscountCodeUsageAdmin(admin.ModelAdmin):
    readonly_fields = ['id']


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass
