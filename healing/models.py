from django.db import models
from django.utils import timezone


class WorkshopCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For Font Awesome icons
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Workshop Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Workshop(models.Model):
    category = models.ForeignKey(WorkshopCategory, on_delete=models.CASCADE, related_name='workshops')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50, blank=True)  # e.g., "2 days"
    duration_hours = models.IntegerField(default=16, help_text="Duration in hours for scheduling")
    image = models.ImageField(upload_to='workshops/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Healer(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='healers/', blank=True, null=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.profession}"


class CustomerFeedback(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    name = models.CharField(max_length=100, help_text="Your full name")
    email = models.EmailField(help_text="Your email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Your phone number (optional)")
    service_received = models.CharField(max_length=200, help_text="Service you received")
    rating = models.IntegerField(
        choices=[(i, f"{i} Star{'s' if i != 1 else ''}") for i in range(1, 6)],
        help_text="Rate your experience (1-5 stars)"
    )
    feedback = models.TextField(help_text="Share your experience with us")
    is_anonymous = models.BooleanField(default=False, help_text="Check to hide your name from public display")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Feedback"
        verbose_name_plural = "Customer Feedback"

    def __str__(self):
        display_name = "Anonymous" if self.is_anonymous else self.name
        return f"{display_name} - {self.rating} stars - {self.get_status_display()}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200, help_text="Blog post title")
    slug = models.SlugField(unique=True, help_text="URL-friendly version of the title")
    content = models.TextField(help_text="Main blog content")
    excerpt = models.TextField(max_length=500, blank=True, help_text="Short description for previews")
    image = models.ImageField(upload_to='blog/', blank=True, null=True, help_text="Main blog image")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True, help_text="Featured image for homepage")
    author = models.CharField(max_length=100, default="Pranic Healing USA")
    category = models.CharField(max_length=100, blank=True, help_text="Blog category (e.g., Healing, Meditation)")
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags (e.g., healing, meditation, energy)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', help_text="Publication status")
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    view_count = models.PositiveIntegerField(default=0, help_text="Number of views")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    @property
    def is_published(self):
        """Check if post is published"""
        return self.status == 'published'


class BlogComment(models.Model):
    """Blog post comments"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Comment"
        verbose_name_plural = "Blog Comments"
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"


class ContactInfo(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return "Contact Information"


class HealingSession(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    healing_type = models.CharField(max_length=100, help_text="Type of healing session")
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_reference = models.CharField(max_length=20, unique=True, blank=True, help_text="Unique booking reference")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.healing_type} on {self.preferred_date}"

    def save(self, *args, **kwargs):
        """Override save to generate booking reference"""
        if not self.booking_reference:
            import uuid
            self.booking_reference = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def session_datetime(self):
        """Return the session datetime"""
        from django.utils import timezone
        return timezone.datetime.combine(self.preferred_date, self.preferred_time)


class SiteContent(models.Model):
    CONTENT_TYPES = [
        ('hero_title', 'Hero Title'),
        ('hero_subtitle', 'Hero Subtitle'),
        ('about_title', 'About Title'),
        ('about_subtitle', 'About Subtitle'),
        ('about_content', 'About Content'),
        ('mission_statement', 'Mission Statement'),
        ('vision_statement', 'Vision Statement'),
    ]

    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES, unique=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['content_type']

    def __str__(self):
        return f"{self.get_content_type_display()}"


class ThemeSettings(models.Model):
    """Theme customization settings"""
    name = models.CharField(max_length=100, default="Pranic Healing Theme")
    is_active = models.BooleanField(default=True)
    
    # Logo and Branding
    logo = models.ImageField(upload_to='theme/', blank=True, null=True)
    favicon = models.ImageField(upload_to='theme/', blank=True, null=True)
    
    # Color Palette - Pranic Healing inspired colors
    primary_color = models.CharField(max_length=7, default='#2E8B57', help_text='Primary color (hex code) - Sea Green')
    secondary_color = models.CharField(max_length=7, default='#32CD32', help_text='Secondary color (hex code) - Lime Green')
    accent_color = models.CharField(max_length=7, default='#228B22', help_text='Accent color (hex code) - Forest Green')
    text_color = models.CharField(max_length=7, default='#2c2c2c', help_text='Text color (hex code)')
    background_color = models.CharField(max_length=7, default='#ffffff', help_text='Background color (hex code)')
    
    # Typography
    heading_font = models.CharField(max_length=100, default='Merriweather', help_text='Font family for headings')
    body_font = models.CharField(max_length=100, default='Open Sans', help_text='Font family for body text')
    
    # Layout Settings
    enable_gradients = models.BooleanField(default=True)
    enable_animations = models.BooleanField(default=True)
    enable_shadows = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Theme Settings"
        verbose_name_plural = "Theme Settings"

    def __str__(self):
        return self.name


class SiteImages(models.Model):
    """Manage site images"""
    IMAGE_TYPES = [
        ('hero_bg', 'Hero Background'),
        ('about_bg', 'About Background'),
        ('gallery_bg', 'Gallery Background'),
        ('testimonial_bg', 'Testimonial Background'),
        ('contact_bg', 'Contact Background'),
        ('default_workshop', 'Default Workshop Image'),
        ('default_healer', 'Default Healer Image'),
        ('default_testimonial', 'Default Testimonial Image'),
    ]
    
    name = models.CharField(max_length=100)
    image_type = models.CharField(max_length=50, choices=IMAGE_TYPES)
    image = models.ImageField(upload_to='site_images/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Site Image"
        verbose_name_plural = "Site Images"

    def __str__(self):
        return f"{self.name} - {self.get_image_type_display()}"


class WorkshopIcons(models.Model):
    """Manage workshop icons"""
    workshop_category = models.ForeignKey(WorkshopCategory, on_delete=models.CASCADE, related_name='icons')
    icon_class = models.CharField(max_length=100, help_text='Font Awesome icon class (e.g., fas fa-hands-healing)')
    icon_color = models.CharField(max_length=7, default='#2E8B57', help_text='Icon color (hex code)')
    background_color = models.CharField(max_length=7, default='#32CD32', help_text='Icon background color (hex code)')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Workshop Icon"
        verbose_name_plural = "Workshop Icons"

    def __str__(self):
        return f"{self.workshop_category.name} - {self.icon_class}"


class SiteSettings(models.Model):
    """General site settings"""
    site_name = models.CharField(max_length=100, default="Pranic Healing USA")
    site_tagline = models.CharField(max_length=200, default="Energy Healing & Spiritual Wellness")
    site_description = models.TextField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Contact Info
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Business Hours
    monday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    tuesday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    wednesday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    thursday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    friday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    saturday_hours = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    sunday_hours = models.CharField(max_length=50, default="10:00 AM - 6:00 PM")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name


class SEOSettings(models.Model):
    """SEO settings for the website"""
    PAGE_TYPES = [
        ('home', 'Home Page'),
        ('about', 'About Page'),
        ('workshops', 'Workshops Page'),
        ('gallery', 'Gallery Page'),
        ('healers', 'Healers Page'),
        ('testimonials', 'Testimonials Page'),
        ('blog', 'Blog Page'),
        ('contact', 'Contact Page'),
        ('healing_sessions', 'Healing Sessions Page'),
    ]
    
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, unique=True)
    page_title = models.CharField(max_length=60, help_text="Page title (max 60 characters)")
    meta_description = models.TextField(max_length=160, help_text="Meta description (max 160 characters)")
    meta_keywords = models.TextField(blank=True, help_text="Comma-separated keywords")
    h1_tag = models.CharField(max_length=100, blank=True, help_text="Main H1 heading")
    h2_tag = models.CharField(max_length=100, blank=True, help_text="Secondary H2 heading")
    canonical_url = models.URLField(blank=True, help_text="Canonical URL for this page")
    og_title = models.CharField(max_length=60, blank=True, help_text="Open Graph title")
    og_description = models.TextField(max_length=160, blank=True, help_text="Open Graph description")
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True, help_text="Open Graph image")
    twitter_title = models.CharField(max_length=60, blank=True, help_text="Twitter Card title")
    twitter_description = models.TextField(max_length=160, blank=True, help_text="Twitter Card description")
    twitter_image = models.ImageField(upload_to='seo/', blank=True, null=True, help_text="Twitter Card image")
    schema_markup = models.TextField(blank=True, help_text="JSON-LD structured data")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SEO Settings"
        verbose_name_plural = "SEO Settings"
        ordering = ['page_type']

    def __str__(self):
        return f"{self.get_page_type_display()} - {self.page_title}"


class GoogleAnalytics(models.Model):
    """Google Analytics and tracking settings"""
    tracking_id = models.CharField(max_length=20, blank=True, help_text="Google Analytics Tracking ID (e.g., GA-XXXXXXXXX)")
    gtag_id = models.CharField(max_length=20, blank=True, help_text="Google Analytics 4 Measurement ID (e.g., G-XXXXXXXXXX)")
    google_tag_manager_id = models.CharField(max_length=20, blank=True, help_text="Google Tag Manager ID (e.g., GTM-XXXXXXX)")
    facebook_pixel_id = models.CharField(max_length=20, blank=True, help_text="Facebook Pixel ID")
    google_ads_conversion_id = models.CharField(max_length=20, blank=True, help_text="Google Ads Conversion ID")
    custom_tracking_code = models.TextField(blank=True, help_text="Custom tracking code (head section)")
    custom_body_code = models.TextField(blank=True, help_text="Custom tracking code (body section)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Google Analytics"
        verbose_name_plural = "Google Analytics"

    def __str__(self):
        return f"Analytics - {self.tracking_id or self.gtag_id or 'Not Configured'}"


class SEOPageContent(models.Model):
    """Additional SEO content for specific pages"""
    page_type = models.CharField(max_length=20, choices=SEOSettings.PAGE_TYPES)
    content_section = models.CharField(max_length=50, help_text="Content section (e.g., 'hero_text', 'about_intro')")
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    image_alt_text = models.CharField(max_length=200, blank=True, help_text="Alt text for images")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SEO Page Content"
        verbose_name_plural = "SEO Page Content"
        unique_together = ['page_type', 'content_section']
        ordering = ['page_type', 'content_section']

    def __str__(self):
        return f"{self.get_page_type_display()} - {self.content_section}"


class BusinessHours(models.Model):
    """Business hours configuration for different days"""
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)
    is_open = models.BooleanField(default=True)
    open_time = models.TimeField(help_text="Opening time (e.g., 10:00)")
    close_time = models.TimeField(help_text="Closing time (e.g., 19:00)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business Hours"
        verbose_name_plural = "Business Hours"
        ordering = ['day_of_week']

    def __str__(self):
        status = "Open" if self.is_open else "Closed"
        return f"{self.get_day_of_week_display()} - {status} ({self.open_time} - {self.close_time})"


class ContactMessage(models.Model):
    """Model to store contact form messages"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"


class Event(models.Model):
    """Events and workshops calendar"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date', 'start_time']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{self.title} - {self.event_date}"

    @property
    def event_datetime(self):
        """Return the event datetime"""
        from django.utils import timezone
        return timezone.datetime.combine(self.event_date, self.start_time)
