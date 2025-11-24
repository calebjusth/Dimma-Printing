# main/jazzmin.py

JAZZMIN_SETTINGS = {
    "site_title": "Dimma Printing Admin",
    "site_header": "Dimma Printing",
    "site_brand": "Dimma Printing",
    "welcome_sign": "Welcome to Dimma Printing Admin",
    "copyright": "Dimma Printing Plc",
    "search_model": ["home.Client", "home.Project", "home.Service"],

    # UI Colors
    "theme": "darkly",  # Bootstrap dark theme
    "site_logo": "images/fav.png",  # Put your logo in static/images
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": "images/fav.png",
    "show_ui_builder": False,

    # Custom Menu
    "topmenu_links": [
        {"name": "Home", "url": "/", "permissions": ["auth.view_user"]},
        {"home": "app"},  # shows all models in your app
    ],

    # Side Menu
    "icons": {
        "auth": "fas fa-users-cog",
        "home.Client": "fas fa-handshake",
        "home.ProjectCategory": "fas fa-folder",
        "home.Project": "fas fa-briefcase",
        "home.SocialMedia": "fas fa-share-alt",
        "home.HomeContent": "fas fa-home",
        "home.Testimonial": "fas fa-comment-dots",
        "home.Service": "fas fa-cogs",
        "home.TeamMember": "fas fa-user-tie",
        "home.ContactInfo": "fas fa-address-book",
        "home.HeroSection": "fa-solid fa-pen",
        "home.SisterCompany": "fa-regular fa-building",

        #blog section

        "blog.BlogCategory": "fa-solid fa-layer-group",
        "blog.BlogPost": "fa-solid fa-blog",
        "blog.BlogComment": "fa-solid fa-comments",
        "blog.BlogTag": "fa-solid fa-tags"
    },

    # Sidebar
    "hide_homes": [],
    "hide_models": [],
    "order_with_respect_to": ["home.Client", "home.Project", "home.Service"],

    # Custom CSS & JS
    "custom_css": None,
    "custom_js": None,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",  # Jazzmin themes: darkly, solar, cyborg, etc.
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark bg-dark",
    "sidebar": "sidebar-dark-danger",  # red accent
    "actions_sticky_top": True,
}
