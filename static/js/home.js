
    document.addEventListener('DOMContentLoaded', function() {
        const colorReveal = document.getElementById('colorReveal');
        const cursor = document.querySelector('.cursor');
        
        // Function to update the color reveal position
        function updateColorReveal() {
            if (!cursor || !colorReveal) return;
            
            const cursorRect = cursor.getBoundingClientRect();
            const cursorX = cursorRect.left + cursorRect.width / 2;
            const cursorY = cursorRect.top + cursorRect.height / 2;
            
            // Update the mask position to follow cursor
            colorReveal.style.webkitMaskPosition = `${cursorX}px ${cursorY}px`;
            colorReveal.style.maskPosition = `${cursorX}px ${cursorY}px`;
            
            requestAnimationFrame(updateColorReveal);
        }
        
        // Start the animation
        updateColorReveal();
    });



    // Scroll animation implementation
document.addEventListener('DOMContentLoaded', function() {
    const scrollElements = document.querySelectorAll('[data-scroll]');
    
    const elementInView = (el, dividend = 1) => {
        const elementTop = el.getBoundingClientRect().top;
        return (
            elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend
        );
    };
    
    const displayScrollElement = (element) => {
        element.classList.add('is-visible');
    };
    
    const hideScrollElement = (element) => {
        element.classList.remove('is-visible');
    };
    
    const handleScrollAnimation = () => {
        scrollElements.forEach((el) => {
            if (elementInView(el, 1.2)) {
                const delay = el.getAttribute('data-scroll-delay') || 0;
                setTimeout(() => {
                    displayScrollElement(el);
                }, delay * 1000);
            }
        });
    };
    
    // Counter animation for stats
    const startCounters = () => {
        const counters = document.querySelectorAll('.stat-number');
        const speed = 200;
        
        counters.forEach(counter => {
            if (elementInView(counter, 1.5) && !counter.classList.contains('animated')) {
                counter.classList.add('animated');
                
                const target = parseInt(counter.getAttribute('data-count'));
                let count = 0;
                
                const updateCount = () => {
                    const increment = Math.ceil(target / speed);
                    
                    if (count < target) {
                        count += increment;
                        if (count > target) count = target;
                        counter.innerText = count;
                        setTimeout(updateCount, 10);
                    } else {
                        counter.innerText = target;
                    }
                };
                
                updateCount();
            }
        });
    };
    
    // Initial check on page load
    handleScrollAnimation();
    startCounters();
    
    // Listen for scroll events
    window.addEventListener('scroll', () => {
        handleScrollAnimation();
        startCounters();
    });
});


// Scroll animation for feature cards
document.addEventListener('DOMContentLoaded', function() {
    const featureCards = document.querySelectorAll('.feature-card');
    
    const elementInView = (el, dividend = 1) => {
        const elementTop = el.getBoundingClientRect().top;
        return (
            elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend
        );
    };
    
    const displayScrollElement = (element) => {
        element.classList.add('is-visible');
    };
    
    const handleScrollAnimation = () => {
        featureCards.forEach((el, index) => {
            if (elementInView(el, 1.2)) {
                const delay = el.getAttribute('data-scroll-delay') || 0;
                setTimeout(() => {
                    displayScrollElement(el);
                }, delay * 300);
            }
        });
    };
    
    // Initial check
    handleScrollAnimation();
    
    // Listen for scroll events
    window.addEventListener('scroll', handleScrollAnimation);
});


document.addEventListener('DOMContentLoaded', function() {
    // Filter functionality
    const filterButtons = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.getAttribute('data-filter');
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Filter items
            portfolioItems.forEach(item => {
                const type = item.getAttribute('data-type');
                
                if (filter === 'all' || filter === type) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
    
    // Modal functionality
    const viewButtons = document.querySelectorAll('.view-project-btn');
    const modal = document.querySelector('.project-modal');
    const modalClose = document.querySelector('.modal-close');
    const modalBody = document.querySelector('.modal-body');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', () => {
            const projectItem = button.closest('.portfolio-item');
            
            // Get data from the project card
            const title = projectItem.querySelector('.project-title').textContent;
            const subtitle = projectItem.querySelector('.project-subtitle')?.textContent || '';
            const description = projectItem.querySelector('.project-description').textContent;
            
            // Get media elements
            const imageElement = projectItem.querySelector('.portfolio-image');
            const videoElement = projectItem.querySelector('.portfolio-video');
            
            // Build modal content
            let mediaContent = '';
            
            if (imageElement) {
                mediaContent = `<img src="${imageElement.src}" alt="${title}" class="modal-image">`;
            }
            
            if (videoElement) {
                // Use the poster as image if available, otherwise use a placeholder
                const poster = videoElement.poster || 'https://placehold.co/600x400';
                mediaContent = `
                    <div class="video-container">
                        <video controls poster="${poster}" class="modal-video">
                            ${videoElement.innerHTML}
                        </video>
                    </div>
                `;
            }
            
            // Set modal content
            modalBody.innerHTML = `
                <div class="modal-project">
                    <div class="modal-media">
                        ${mediaContent}
                    </div>
                    <div class="modal-details">
                        <h2 style="color:whitesmoke !important;">${title}</h2>
                        ${subtitle ? `<p class="modal-subtitle" style="color:whitesmoke !important;">${subtitle}</p>` : ''}
                        <div class="modal-description" style="color:whitesmoke !important;">${description}</div>
                    </div>
                </div>
            `;
            
            // Show the modal
            modal.classList.add('active');
        });
    });
    
    modalClose.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    
    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
  const floatingContainer = document.querySelector('.floating-action-container');
  const floatingBtn = document.querySelector('.floating-action-btn');
  const portfolioSection = document.querySelector('.portfolio-section');
  let hasExpanded = false;
  
  function checkButtonVisibility() {
    const sectionRect = portfolioSection.getBoundingClientRect();
    const scrollPosition = window.innerHeight + window.pageYOffset;
    const sectionBottom = portfolioSection.offsetTop + portfolioSection.offsetHeight;
    
    // Show button when user is 300px from the bottom of the section
    if (scrollPosition > sectionBottom - 300 && !hasExpanded) {
      floatingContainer.classList.add('visible');
      
      // Expand the button after a short delay
      setTimeout(() => {
        floatingBtn.classList.add('expanded');
        hasExpanded = true;
        
        // Store in sessionStorage that button has expanded
        sessionStorage.setItem('buttonExpanded', 'true');
      }, 800);
    }
  }
  
  // Check if button has already expanded in this session
  if (sessionStorage.getItem('buttonExpanded') !== 'true') {
    // Initial check
    checkButtonVisibility();
    
    // Listen for scroll events
    window.addEventListener('scroll', checkButtonVisibility);
  }
  
  // Button click handler
  floatingBtn.addEventListener('click', function() {
    // Scroll to the top of the portfolio section
    document.querySelector('.portfolio-section').scrollIntoView({ 
      behavior: 'smooth' 
    });
    
    // Optional: Trigger the "All" filter
    const allFilter = document.querySelector('.filter-btn[data-filter="all"]');
    if (allFilter) {
      allFilter.click();
    }
  });
});


document.addEventListener('DOMContentLoaded', function() {
    const blogCards = document.querySelectorAll('.blog-card');
    
    const elementInView = (el, dividend = 1) => {
        const elementTop = el.getBoundingClientRect().top;
        return (
            elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend
        );
    };
    
    const displayScrollElement = (element) => {
        element.classList.add('is-visible');
    };
    
    const handleScrollAnimation = () => {
        blogCards.forEach((el, index) => {
            if (elementInView(el, 1.2)) {
                setTimeout(() => {
                    displayScrollElement(el);
                }, index * 200);
            }
        });
    };
    
    // Initial check
    handleScrollAnimation();
    
    // Listen for scroll events
    window.addEventListener('scroll', handleScrollAnimation);
});