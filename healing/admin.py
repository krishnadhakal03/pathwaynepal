from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from .models import (
    WorkshopCategory, Workshop, Healer, Testimonial, CustomerFeedback,
    GalleryImage, BlogPost, BlogComment, ContactInfo, HealingSession,
    SiteContent, ThemeSettings, SiteImages, WorkshopIcons, SiteSettings,
    SEOSettings, GoogleAnalytics, SEOPageContent, BusinessHours,
    ContactMessage, Event
)


class CustomAdminSite(AdminSite):
    site_header = "Pranic Healing USA Administration"
    site_title = "Pranic Healing Admin"
    index_title = "Welcome to Pranic Healing USA Administration"
    site_url = "/"


# Create custom admin site instance
admin_site = CustomAdminSite(name='custom_admin')


@admin.register(WorkshopCategory, site=admin_site)
class WorkshopCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['name']


@admin.register(Workshop, site=admin_site)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    list_editable = ['is_featured', 'is_active']
    ordering = ['category', 'name']
    raw_id_fields = ['category']


@admin.register(Healer, site=admin_site)
class HealerAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'specialization', 'is_active', 'created_at']
    list_filter = ['is_active', 'position', 'created_at']
    search_fields = ['name', 'position', 'specialization', 'bio']
    list_editable = ['is_active']
    ordering = ['name']


@admin.register(Testimonial, site=admin_site)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'profession', 'rating', 'is_featured', 'is_active', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['client_name', 'profession', 'content']
    list_editable = ['is_featured', 'is_active']
    ordering = ['-created_at']


@admin.register(CustomerFeedback, site=admin_site)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_received', 'rating', 'status', 'is_featured', 'created_at']
    list_filter = ['rating', 'status', 'is_featured', 'is_anonymous', 'created_at']
    search_fields = ['name', 'email', 'service_received', 'feedback']
    list_editable = ['status', 'is_featured']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GalleryImage, site=admin_site)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'is_active']
    ordering = ['-created_at']


@admin.register(BlogPost, site=admin_site)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'view_count', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'content', 'author', 'category', 'tags']
    list_editable = ['status', 'is_featured']
    ordering = ['-created_at']
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(BlogComment, site=admin_site)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'comment', 'post__title']
    list_editable = ['is_approved']
    ordering = ['-created_at']
    raw_id_fields = ['post']


@admin.register(ContactInfo, site=admin_site)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['phone', 'email', 'address']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(HealingSession, site=admin_site)
class HealingSessionAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'healing_type', 'preferred_date', 'preferred_time', 'status', 'booking_reference', 'created_at']
    list_filter = ['status', 'healing_type', 'preferred_date', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'booking_reference', 'healing_type']
    list_editable = ['status']
    ordering = ['-created_at']
    readonly_fields = ['booking_reference', 'created_at', 'updated_at']
    date_hierarchy = 'preferred_date'
    fieldsets = (
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Session Details', {
            'fields': ('healing_type', 'preferred_date', 'preferred_time')
        }),
        ('Status & Reference', {
            'fields': ('status', 'booking_reference')
        }),
        ('Additional Information', {
            'fields': ('message',)
        }),
    )


@admin.register(Event, site=admin_site)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'start_time', 'end_time', 'location', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_featured', 'is_active', 'event_date', 'created_at']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_featured', 'is_active']
    ordering = ['event_date', 'start_time']
    date_hierarchy = 'event_date'


@admin.register(SiteContent, site=admin_site)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'title', 'is_active', 'updated_at']
    list_filter = ['content_type', 'is_active', 'created_at', 'updated_at']
    search_fields = ['content_type', 'title', 'content']
    list_editable = ['is_active']
    ordering = ['content_type']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ThemeSettings, site=admin_site)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'primary_color', 'secondary_color', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Settings', {
            'fields': ('name', 'is_active')
        }),
        ('Logo & Branding', {
            'fields': ('logo', 'favicon')
        }),
        ('Color Palette', {
            'fields': ('primary_color', 'secondary_color', 'accent_color', 'text_color', 'background_color')
        }),
        ('Typography', {
            'fields': ('heading_font', 'body_font')
        }),
        ('Layout Settings', {
            'fields': ('enable_gradients', 'enable_animations', 'enable_shadows')
        }),
    )


@admin.register(SiteImages, site=admin_site)
class SiteImagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_type', 'is_active', 'created_at']
    list_filter = ['image_type', 'is_active', 'created_at']
    search_fields = ['name', 'alt_text']
    list_editable = ['is_active']
    ordering = ['image_type', 'name']


@admin.register(WorkshopIcons, site=admin_site)
class WorkshopIconsAdmin(admin.ModelAdmin):
    list_display = ['workshop_category', 'icon_class', 'icon_color', 'is_active', 'created_at']
    list_filter = ['is_active', 'workshop_category', 'created_at']
    search_fields = ['workshop_category__name', 'icon_class']
    list_editable = ['is_active']
    ordering = ['workshop_category', 'icon_class']
    raw_id_fields = ['workshop_category']


@admin.register(SiteSettings, site=admin_site)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_tagline', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['site_name', 'site_tagline', 'site_description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_tagline', 'site_description', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url')
        }),
        ('Business Hours', {
            'fields': ('monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours', 
                      'friday_hours', 'saturday_hours', 'sunday_hours')
        }),
    )


@admin.register(SEOSettings, site=admin_site)
class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ['page_type', 'page_title', 'meta_description', 'is_active', 'updated_at']
    list_filter = ['page_type', 'is_active', 'created_at', 'updated_at']
    search_fields = ['page_title', 'meta_description', 'meta_keywords', 'h1_tag']
    list_editable = ['is_active']
    ordering = ['page_type']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic SEO', {
            'fields': ('page_type', 'page_title', 'meta_description', 'meta_keywords', 'is_active')
        }),
        ('Headings', {
            'fields': ('h1_tag', 'h2_tag')
        }),
        ('URLs & Canonical', {
            'fields': ('canonical_url',)
        }),
        ('Open Graph (Facebook)', {
            'fields': ('og_title', 'og_description', 'og_image')
        }),
        ('Twitter Cards', {
            'fields': ('twitter_title', 'twitter_description', 'twitter_image')
        }),
        ('Structured Data', {
            'fields': ('schema_markup',)
        }),
    )


@admin.register(GoogleAnalytics, site=admin_site)
class GoogleAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'gtag_id', 'google_tag_manager_id', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['tracking_id', 'gtag_id', 'google_tag_manager_id', 'facebook_pixel_id']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Google Analytics', {
            'fields': ('tracking_id', 'gtag_id', 'is_active')
        }),
        ('Google Tag Manager', {
            'fields': ('google_tag_manager_id',)
        }),
        ('Social Media Tracking', {
            'fields': ('facebook_pixel_id',)
        }),
        ('Google Ads', {
            'fields': ('google_ads_conversion_id',)
        }),
        ('Custom Tracking Code', {
            'fields': ('custom_tracking_code', 'custom_body_code')
        }),
    )


@admin.register(SEOPageContent, site=admin_site)
class SEOPageContentAdmin(admin.ModelAdmin):
    list_display = ['page_type', 'content_section', 'title', 'is_active', 'updated_at']
    list_filter = ['page_type', 'is_active', 'created_at', 'updated_at']
    search_fields = ['page_type', 'content_section', 'title', 'content']
    list_editable = ['is_active']
    ordering = ['page_type', 'content_section']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Content Information', {
            'fields': ('page_type', 'content_section', 'title', 'is_active')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Image SEO', {
            'fields': ('image_alt_text',)
        }),
    )


@admin.register(BusinessHours, site=admin_site)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ['day_of_week', 'is_open', 'open_time', 'close_time', 'is_active', 'updated_at']
    list_filter = ['is_open', 'is_active', 'day_of_week']
    search_fields = ['day_of_week']
    list_editable = ['is_open', 'open_time', 'close_time', 'is_active']
    ordering = ['day_of_week']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Day Configuration', {
            'fields': ('day_of_week', 'is_open', 'is_active')
        }),
        ('Hours', {
            'fields': ('open_time', 'close_time')
        }),
    )


@admin.register(ContactMessage, site=admin_site)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'subject']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['status']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Status & Timestamps', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )


# Custom admin URLs
admin_urlpatterns = [
    path('admin/', admin_site.urls),
    path('admin', lambda request: redirect('/admin/')),
]
