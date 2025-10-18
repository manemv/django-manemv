from django.contrib import admin
from .models import Page, ContentPage, Course, Module, Topic, ContentItem
import nested_admin

# This allows us to edit ContentPage items directly within the Page admin
class ContentPageInline(admin.TabularInline):
    model = ContentPage
    extra = 1 # Provides one extra blank form for new content

# Define a custom admin class for the Page model
class PageAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'slug', 'created_at')
    # Fields to search by
    search_fields = ('title', 'content',)
    # Automatically populate the slug field from the title field in the admin form
    prepopulated_fields = {'slug': ('title',)}
    # Add the inline editor for ContentPage
    inlines = [ContentPageInline]

# Register your models here.
admin.site.register(Page, PageAdmin)
# It's also good practice to register the ContentPage model directly
admin.site.register(ContentPage)

# --- Course Admin Configuration ---

class ContentItemInline(nested_admin.NestedTabularInline):
    model = ContentItem
    extra = 1

class TopicInline(nested_admin.NestedStackedInline):
    model = Topic
    extra = 1
    inlines = [ContentItemInline]

class ModuleInline(nested_admin.NestedStackedInline):
    model = Module
    extra = 1
    inlines = [TopicInline]

@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

# Registering other models to be visible, though they are best managed via inlines
admin.site.register(Module, nested_admin.NestedModelAdmin)
admin.site.register(Topic, nested_admin.NestedModelAdmin)
admin.site.register(ContentItem, nested_admin.NestedModelAdmin)
