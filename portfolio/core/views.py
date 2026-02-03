from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
import json

def home(request):
    context = {
        'name': 'Adum Thuc',
        'title': 'Full-Stack Software Engineer',
        'email': 'adummanyok96@gmail.com',
        'phone': '+211 910 111 997',
        'location': 'Juba, South Sudan',
        'github': 'https://github.com/ManyokAdum',
        'linkedin': 'https://www.linkedin.com/in/adum-thuc-b194b0217/',
        'twitter': 'https://x.com/Ayameraau',
        'facebook': 'https://www.facebook.com/adumthuc',
        'about_me_summary': 'Passionate about creating innovative solutions that bridge technology and real-world needs',
        'my_journey_text_1': "With over 5 years of experience in software development, I've had the privilege of working across multiple domains—from building robust web applications to developing secure mobile solutions and implementing cybersecurity measures.",
        'my_journey_text_2': "My journey began with a Computer Science degree from Kenya Methodist University, where I developed a strong foundation in programming principles and software engineering practices. Since then, I've continuously evolved my skill set to stay at the forefront of technology.",
        'my_journey_text_3': "Currently serving as a Systems Administrator at Belednai Technology in South Sudan, I focus on maintaining critical infrastructure while developing innovative solutions that enhance operational efficiency and security.",
        'my_journey_text_4': "What drives me is the ability to solve complex real-world problems through technology—whether it's building a seamless user experience, securing sensitive data, or optimizing system performance for maximum impact.",
        'education_degree': 'Computer Science',
        'education_university': 'Kenya Methodist University',
        'current_role': 'Systems Administrator',
        'current_company': 'Belednai Technology',
        'expertise_list': [
            {'icon': 'web-dev-icon.svg', 'name': 'Web Development'},
            {'icon': 'mobile-app-icon.svg', 'name': 'Mobile Applications'},
            {'icon': 'database-icon.svg', 'name': 'Database Design'},
            {'icon': 'cybersecurity-icon.svg', 'name': 'Cybersecurity'},
            {'icon': 'data-analysis-icon.svg', 'name': 'Data Analysis'},
        ],
        'frontend_skills': ['React', 'JavaScript/TypeScript', 'HTML5/CSS3', 'Tailwind CSS', 'Vue.js'],
        'backend_skills': ['Java', 'Spring Boot', 'Node.js', 'Python', 'Django', 'REST APIs'],
        'mobile_skills': ['Flutter', 'Dart', 'Android Development', 'iOS Development', 'Cross-platform'],
        'database_skills': ['PostgreSQL', 'MySQL', 'MongoDB', 'Firebase', 'Database Design'],
        'devops_tools_skills': ['Docker', 'Git', 'Linux', 'AWS', 'CI/CD', 'System Administration'],
        'security_skills': ['Network Security', 'Penetration Testing', 'Vulnerability Assessment', 'Compliance'],
        'tools_technologies': ['IntelliJ IDEA', 'VS Code', 'Android Studio', 'Postman', 'Docker Desktop', 'Git/GitHub', 'Figma', 'Tableau', 'Wireshark', 'Burp Suite'],
        'projects': [
            {
                'image': 'ecommerce.jpg',
                'title': 'E-Commerce Platform',
                'description': 'Full-stack e-commerce solution with payment integration, inventory management, and admin dashboard. Built with modern web technologies.',
                'technologies': ['Java', 'Spring Boot', 'React', 'PostgreSQL', 'Docker'],
                'live_demo_url': '#',
                'code_url': '#'
            },
            {
                'image': 'mobile-banking.jpg',
                'title': 'Mobile Banking App',
                'description': 'Secure mobile banking application with biometric authentication, transaction history, and real-time notifications.',
                'technologies': ['Flutter', 'Dart', 'Firebase', 'Encryption', 'REST API'],
                'live_demo_url': '#',
                'code_url': '#'
            },
            {
                'image': 'analytics.jpg',
                'title': 'Data Analytics Dashboard',
                'description': 'Interactive dashboard for business intelligence with real-time data visualization and predictive analytics.',
                'technologies': ['Python', 'Django', 'Chart.js', 'PostgreSQL', 'Machine Learning'],
                'live_demo_url': '#',
                'code_url': '#'
            },
            {
                'image': 'cybersecurity.jpg',
                'title': 'Cybersecurity Monitoring Tool',
                'description': 'Network security monitoring system with threat detection, alert management, and compliance reporting.',
                'technologies': ['Python', 'Network Security', 'Monitoring', 'Alerts', 'Compliance'],
                'live_demo_url': '#',
                'code_url': '#'
            },
        ]
    }
    return render(request, 'index.html', context)

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            subject = data.get('subject', '').strip()
            message = data.get('message', '').strip()

            if not all([name, email, subject, message]):
                return JsonResponse({
                    'success': False,
                    'message': 'Please fill in all fields.'
                }, status=400)

            recipient = getattr(settings, 'CONTACT_EMAIL', 'adummanyok96@gmail.com')
            email_subject = f"[Portfolio] {subject}"
            email_body = f"You received a message from your portfolio contact form.\n\n"
            email_body += f"From: {name} <{email}>\n"
            email_body += f"Subject: {subject}\n\n"
            email_body += f"Message:\n{message}"

            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )

            return JsonResponse({
                'success': True,
                'message': 'Thank you! Your message has been sent successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again later.'
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)

