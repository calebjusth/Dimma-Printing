
// DOM Elements
        const header = document.getElementById('header');
        const navToggle = document.getElementById('navToggle');
        const navOverlay = document.getElementById('navOverlay');
        const hamburgerIcon = document.querySelector('.hamburger-icon');
        const closeIcon = document.querySelector('.close-icon');
        
        // Scroll event for header background change
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
                header.classList.remove('transparent');
            } else {
                header.classList.remove('scrolled');
                header.classList.add('transparent');
            }
        });
        
        // Toggle navigation
        navToggle.addEventListener('click', () => {
            const isOpen = navOverlay.classList.toggle('active');
            
            if (isOpen) {
                // Show close icon, hide hamburger
                hamburgerIcon.style.display = 'none';
                closeIcon.style.display = 'block';
                document.body.style.overflow = 'hidden'; // Prevent scrolling when nav is open
            } else {
                // Show hamburger icon, hide close
                hamburgerIcon.style.display = 'block';
                closeIcon.style.display = 'none';
                document.body.style.overflow = ''; // Re-enable scrolling
            }
        });
        
        // Close navigation when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navOverlay.classList.remove('active');
                hamburgerIcon.style.display = 'block';
                closeIcon.style.display = 'none';
                document.body.style.overflow = '';
            });
        });

        // Cursor code remains the same as before
        document.addEventListener('DOMContentLoaded', function() {
            const cursor = document.querySelector('.cursor');
            const follower = document.querySelector('.cursor-follower');
            
            let posX = 0, posY = 0;
            let mouseX = 0, mouseY = 0;
            
            // Update cursor position
            function updateCursor() {
                posX += (mouseX - posX) / 2;
                posY += (mouseY - posY) / 2;
                
                cursor.style.transform = `translate(${posX}px, ${posY}px)`;
                follower.style.transform = `translate(${posX}px, ${posY}px)`;
                
                requestAnimationFrame(updateCursor);
            }
            
            // Mouse move event
            document.addEventListener('mousemove', function(e) {
                mouseX = e.clientX;
                mouseY = e.clientY;
            });
            
            // Hover effects
            const hoverElements = document.querySelectorAll('.btn, a, button, [data-hover]');
            
            hoverElements.forEach(el => {
                el.addEventListener('mouseenter', () => {
                    cursor.classList.add('hover');
                    follower.classList.add('hover');
                });
                
                el.addEventListener('mouseleave', () => {
                    cursor.classList.remove('hover');
                    follower.classList.remove('hover');
                });
            });
            
            // Click effect
            document.addEventListener('mousedown', () => {
                cursor.classList.add('click');
                follower.classList.add('click');
            });
            
            document.addEventListener('mouseup', () => {
                cursor.classList.remove('click');
                follower.classList.remove('click');
            });
            
            // Hide cursor when leaving window
            document.addEventListener('mouseout', () => {
                cursor.style.opacity = '0';
                follower.style.opacity = '0';
            });
            
            document.addEventListener('mouseover', () => {
                cursor.style.opacity = '1';
                follower.style.opacity = '1';
            });
            
            // Start animation
            updateCursor();
        });


    const loadingAnimation = document.querySelector('.loading-animation');
    
    // Hide loading animation after page load
    window.addEventListener('load', function() {
        setTimeout(() => {
            loadingAnimation.classList.add('hidden');
        }, 1000);
    });
    