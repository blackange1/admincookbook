from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db.models import Count

from .models import Category, Hero, Origin, Villain


# show calculated fields on listview page
@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("name", "hero_count", "villain_count")

    # optimize queries in Django admin
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _hero_count=Count("hero", distinct=True),
            _villain_count=Count("villain", distinct=True),
        )
        return queryset

    # show calculated fields on listview page
    def hero_count(self, obj):
        return obj.hero_set.count()

    def villain_count(self, obj):
        return obj.villain_set.count()

    # enable sorting on calculated fields
    hero_count.admin_order_field = '_hero_count'
    villain_count.admin_order_field = '_villain_count'


# enable filtering on calculated fields
class IsVeryBenevolentFilter(admin.SimpleListFilter):
    title = 'is_very_benevolent'
    parameter_name = 'is_very_benevolent'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(benevolence_factor__gt=75)
        elif value == 'No':
            return queryset.exclude(benevolence_factor__gt=75)
        return queryset


# enable filtering on calculated fields
@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ("name", "is_immortal", "category", "origin", "is_very_benevolent")
    list_filter = ("is_immortal", "category", "origin", IsVeryBenevolentFilter)

    def is_very_benevolent(self, obj):
        return obj.benevolence_factor > 75

    # show “on” or “off” icons for calculated boolean fields?
    is_very_benevolent.boolean = True

    # add additional actions in Django admin
    actions = ["mark_immortal"]

    def mark_immortal(self, request, queryset):
        queryset.update(is_immortal=True)


admin.site.register(Category)
admin.site.register(Villain)

# remove default apps from Django admin
admin.site.unregister(User)
admin.site.unregister(Group)
