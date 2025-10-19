from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost, Workshop, GalleryImage, Healer, Testimonial

class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'healing:home',
            'healing:about',
            'healing:workshops',
            'healing:healers',
            'healing:gallery',
            'healing:testimonials',
            'healing:blog',
            'healing:contact',
            'healing:events',
            'healing:meditation',
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        from django.utils import timezone
        return timezone.now()


class BlogPostSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(status='published', is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('healing:blog_detail', kwargs={'slug': obj.slug})


class WorkshopSitemap(Sitemap):
    """Sitemap for workshops"""
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Workshop.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('healing:workshop_detail', kwargs={'workshop_id': obj.pk})


class GallerySitemap(Sitemap):
    """Sitemap for gallery images"""
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return GalleryImage.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('healing:gallery')


class HealerSitemap(Sitemap):
    """Sitemap for healers"""
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Healer.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('healing:healers')


class TestimonialSitemap(Sitemap):
    """Sitemap for testimonials"""
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Testimonial.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('healing:testimonials')
