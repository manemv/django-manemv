# pages/models.py
from django.db import models
from django.utils.text import slugify

class Page(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if it's not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ContentPage(models.Model):
    page = models.ForeignKey(Page, related_name='content_pages', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order content pages by their creation date by default
        ordering = ['created_at']

    def __str__(self):
        return self.title


# --- Course Structure Models ---

class Course(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(help_text="A brief summary of the course.")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0, help_text="Order in which the module appears.")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Topic(models.Model):
    module = models.ForeignKey(Module, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0, help_text="Order in which the topic appears.")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class ContentItem(models.Model):
    topic = models.ForeignKey(Topic, related_name='content_items', on_delete=models.CASCADE, null=True) # Temporarily allow null
    text_content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    video_embed_url = models.URLField(blank=True, null=True, help_text="URL for embedding video (e.g., from YouTube, Vimeo).")
    order = models.PositiveIntegerField(default=0, help_text="Order of content within the topic.")

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Content Items"

    def __str__(self):
        # Provide a helpful representation for the admin.
        if self.topic:
            return f"Content for '{self.topic.title}' (Order: {self.order})"
        return f"Content Item (Unassigned, Order: {self.order})"
