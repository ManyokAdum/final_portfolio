// ====================================
// Smooth Scrolling & Navigation
// ====================================

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Update active navigation link based on scroll position
function updateActiveNav() {
    const sections = document.querySelectorAll('section[id]');
    const scrollPosition = window.scrollY + 200;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            // Remove active class from all nav links
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            
            // Add active class to current section's nav link
            const activeLink = document.querySelector(`.nav-link[onclick*="${sectionId}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }
        }
    });
}

window.addEventListener('scroll', updateActiveNav);

// ====================================
// Sidebar Toggle
// ====================================

const toggleSidebarBtn = document.getElementById('toggle-sidebar-btn');
const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
const sidebar = document.getElementById('sidebar');

// Desktop sidebar toggle (collapse/expand)
if (toggleSidebarBtn) {
    toggleSidebarBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (window.innerWidth > 968) {
            sidebar.classList.toggle('collapsed');
            
            // Store state in localStorage
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebarCollapsed', isCollapsed);
        }
    });
}

// Mobile menu toggle (show/hide sidebar)
const sidebarOverlay = document.getElementById('sidebar-overlay');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        if (window.innerWidth <= 968) {
            const isActive = sidebar.classList.toggle('active');
            mobileMenuToggle.classList.toggle('active');
            mobileMenuToggle.setAttribute('aria-expanded', isActive);
            mobileMenuToggle.setAttribute('aria-label', isActive ? 'Close menu' : 'Open menu');
            
            if (sidebarOverlay) {
                sidebarOverlay.classList.toggle('active');
            }
            
            if (isActive) {
                document.body.classList.add('sidebar-open');
            } else {
                document.body.classList.remove('sidebar-open');
            }
        }
    });
}

// Close sidebar when clicking overlay
if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', () => {
        if (window.innerWidth <= 968) {
            sidebar.classList.remove('active');
            if (mobileMenuToggle) {
                mobileMenuToggle.classList.remove('active');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
                mobileMenuToggle.setAttribute('aria-label', 'Open menu');
            }
            sidebarOverlay.classList.remove('active');
            document.body.classList.remove('sidebar-open');
        }
    });
}

// Apply saved sidebar state on load (default to collapsed)
const savedSidebarState = localStorage.getItem('sidebarCollapsed');
if (sidebar) {
    if (window.innerWidth > 968) {
        if (savedSidebarState === 'false') {
            // Only expand if explicitly set to false
            sidebar.classList.remove('collapsed');
        } else {
            // Default to collapsed
            sidebar.classList.add('collapsed');
            localStorage.setItem('sidebarCollapsed', 'true');
        }
    }
}

// Close sidebar when clicking outside on mobile
function closeMobileSidebar() {
    sidebar.classList.remove('active');
    if (mobileMenuToggle) {
        mobileMenuToggle.classList.remove('active');
        mobileMenuToggle.setAttribute('aria-expanded', 'false');
        mobileMenuToggle.setAttribute('aria-label', 'Open menu');
    }
    if (sidebarOverlay) sidebarOverlay.classList.remove('active');
    document.body.classList.remove('sidebar-open');
}

document.addEventListener('click', (e) => {
    if (window.innerWidth <= 968) {
        if (!sidebar.contains(e.target) && 
            !mobileMenuToggle.contains(e.target) && 
            !sidebarOverlay.contains(e.target) &&
            sidebar.classList.contains('active')) {
            closeMobileSidebar();
        }
    }
});

// Close sidebar when clicking a nav link on mobile
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 968) closeMobileSidebar();
    });
});

// ====================================
// Theme Toggle
// ====================================

const themeToggle = document.getElementById('theme-toggle');
let currentTheme = localStorage.getItem('theme') || 'dark';

// Apply saved theme on load (default to dark)
if (currentTheme === 'light') {
    document.body.classList.add('light-theme');
} else {
    document.body.classList.remove('light-theme');
    localStorage.setItem('theme', 'dark');
}

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        currentTheme = document.body.classList.contains('light-theme') ? 'light' : 'dark';
        themeToggle.setAttribute('title', currentTheme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode');
        localStorage.setItem('theme', currentTheme);
    });
}

// ====================================
// Search Functionality
// ====================================

const searchInput = document.getElementById('search-input');

if (searchInput) {
    // Keyboard shortcut (Ctrl+K or Cmd+K)
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            searchInput.focus();
        }
    });

    // Simple search functionality
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        
        if (searchTerm.length < 2) return;

        // Search through sections and navigate to first match
        const sections = ['home', 'about', 'projects', 'contact'];
        const keywords = {
            'home': ['home', 'hero', 'intro', 'start'],
            'about': ['about', 'skills', 'expertise', 'experience', 'journey', 'technical'],
            'projects': ['projects', 'portfolio', 'work', 'showcase'],
            'contact': ['contact', 'message', 'email', 'connect', 'hire']
        };

        for (const section in keywords) {
            if (keywords[section].some(keyword => keyword.includes(searchTerm))) {
                scrollToSection(section);
                searchInput.blur();
                break;
            }
        }
    });
}

// ====================================
// Contact Form Submission
// ====================================

const contactForm = document.getElementById('contact-form');

if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(contactForm);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            subject: formData.get('subject'),
            message: formData.get('message')
        };

        // Validate form data
        if (!data.name || !data.email || !data.subject || !data.message) {
            showNotification('Please fill in all fields', 'error');
            return;
        }

        // Validate email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            showNotification('Please enter a valid email address', 'error');
            return;
        }

        try {
            // Get CSRF token from cookie
            const csrfToken = getCookie('csrftoken');

            const response = await fetch('/send-message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                showNotification('Message sent successfully! I\'ll get back to you soon.', 'success');
                contactForm.reset();
            } else {
                showNotification(result.message || 'Failed to send message. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('An error occurred. Please try again later.', 'error');
        }
    });
}

// ====================================
// Notification System
// ====================================

function showNotification(message, type = 'success') {
    const container = document.getElementById('notification-container');
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    const icon = type === 'success' 
        ? `<svg class="notification-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>`
        : `<svg class="notification-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>`;
    
    notification.innerHTML = `
        ${icon}
        <span class="notification-message">${message}</span>
    `;
    
    container.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ====================================
// Utility Functions
// ====================================

// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ====================================
// Intersection Observer for Animations
// ====================================

// Add fade-in animation for elements as they come into view
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards and sections
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.project-card, .skill-category, .info-item, .expertise-item');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
});

// ====================================
// Scroll to Top on Page Load
// ====================================

window.addEventListener('load', () => {
    window.scrollTo(0, 0);
});

// ====================================
// Handle Window Resize
// ====================================

let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        closeMobileSidebar();
    }, 250);
});

// ====================================
// Project Card Animations
// ====================================

const projectCards = document.querySelectorAll('.project-card');

projectCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
    });
});

// ====================================
// Initialize
// ====================================

console.log('%c Portfolio Website Loaded Successfully! ', 
    'background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%); color: white; font-size: 16px; padding: 10px; border-radius: 5px;'
);

console.log('%c Developed by Adum Thuc ', 
    'background: #0a0a0f; color: #6366f1; font-size: 14px; padding: 5px; border: 2px solid #6366f1; border-radius: 3px;'
);

