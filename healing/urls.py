from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import StaticViewSitemap, BlogPostSitemap, WorkshopSitemap, GallerySitemap, HealerSitemap, TestimonialSitemap
from .robots_views import robots_txt

app_name = 'healing'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('workshops/', views.workshops, name='workshops'),
    path('workshop/<int:workshop_id>/', views.workshop_detail, name='workshop_detail'),
    path('healers/', views.healers, name='healers'),
    path('gallery/', views.gallery, name='gallery'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('book-healing-session/', views.book_healing_session, name='book_healing_session'),
    path('events/', views.events, name='events'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('meditation/', views.meditation, name='meditation'),
    path('dynamic-theme.css', views.dynamic_theme_css, name='dynamic_theme_css'),
    
    # SEO URLs
    path('sitemap.xml', sitemap, {
        'sitemaps': {
            'static': StaticViewSitemap,
            'blog': BlogPostSitemap,
            'workshops': WorkshopSitemap,
            'gallery': GallerySitemap,
            'healers': HealerSitemap,
            'testimonials': TestimonialSitemap,
        }
    }, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
]
