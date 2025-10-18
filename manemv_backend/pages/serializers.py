# pages/serializers.py
from rest_framework import serializers
from .models import Page, ContentPage, Course, Module, Topic, ContentItem

class ContentPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentPage
        fields = ['id', 'title', 'description', 'created_at']

class PageSerializer(serializers.ModelSerializer):
    # This nests the serialized ContentPage data within the Page data.
    # 'content_pages' matches the related_name in the model's ForeignKey.
    content_pages = ContentPageSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'content', 'created_at', 'content_pages']

# --- Course Serializers ---

class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ['id', 'text_content', 'image', 'video_embed_url', 'order']

class TopicSerializer(serializers.ModelSerializer):
    content_items = ContentItemSerializer(many=True, read_only=True)
    class Meta:
        model = Topic
        fields = ['id', 'title', 'order', 'content_items']

class ModuleSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'topics']

class CourseSerializer(serializers.ModelSerializer):
    # For the list view, we don't need all the nested data
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description']

class CourseDetailSerializer(CourseSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['modules']
