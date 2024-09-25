from django.contrib import admin
from django.utils.safestring import mark_safe

from core.constans import FIELD_TO_EDIT
from recipes.formsets import (
    TagRecipeInlineFormSet, IngredientRecipeAmountInlineFormSet,
    ShoppingCartForm, FavoriteRecipeForm)
from recipes.models import (
    Tag,
    Recipe,
    ShortLink,
    FavoriteRecipe,
    Ingredient,
    ShoppingCart,
    IngredientRecipeAmountModel,
    TagRecipe
)


class TagAdmin(admin.ModelAdmin):
    """
    Панель редактирования тегов.
    """
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    """
    Панель редактирования ингредиентов.
    """
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    ordering = ('name',)


class IngredientRecipeAmountInline(admin.TabularInline):
    """
    Инлайн-класс для редактирования ингредиентов рецепта.
    """
    model = IngredientRecipeAmountModel
    extra = FIELD_TO_EDIT
    formset = IngredientRecipeAmountInlineFormSet


class TagRecipeInline(admin.TabularInline):
    """
    Инлайн-класс для редактирования тегов рецепта.
    """
    model = TagRecipe
    extra = FIELD_TO_EDIT
    formset = TagRecipeInlineFormSet


class RecipeAdmin(admin.ModelAdmin):
    """
    Панель редактирования рецептов.
    Включаен инлайн-классы для гибкой настройки.
    """
    list_display = (
        'id', 'name', 'author_username', 'image_tag'
    )
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = ('tags',)
    ordering = ('-id',)
    inlines = [IngredientRecipeAmountInline, TagRecipeInline]
    filter_horizontal = ('tags',)

    def author_username(self, obj):
        return obj.author.username

    def favorites_count(self, obj):
        return obj.favorites.count()

    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" width="150"'
                             'height="100" />'.format(obj.image.url))
        return None

    class Meta:
        model = Recipe


class ShortLinkAdmin(admin.ModelAdmin):
    """
    Панель коротких ссылок.
    """
    list_display = ('recipe', 'link')
    search_fields = ('recipe__name', 'link',)


class ShoppingCartAdmin(admin.ModelAdmin):
    """
    Панель корзины.
    """
    list_display = ('id', 'user', 'recipe')

    def get_form(self, request, obj=None, **kwargs):
        super().get_form(request, obj, **kwargs)
        return ShoppingCartForm


class FavoriteRecipeAdmin(admin.ModelAdmin):
    """
    Панель избранного.
    """
    list_display = ('id', 'user', 'recipe')

    def get_form(self, request, obj=None, **kwargs):
        super().get_form(request, obj, **kwargs)
        return FavoriteRecipeForm


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShortLink, ShortLinkAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
