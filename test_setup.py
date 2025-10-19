#!/usr/bin/env python
"""
Test script to verify the Pranic Healing USA project setup
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))
sys.path.insert(0, str(project_dir / 'pranicpathway'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pranicpathway.settings')

try:
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

# Test imports
try:
    from healing.models import WorkshopCategory, Workshop, Healer, Testimonial, SiteSettings
    print("✅ Model imports successful")
except Exception as e:
    print(f"❌ Model imports failed: {e}")
    sys.exit(1)

# Test URL patterns
try:
    from django.urls import reverse
    from healing.urls import urlpatterns
    print("✅ URL patterns loaded successfully")
    print(f"   Found {len(urlpatterns)} URL patterns")
except Exception as e:
    print(f"❌ URL patterns failed: {e}")
    sys.exit(1)

# Test views
try:
    from healing.views import home, about, workshops, contact
    print("✅ View imports successful")
except Exception as e:
    print(f"❌ View imports failed: {e}")
    sys.exit(1)

# Test admin
try:
    from healing.admin import admin_site
    print("✅ Admin configuration loaded successfully")
except Exception as e:
    print(f"❌ Admin configuration failed: {e}")
    sys.exit(1)

# Test forms
try:
    from healing.forms import ContactForm, HealingSessionForm, CustomerFeedbackForm
    print("✅ Form imports successful")
except Exception as e:
    print(f"❌ Form imports failed: {e}")
    sys.exit(1)

# Test management commands
try:
    from healing.management.commands.populate_data import Command
    print("✅ Management command loaded successfully")
except Exception as e:
    print(f"❌ Management command failed: {e}")
    sys.exit(1)

print("\n🎉 All tests passed! The Pranic Healing USA project is ready to use.")
print("\nNext steps:")
print("1. Run: python manage.py makemigrations")
print("2. Run: python manage.py migrate")
print("3. Run: python manage.py populate_data")
print("4. Run: python manage.py createsuperuser")
print("5. Run: python manage.py runserver")
print("\nThen visit: http://127.0.0.1:8000")
