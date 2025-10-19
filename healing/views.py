from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import redirect
from datetime import datetime, timedelta
import json

from .models import (
    WorkshopCategory, Workshop, Healer, Testimonial, 
    GalleryImage, BlogPost, ContactInfo, HealingSession, SiteContent, ContactMessage, Event
)


def home(request):
    """Home page view"""
    # Get featured workshops
    featured_workshops = Workshop.objects.filter(is_featured=True, is_active=True)[:6]
    
    # Get all workshop categories for navigation
    workshop_categories = WorkshopCategory.objects.filter(is_active=True)
    
    # Get testimonials
    testimonials = Testimonial.objects.filter(
        is_active=True,
        content__isnull=False
    ).exclude(content__exact='')[:4]
    
    # Get customer feedback
    customer_feedback = Testimonial.objects.filter(
        is_active=True, 
        is_featured=True,
        content__isnull=False
    ).exclude(content__exact='')[:4]
    
    # Get healers
    healers = Healer.objects.filter(is_active=True)[:4]
    
    # Get gallery images
    gallery_images = GalleryImage.objects.filter(is_active=True)[:6]
    
    # Get blog posts
    blog_posts = BlogPost.objects.filter(status='published')[:2]
    
    # Get upcoming events
    upcoming_events = Event.objects.filter(
        is_active=True,
        event_date__gte=timezone.now().date()
    ).order_by('event_date')[:3]
    
    # Get site content
    site_content = {}
    for content in SiteContent.objects.filter(is_active=True):
        site_content[content.content_type] = content
    
    # Get contact info
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    # Handle feedback form submission
    if request.method == 'POST' and 'feedback_submit' in request.POST:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        service_received = request.POST.get('service_received', '').strip()
        rating = request.POST.get('rating', '5')
        feedback_text = request.POST.get('feedback', '').strip()
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        # Validate required fields
        if not name or not email or not service_received or not feedback_text:
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                # Create new testimonial
                testimonial = Testimonial.objects.create(
                    client_name='Anonymous' if is_anonymous else name,
                    profession=service_received,
                    content=feedback_text,
                    rating=int(rating),
                    is_active=True,
                    is_featured=True
                )
                messages.success(request, 'Thank you for your feedback! Your review has been added.')
                return redirect('healing:home')
            except Exception as e:
                messages.error(request, 'There was an error submitting your feedback. Please try again.')
    
    # Create form data for template
    feedback_form_data = {
        'name': request.POST.get('name', '') if request.method == 'POST' else '',
        'email': request.POST.get('email', '') if request.method == 'POST' else '',
        'service_received': request.POST.get('service_received', '') if request.method == 'POST' else '',
        'rating': request.POST.get('rating', '5') if request.method == 'POST' else '5',
        'feedback': request.POST.get('feedback', '') if request.method == 'POST' else '',
        'is_anonymous': request.POST.get('is_anonymous') == 'on' if request.method == 'POST' else False,
    }
    
    context = {
        'featured_workshops': featured_workshops,
        'workshop_categories': workshop_categories,
        'testimonials': testimonials,
        'customer_feedback': customer_feedback,
        'feedback_form_data': feedback_form_data,
        'healers': healers,
        'gallery_images': gallery_images,
        'blog_posts': blog_posts,
        'upcoming_events': upcoming_events,
        'site_content': site_content,
        'contact_info': contact_info,
    }
    
    return render(request, 'healing/home.html', context)


def about(request):
    """About page view"""
    healers = Healer.objects.filter(is_active=True)
    site_content = {}
    for content in SiteContent.objects.filter(is_active=True):
        site_content[content.content_type] = content
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'healers': healers,
        'site_content': site_content,
        'contact_info': contact_info,
    }
    
    return render(request, 'healing/about.html', context)


def workshops(request):
    """Workshops page view"""
    workshop_categories = WorkshopCategory.objects.filter(is_active=True).prefetch_related('workshops')
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'workshop_categories': workshop_categories,
        'contact_info': contact_info,
    }
    
    return render(request, 'healing/workshops.html', context)


def workshop_detail(request, workshop_id):
    """Individual workshop detail view"""
    workshop = get_object_or_404(Workshop, id=workshop_id, is_active=True)
    related_workshops = Workshop.objects.filter(
        category=workshop.category, 
        is_active=True
    ).exclude(id=workshop.id)[:3]
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'workshop': workshop,
        'related_workshops': related_workshops,
        'contact_info': contact_info,
    }
    
    return render(request, 'healing/workshop_detail.html', context)


def healers(request):
    """Healers page view"""
    healers = Healer.objects.filter(is_active=True)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'healers': healers,
        'contact_info': contact_info,
    }
    
    return render(request, 'healing/healers.html', context)


def gallery(request):
    """Gallery page view"""
    # Get category filter from URL
    category_filter = request.GET.get('category', 'all')
    
    # Get all active gallery images
    gallery_images = GalleryImage.objects.filter(is_active=True)
    
    # Apply category filter if not 'all'
    if category_filter != 'all':
        # Map URL categories to search terms
        category_mapping = {
            'healing-sessions': ['healing', 'session', 'therapy'],
            'workshops': ['workshop', 'training', 'class'],
            'meditation': ['meditation', 'meditate', 'mindfulness'],
            'events': ['event', 'gathering', 'meeting'],
            'testimonials': ['testimonial', 'review', 'feedback'],
        }
        
        search_terms = category_mapping.get(category_filter, [])
        if search_terms:
            # Filter by title or description containing any of the search terms
            from django.db.models import Q
            query = Q()
            for term in search_terms:
                query |= Q(title__icontains=term) | Q(description__icontains=term)
            gallery_images = gallery_images.filter(query)
    
    # Pagination
    paginator = Paginator(gallery_images, 12)  # 12 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'page_obj': page_obj,
        'gallery_images': page_obj,
        'contact_info': contact_info,
        'current_category': category_filter,
    }
    
    return render(request, 'healing/gallery.html', context)


def testimonials(request):
    """Testimonials page view"""
    testimonials = Testimonial.objects.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(testimonials, 6)  # 6 testimonials per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'page_obj': page_obj,
        'testimonials': page_obj,
        'contact_info': contact_info,
    }
    
    return render(request, 'healing/testimonials.html', context)


def blog(request):
    """Blog page view"""
    blog_posts = BlogPost.objects.filter(status='published')
    
    # Pagination
    paginator = Paginator(blog_posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'page_obj': page_obj,
        'blog_posts': page_obj,
        'contact_info': contact_info,
    }
    
    return render(request, 'healing/blog.html', context)


def blog_detail(request, slug):
    """Individual blog post detail view"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    # Increment view count
    post.view_count += 1
    post.save(update_fields=['view_count'])
    
    # Handle comment submission
    if request.method == 'POST':
        from .models import BlogComment
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_text = request.POST.get('comment')
        
        if name and email and comment_text:
            BlogComment.objects.create(
                post=post,
                name=name,
                email=email,
                comment=comment_text
            )
            messages.success(request, 'Your comment has been submitted and will be reviewed.')
            return redirect('healing:blog_detail', slug=slug)
    
    # Get approved comments
    comments = post.comments.filter(is_approved=True)
    
    recent_posts = BlogPost.objects.filter(
        status='published'
    ).exclude(id=post.id)[:3]
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'post': post,
        'comments': comments,
        'recent_posts': recent_posts,
        'contact_info': contact_info,
    }
    
    return render(request, 'healing/blog_detail.html', context)


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create contact message
            contact_message = ContactMessage.objects.create(
                name=data.get('name', ''),
                email=data.get('email', ''),
                phone=data.get('phone', ''),
                subject=data.get('subject', ''),
                message=data.get('message', ''),
                status='new'
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Message sent successfully! We will get back to you soon.',
                'message_id': contact_message.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    # Get contact info and workshop categories
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    workshop_categories = WorkshopCategory.objects.filter(is_active=True).prefetch_related('workshops')
    
    context = {
        'contact_info': contact_info,
        'workshop_categories': workshop_categories,
    }
    
    return render(request, 'healing/contact.html', context)


def book_healing_session(request):
    """Healing session booking page"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create healing session
            healing_session = HealingSession.objects.create(
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                email=data.get('email', ''),
                phone=data.get('phone', ''),
                preferred_date=datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else None,
                preferred_time=datetime.strptime(data.get('time'), '%H:%M').time() if data.get('time') else None,
                healing_type=data.get('healing_type', ''),
                message=data.get('message', ''),
                status='pending'
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Healing session request submitted successfully!',
                'booking_reference': healing_session.booking_reference
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return render(request, 'healing/book_healing_session.html')


def events(request):
    """Events page view"""
    events = Event.objects.filter(is_active=True).order_by('event_date')
    
    # Pagination
    paginator = Paginator(events, 9)  # 9 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'page_obj': page_obj,
        'events': page_obj,
        'contact_info': contact_info,
    }
    
    return render(request, 'healing/events.html', context)


def event_detail(request, event_id):
    """Individual event detail view"""
    event = get_object_or_404(Event, id=event_id, is_active=True)
    related_events = Event.objects.filter(
        is_active=True
    ).exclude(id=event.id)[:3]
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'event': event,
        'related_events': related_events,
        'contact_info': contact_info,
    }
    
    return render(request, 'healing/event_detail.html', context)


def meditation(request):
    """Meditation page view"""
    # Get meditation-related content
    meditation_events = Event.objects.filter(
        is_active=True,
        title__icontains='meditation'
    ).order_by('event_date')
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'meditation_events': meditation_events,
        'contact_info': contact_info,
    }
    
    return render(request, 'healing/meditation.html', context)


def dynamic_theme_css(request):
    """Serve dynamic CSS based on theme settings"""
    css_content = render_to_string('healing/dynamic_theme.css')
    response = HttpResponse(css_content, content_type='text/css')
    response['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
    return response
