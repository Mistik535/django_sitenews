from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import News, Category


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'tags']
    # exclude = ['tags', 'is_published']
    readonly_fields = ['post_photo']
    prepopulated_fields = {"slug": ("title", )}
    # filter_horizontal = ['tags']
    filter_vertical = ['tags']
    list_display = ('title', 'post_photo', 'time_created', 'is_published', 'cat')
    list_display_links = ('title', )
    ordering = ('-time_created', 'title')
    list_editable = ('is_published', )
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name']
    save_on_top = True

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, news: News):
        if news.photo:
            return mark_safe(f"<img src='{news.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные посты")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=News.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} постов.")

    @admin.action(description="Снять с публикации выбранные посты")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=News.Status.DRAFT)
        self.message_user(request, f"{count} постов снято с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

