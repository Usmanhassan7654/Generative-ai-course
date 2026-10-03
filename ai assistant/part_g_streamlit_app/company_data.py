# This dictionary is the "brain data" of our company assistant.
# Students can change this dictionary and convert the same assistant
# for a clinic, school, restaurant, software house, real estate agency, etc.

COMPANY_CONFIG = {
    "company_name": "TechNova Solutions",
    "location": "Karachi, Pakistan",
    "working_hours": "Monday to Friday, 9 AM to 6 PM",
    "contact_email": "hello@technova.example",
    "phone": "+92-300-0000000",
    "about": (
        "TechNova Solutions builds practical AI, web, mobile and automation "
        "solutions for small and medium businesses."
    ),
    "services": {
        "website": {
            "display_name": "Business Website",
            "starting_price_usd": 1500,
            "description": "A professional company website with pages, contact form and basic SEO."
        },
        "chatbot": {
            "display_name": "AI Website Chatbot",
            "starting_price_usd": 2000,
            "description": "An AI assistant for customer support, FAQs and lead collection."
        },
        "mobile app": {
            "display_name": "Mobile App",
            "starting_price_usd": 5000,
            "description": "Android/iOS app for customers, bookings, orders or internal operations."
        },
        "computer vision": {
            "display_name": "Computer Vision System",
            "starting_price_usd": 4500,
            "description": "Camera-based detection, counting, safety monitoring or analytics."
        },
        "automation": {
            "display_name": "Business Automation",
            "starting_price_usd": 2500,
            "description": "Automating repetitive tasks using APIs, workflows and AI tools."
        }
    },
    "faqs": {
        "payment": "We usually take 40% advance, 40% after first demo and 20% before final delivery.",
        "timeline": "Small projects usually take 2–4 weeks. Bigger projects depend on scope.",
        "support": "We provide 30 days of free basic support after delivery."
    }
}
