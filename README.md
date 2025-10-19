# Pranic Pathway Nepal

A Django-based website for Pranic Pathway Nepal, featuring energy healing services, workshops, and spiritual wellness content.

## Features

- **Home Page**: Hero section with mission statement and service overview
- **About Us**: Information about Pranic Healing and the organization
- **Workshops**: Comprehensive workshop listings and registration
- **Healers**: Meet our certified Pranic Healers
- **Gallery**: Photo gallery of healing sessions and events
- **Testimonials**: Client testimonials and feedback
- **Blog**: Articles about healing, meditation, and spiritual growth
- **Contact**: Contact form and business information
- **Healing Sessions**: Book personalized healing sessions
- **Events**: Upcoming workshops and meditation sessions
- **Meditation**: Meditation resources and group sessions

## Technology Stack

- **Backend**: Django 5.1.7
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **Icons**: Font Awesome 6
- **Fonts**: Merriweather, Open Sans

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pranicpathway_project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
pranicpathway_project/
├── pranicpathway/
│   ├── pranicpathway/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── healing/
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── admin.py
│       ├── forms.py
│       └── context_processors.py
├── templates/
│   └── healing/
│       ├── base.html
│       ├── home.html
│       ├── about.html
│       ├── workshops.html
│       ├── contact.html
│       └── book_healing_session.html
├── static/
│   ├── css/
│   │   ├── pranic-healing.css
│   │   └── bootstrap.min.css
│   ├── js/
│   │   └── pranic-healing.js
│   └── img/
├── media/
└── manage.py
```

## Models

- **WorkshopCategory**: Categories for workshops (Basic, Spiritual, Prosperity)
- **Workshop**: Individual workshop details
- **Healer**: Certified Pranic Healers
- **Testimonial**: Client testimonials
- **GalleryImage**: Photo gallery
- **BlogPost**: Blog articles
- **HealingSession**: Healing session bookings
- **Event**: Workshops and events calendar
- **ContactMessage**: Contact form submissions
- **SiteSettings**: General site configuration
- **ThemeSettings**: Customizable theme options
- **SEOSettings**: SEO optimization settings

## Admin Features

- Custom admin interface with organized sections
- Content management for all site elements
- SEO settings for each page
- Theme customization
- Analytics integration
- Contact message management

## Deployment

The project is configured for deployment on platforms like Render, Heroku, or any Django-compatible hosting service.

### Environment Variables

Set the following environment variables for production:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string (for PostgreSQL)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions about this project, please contact the development team.

---

**Pranic Healing USA** - Energy Healing & Spiritual Wellness

