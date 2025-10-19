from django.core.management.base import BaseCommand
from healing.models import (
    WorkshopCategory, Workshop, Healer, Testimonial, SiteSettings,
    SiteContent, ThemeSettings, ContactInfo, Event, GalleryImage
)


class Command(BaseCommand):
    help = 'Populate the database with initial data for Pranic Healing USA'

    def handle(self, *args, **options):
        self.stdout.write('Populating database with initial data...')
        
        # Create Site Settings
        site_settings, created = SiteSettings.objects.get_or_create(
            site_name="Pranic Healing USA",
            defaults={
                'site_tagline': 'Energy Healing & Spiritual Wellness',
                'site_description': 'The Center for Pranic Healing is a non-profit tax-exempt organization whose mission is to help people live a happy, healthy and well-balanced life.',
                'phone': '(877) 787-3792',
                'email': 'info@pranichealingusa.com',
                'address': '420 Valley Brook Ave\nLyndhurst, NJ 07071',
                'facebook_url': 'https://facebook.com/pranichealingusa',
                'instagram_url': 'https://instagram.com/pranichealingusa',
                'is_active': True
            }
        )
        
        # Create Contact Info
        contact_info, created = ContactInfo.objects.get_or_create(
            phone="(877) 787-3792",
            defaults={
                'email': 'info@pranichealingusa.com',
                'address': '420 Valley Brook Ave\nLyndhurst, NJ 07071',
                'facebook_url': 'https://facebook.com/pranichealingusa',
                'instagram_url': 'https://instagram.com/pranichealingusa',
                'is_active': True
            }
        )
        
        # Create Theme Settings
        theme_settings, created = ThemeSettings.objects.get_or_create(
            name="Pranic Healing Theme",
            defaults={
                'primary_color': '#2E8B57',
                'secondary_color': '#32CD32',
                'accent_color': '#228B22',
                'text_color': '#2c2c2c',
                'background_color': '#ffffff',
                'heading_font': 'Merriweather',
                'body_font': 'Open Sans',
                'is_active': True
            }
        )
        
        # Create Site Content
        content_data = [
            ('hero_title', 'Balance Every Area of Your Life', 'Balance Every Area of Your Life'),
            ('hero_subtitle', 'The Center for Pranic Healing is a non-profit tax-exempt organization whose mission is to help people live a happy, healthy and well-balanced life.', 'The Center for Pranic Healing is a non-profit tax-exempt organization whose mission is to help people live a happy, healthy and well-balanced life.'),
            ('about_title', 'WHO WE ARE', 'WHO WE ARE'),
            ('about_subtitle', 'The Center for Pranic Healing is a non-profit tax-exempt organization whose mission is to help people live a happy, healthy and well-balanced life.', 'The Center for Pranic Healing is a non-profit tax-exempt organization whose mission is to help people live a happy, healthy and well-balanced life.'),
            ('mission_statement', 'Our mission is to help you create remarkable transformations in all areas of your life. Through knowledge of Pranic Healing and Arhatic Yoga you will learn how to enhance all aspects of your life including physical, emotional, financial and spiritual.', 'Our mission is to help you create remarkable transformations in all areas of your life. Through knowledge of Pranic Healing and Arhatic Yoga you will learn how to enhance all aspects of your life including physical, emotional, financial and spiritual.'),
        ]
        
        for content_type, title, content in content_data:
            SiteContent.objects.get_or_create(
                content_type=content_type,
                defaults={
                    'title': title,
                    'content': content,
                    'is_active': True
                }
            )
        
        # Create Workshop Categories
        categories_data = [
            ('Basic Pranic Healing', 'This is the basic and introductory course in Pranic Healing. It is an experiential workshop to discover one\'s innate ability to heal.'),
            ('Spiritual Workshops', 'Come explore our Spiritual Workshop and learn about the priceless techniques taught by GrandMaster Choa Kok Sui.'),
            ('Prosperity Workshops', 'Ancient teaching and concepts will show you effective ways to create, materialize and facilitate the flow of prosperity energy.'),
            ('Meditation', 'Learn about the different meditations and find a group to join near you!'),
        ]
        
        for name, description in categories_data:
            WorkshopCategory.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'is_active': True
                }
            )
        
        # Create Workshops
        workshops_data = [
            ('Basic Pranic Healing Level 1', 'Basic Pranic Healing', 'Learn the fundamentals of Pranic Healing in this comprehensive 2-day workshop.', 299, '2 days', 16, True),
            ('Basic Pranic Healing Level 2', 'Basic Pranic Healing', 'Advanced techniques and deeper understanding of Pranic Healing principles.', 399, '2 days', 16, True),
            ('Meditation on Twin Hearts', 'Meditation', 'Learn the powerful meditation technique for spiritual development and world peace.', 150, '1 day', 8, True),
            ('Arhatic Yoga Level 1', 'Spiritual Workshops', 'Introduction to Arhatic Yoga for spiritual development and self-realization.', 500, '3 days', 24, True),
            ('Prosperity Workshop', 'Prosperity Workshops', 'Learn ancient techniques for creating abundance and prosperity in all areas of life.', 250, '1 day', 8, True),
        ]
        
        for name, category_name, description, price, duration, duration_hours, is_featured in workshops_data:
            category = WorkshopCategory.objects.get(name=category_name)
            Workshop.objects.get_or_create(
                name=name,
                category=category,
                defaults={
                    'description': description,
                    'price': price,
                    'duration': duration,
                    'duration_hours': duration_hours,
                    'is_featured': is_featured,
                    'is_active': True
                }
            )
        
        # Create Healers
        healers_data = [
            ('Master Glenn', 'Senior Pranic Healer', 'Physical & Emotional Healing', 'Master Glenn has over 20 years of experience in Pranic Healing and has helped thousands of people achieve wellness and transformation.'),
            ('Master Marilag', 'Certified Pranic Healer', 'Spiritual & Energy Healing', 'Master Marilag specializes in spiritual healing and chakra balancing, bringing deep transformation to her clients.'),
            ('Dr. Sarah Johnson', 'Certified Pranic Healer', 'Physical Healing & Pain Relief', 'Dr. Sarah combines her medical background with Pranic Healing to provide comprehensive healing solutions.'),
            ('Michael Chen', 'Certified Pranic Healer', 'Emotional & Mental Healing', 'Michael specializes in emotional healing and stress management, helping clients overcome anxiety and depression.'),
        ]
        
        for name, position, specialization, bio in healers_data:
            Healer.objects.get_or_create(
                name=name,
                defaults={
                    'position': position,
                    'specialization': specialization,
                    'bio': bio,
                    'is_active': True
                }
            )
        
        # Create Testimonials
        testimonials_data = [
            ('Elena Brower', 'Certified Anusara Yoga Teacher', 'Learning Pranic Healing is very important for every yoga teacher. With these tools, teachers can know how to clear unwanted and negative energies from their students and space, and create real comfort for people when they enter their classes', 5, True),
            ('Allison Eibach', 'L.P.N., Davis Dermatology Clinic', 'Since I was introduced to Pranic Healing I have seen amazing healings of wounds and skin rashes. The surgeries in this practice heal so much faster than I have ever seen since we incorporated Pranic Healing.', 5, True),
            ('Connie Williams', 'Speech Therapist, M.Ed., CCC-SLP', 'As a speech therapist with 25 years of experience I have found Pranic Healing to be extremely beneficial for children who have speech, learning and attention problems, and autism.', 5, True),
            ('John Smith', 'Business Owner', 'Pranic Healing has transformed my life completely. I was suffering from chronic pain for years, and after just a few sessions, I felt relief I never thought possible.', 5, True),
            ('Maria Garcia', 'Teacher', 'The meditation techniques I learned have brought so much peace and clarity to my life. I feel more centered and focused than ever before.', 5, True),
        ]
        
        for name, profession, content, rating, is_featured in testimonials_data:
            Testimonial.objects.get_or_create(
                client_name=name,
                profession=profession,
                defaults={
                    'content': content,
                    'rating': rating,
                    'is_featured': is_featured,
                    'is_active': True
                }
            )
        
        # Create Events
        from datetime import date, time, timedelta
        events_data = [
            ('Wednesday Global Meditation', 'Join us for our weekly global meditation session. All are welcome to participate in this powerful group meditation.', date.today() + timedelta(days=7), time(20, 0), time(21, 30), 'New Jersey', True),
            ('Basic Pranic Healing Workshop', 'Learn the fundamentals of Pranic Healing in this comprehensive 2-day workshop.', date.today() + timedelta(days=14), time(9, 0), time(18, 0), 'New York, NY', True),
            ('Meditation on Twin Hearts', 'Experience the powerful meditation technique for spiritual development and world peace.', date.today() + timedelta(days=21), time(19, 0), time(21, 0), 'Brooklyn, NY', True),
        ]
        
        for title, description, event_date, start_time, end_time, location, is_featured in events_data:
            Event.objects.get_or_create(
                title=title,
                event_date=event_date,
                defaults={
                    'description': description,
                    'start_time': start_time,
                    'end_time': end_time,
                    'location': location,
                    'is_featured': is_featured,
                    'is_active': True
                }
            )
        
        # Create Gallery Images
        gallery_data = [
            ('Healing Session 1', 'A peaceful healing session in progress', 'healing-sessions'),
            ('Healing Session 2', 'Energy healing techniques demonstration', 'healing-sessions'),
            ('Workshop Training', 'Students learning Pranic Healing techniques', 'workshops'),
            ('Meditation Group', 'Group meditation session for inner peace', 'meditation'),
            ('Meditation Class', 'Learning meditation techniques', 'meditation'),
            ('Community Event', 'Healing community gathering', 'events'),
            ('Workshop Graduation', 'Students completing their training', 'workshops'),
            ('Testimonial Photo', 'Client sharing their healing experience', 'testimonials'),
            ('Healing Therapy', 'One-on-one healing session', 'healing-sessions'),
            ('Meditation Retreat', 'Weekend meditation retreat', 'meditation'),
            ('Workshop Practice', 'Hands-on practice session', 'workshops'),
            ('Community Healing', 'Group healing session', 'events'),
        ]
        
        for title, description, category in gallery_data:
            GalleryImage.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'is_active': True
                }
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with initial data!')
        )
