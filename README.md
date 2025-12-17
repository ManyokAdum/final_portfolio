# Django Portfolio Website

A modern, professional portfolio website built with Django, HTML, CSS, and JavaScript. This portfolio features a beautiful design with smooth animations, responsive layout, and interactive elements.

## 🌟 Features

- **Modern Design**: Clean, professional UI with gradient accents and smooth animations
- **Responsive Layout**: Fully responsive design that works on all devices (desktop, tablet, mobile)
- **Dark Theme**: Beautiful dark theme with an accent mode switcher
- **Smooth Navigation**: Sidebar navigation with smooth scrolling to sections
- **Interactive Elements**: 
  - Smooth scroll navigation
  - Theme switcher (Default/Accent modes)
  - Contact form with validation
  - Hover effects and animations
  - Search functionality
- **Sections**:
  - Hero section with profile image
  - About Me (Journey, Quick Info, Expertise)
  - Technical Skills (Frontend, Backend, Mobile, Database, DevOps, Security)
  - Tools & Technologies
  - Featured Projects showcase
  - Contact form with social links
  - Professional footer

## 📁 Project Structure

```
portfolio/
├── manage.py
├── db.sqlite3
├── portfolio/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   ├── asgi.py
│   └── core/                # Main app
│       ├── __init__.py
│       ├── apps.py
│       ├── views.py         # View functions
│       ├── urls.py          # App URL configuration
│       ├── static/          # Static files
│       │   ├── CSS/
│       │   │   └── style.css    # Main stylesheet
│       │   ├── Images/
│       │   │   ├── profile.jpg
│       │   │   ├── ecommerce.jpg
│       │   │   ├── mobile-banking.jpg
│       │   │   ├── analytics.jpg
│       │   │   └── cybersecurity.jpg
│       │   └── Js/
│       │       └── script.js    # JavaScript functionality
│       └── templates/
│           └── index.html       # Main template
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Django 5.1.6 or higher

### Installation

1. **Clone or navigate to the project directory**:
```bash
cd portfolio
```

2. **Install Django** (if not already installed):
```bash
pip install django
```

3. **Run migrations** (if needed):
```bash
python manage.py migrate
```

4. **Start the development server**:
```bash
python manage.py runserver
```

5. **Open your browser** and navigate to:
```
http://127.0.0.1:8000/
```

## 🎨 Customization

### Updating Personal Information

Edit `portfolio/core/views.py` to update your personal information:

```python
context = {
    'name': 'Your Name',
    'title': 'Your Title',
    'description': 'Your description',
    'email': 'your.email@example.com',
    'phone': 'your-phone',
    'location': 'Your Location',
    'github': 'https://github.com/yourusername',
    'linkedin': 'https://linkedin.com/in/yourusername',
    'twitter': 'https://twitter.com/yourusername',
}
```

### Updating Images

Replace the placeholder images in `portfolio/core/static/Images/` with your own:

- **profile.jpg**: Your professional profile photo (350x350px recommended)
- **ecommerce.jpg**: E-Commerce project screenshot
- **mobile-banking.jpg**: Mobile Banking project screenshot
- **analytics.jpg**: Data Analytics project screenshot
- **cybersecurity.jpg**: Cybersecurity project screenshot

### Updating Content

Edit `portfolio/core/templates/index.html` to update:
- About Me content
- Skills and technologies
- Projects information
- Contact information

### Customizing Styles

Edit `portfolio/core/static/CSS/style.css` to customize:
- Colors (see CSS variables at the top)
- Fonts
- Spacing
- Animations
- Layout

### Customizing JavaScript

Edit `portfolio/core/static/Js/script.js` to customize:
- Navigation behavior
- Theme switching
- Form validation
- Search functionality
- Animations

## 🎯 Key Features Explained

### Theme Switcher
The portfolio includes two themes:
- **Default Theme**: Dark blue/purple gradient theme
- **Accent Theme**: Purple/pink gradient theme

Users can switch between themes using the theme toggle button in the sidebar. The preference is saved in localStorage.

### Smooth Scrolling
Click on navigation items to smoothly scroll to different sections of the portfolio.

### Contact Form
The contact form includes:
- Client-side validation
- AJAX submission (without page reload)
- Success/error notifications
- Required field validation
- Email format validation

### Responsive Design
The portfolio is fully responsive with breakpoints for:
- Desktop (> 968px)
- Tablet (768px - 968px)
- Mobile (< 768px)

The sidebar becomes a slide-out menu on mobile devices.

### Animations
- Fade-in animations for cards and sections
- Hover effects on buttons and links
- Smooth transitions between states
- Floating animation on profile image

## 📝 Django Configuration

### Settings (`portfolio/settings.py`)
- `INSTALLED_APPS`: Includes the core app
- `TEMPLATES`: Configured to use templates from core app
- `STATICFILES_DIRS`: Configured to serve static files from core app
- `DEBUG`: Set to True for development (change to False for production)

### URLs (`portfolio/urls.py`)
- Main URL configuration includes the core app URLs
- Admin panel available at `/admin/`

### Views (`portfolio/core/views.py`)
- `home()`: Renders the main portfolio page with context data
- `send_message()`: Handles contact form submissions (API endpoint)

## 🔒 Security Notes

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Update `ALLOWED_HOSTS` in `settings.py`
3. Change `SECRET_KEY` to a secure random value
4. Set up proper database (PostgreSQL, MySQL, etc.)
5. Configure static file serving (e.g., with WhiteNoise or CDN)
6. Set up HTTPS
7. Configure CSRF protection properly
8. Set up email backend for contact form

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📱 Mobile Features

- Collapsible sidebar navigation
- Touch-friendly buttons and links
- Optimized images for mobile
- Responsive typography
- Mobile-friendly forms

## 🛠️ Technologies Used

- **Backend**: Django 5.1.6
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite3 (default)
- **Icons**: SVG icons (Feather Icons style)
- **Fonts**: System fonts (-apple-system, Segoe UI, etc.)

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [CSS Tricks](https://css-tricks.com/)

## 🤝 Contributing

Feel free to fork this project and customize it for your own portfolio!

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Adum Thuc**
- Email: adummanyok96@gmail.com
- Phone: +211 910 111 997
- Location: Juba, South Sudan
- GitHub: [@adamthuc](https://github.com/adamthuc)
- LinkedIn: [adamthuc](https://linkedin.com/in/adamthuc)
- Twitter: [@adamthuc](https://twitter.com/adamthuc)

## 🎉 Acknowledgments

- Design inspired by modern portfolio websites
- Built with Django framework
- Icons inspired by Feather Icons

---

**Note**: This is a development setup. For production deployment, please follow Django's deployment best practices and security guidelines.



