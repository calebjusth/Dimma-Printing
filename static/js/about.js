// Edit Mode Management
document.addEventListener('DOMContentLoaded', function() {
    const editModeToggle = document.getElementById('editModeToggle');
    const editPens = document.querySelectorAll('.section-edit-pen');
    const modalOverlay = document.getElementById('modalOverlay');
    const modalContainer = document.getElementById('modalContainer');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    const modalClose = document.getElementById('modalClose');
    const modalCancel = document.getElementById('modalCancel');
    const modalSave = document.getElementById('modalSave');
    
    let isEditMode = false;
    let currentSection = null;

    // Toggle edit mode
    if (editModeToggle) {
        editModeToggle.addEventListener('click', function() {
            isEditMode = !isEditMode;
            document.body.classList.toggle('edit-mode-active', isEditMode);
            
            if (isEditMode) {
                editModeToggle.innerHTML = '<i class="fas fa-times"></i><span>Exit Edit Mode</span>';
                editModeToggle.classList.add('active');
            } else {
                editModeToggle.innerHTML = '<i class="fas fa-pencil-alt"></i><span>Enter Edit Mode</span>';
                editModeToggle.classList.remove('active');
            }
        });
    }

    // Edit pen click handlers
    editPens.forEach(pen => {
        pen.addEventListener('click', function() {
            if (!isEditMode) return;
            
            currentSection = this.dataset.section;
            openEditModal(currentSection);
        });
    });

    // Open edit modal
    function openEditModal(section) {
        modalTitle.textContent = `Edit ${section.replace('-', ' ')}`;
        loadFormForSection(section);
        modalOverlay.style.display = 'flex';
        setTimeout(() => {
            modalOverlay.classList.add('active');
            modalContainer.classList.add('active');
        }, 10);
    }

    // Close modal
    function closeModal() {
        modalOverlay.classList.remove('active');
        modalContainer.classList.remove('active');
        setTimeout(() => {
            modalOverlay.style.display = 'none';
            modalBody.innerHTML = '';
        }, 300);
    }

    // Close modal handlers
    modalClose.addEventListener('click', closeModal);
    modalCancel.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', function(e) {
        if (e.target === modalOverlay) closeModal();
    });

    // Load form for section via AJAX
    function loadFormForSection(section) {
        fetch(`/edit-section/${section}/`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            credentials: 'include'
        })
        .then(response => {
            if (response.status === 403 || response.status === 302) {
                window.location.href = '/admin/login/?next=' + encodeURIComponent(window.location.pathname);
                return;
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.type === 'list') {
                showListModal(section, data.items);
            } else {
                modalBody.innerHTML = data.form;
                initFormHandlers(section);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            modalBody.innerHTML = `<div class="alert alert-danger">Error loading form: ${error.message}</div>`;
        });
    }
    
    function showListModal(section, items) {
        let html = `<div class="list-management">
            <h4>Manage ${section.replace('-', ' ')}</h4>
            <button class="btn btn-primary mb-3" id="addNewItem">Add New</button>
            <ul class="list-group">`;
        
        items.forEach(item => {
            html += `<li class="list-group-item d-flex justify-content-between align-items-center">
                ${item.title || item.name}
                <div>
                    <button class="btn btn-sm btn-primary edit-item" data-id="${item.id}">Edit</button>
                    <button class="btn btn-sm btn-danger delete-item" data-id="${item.id}">Delete</button>
                </div>
            </li>`;
        });
        
        html += `</ul></div>`;
        modalBody.innerHTML = html;
        
        // Add event listeners
        document.getElementById('addNewItem').addEventListener('click', function() {
            loadItemForm(section);
        });
        
        document.querySelectorAll('.edit-item').forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = this.dataset.id;
                loadItemForm(section, itemId);
            });
        });
        
        document.querySelectorAll('.delete-item').forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = this.dataset.id;
                deleteItem(section, itemId);
            });
        });
    }
    
    function loadItemForm(section, itemId = null) {
        const url = itemId ? 
            `/edit-item/${section}/${itemId}/` : 
            `/edit-item/${section}/`;
            
        console.log('Loading item form from:', url);
        
        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            credentials: 'include'
        })
        .then(response => {
            if (response.status === 403 || response.status === 302) {
                window.location.href = '/admin/login/?next=' + encodeURIComponent(window.location.pathname);
                return;
            }
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`HTTP error! status: ${response.status}, response: ${text}`);
                });
            }
            return response.json();
        })
        .then(data => {
            modalBody.innerHTML = data.form;
            initFormHandlers(section, itemId);
        })
        .catch(error => {
            console.error('Error loading item form:', error);
            modalBody.innerHTML = `<div class="alert alert-danger">Error loading form: ${error.message}</div>`;
        });
    }
    
    function initFormHandlers(section, itemId = null) {
        const form = document.getElementById('editForm');
        if (form) {
            // Remove any existing submit event listeners
            const newForm = form.cloneNode(true);
            form.parentNode.replaceChild(newForm, form);
            
            // Remove any form action that might cause submission to wrong URL
            newForm.removeAttribute('action');
            
            // Add new submit handler
            newForm.addEventListener('submit', function(e) {
                e.preventDefault();
                submitForm(this, section, itemId);
            });
            
            // Set up save button handler
            modalSave.onclick = function() {
                newForm.dispatchEvent(new Event('submit'));
            };
        } else {
            console.error('Form not found');
        }
    }
    
    function submitForm(form, section, itemId = null) {
        const formData = new FormData(form);
        
        // Add CSRF token to FormData
        const csrfTokenInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfTokenInput) {
            formData.set('csrfmiddlewaretoken', csrfTokenInput.value);
        } else {
            formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        }
        
        console.log('Submitting form for section:', section, 'itemId:', itemId);
        
        // Determine the correct URL
        let url;
        if (section === 'hero' || section === 'cta') {
            url = `/edit-section/${section}/`;
        } else {
            if (itemId) {
                url = `/edit-item/${section}/${itemId}/`;
            } else {
                url = `/edit-item/${section}/`;
            }
        }
        
        console.log('Submitting to:', url);
        
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
            credentials: 'include'
        })
        .then(response => {
            if (response.status === 403 || response.status === 302) {
                window.location.href = '/admin/login/?next=' + encodeURIComponent(window.location.pathname);
                return;
            }
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`HTTP error! status: ${response.status}, response: ${text}`);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Changes saved successfully!');
                closeModal();
                location.reload();
            } else if (data.errors) {
                displayFormErrors(data.errors);
            } else {
                alert('Error saving changes: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error submitting form:', error);
            alert('Error saving changes: ' + error.message);
        });
    }
    
    function deleteItem(section, itemId) {
        if (!confirm('Are you sure you want to delete this item?')) return;
        
        fetch(`/edit-item/${section}/${itemId}/`, {
            method: 'DELETE',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            credentials: 'include'
        })
        .then(response => {
            if (response.status === 403 || response.status === 302) {
                window.location.href = '/admin/login/?next=' + encodeURIComponent(window.location.pathname);
                return;
            }
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`HTTP error! status: ${response.status}, response: ${text}`);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Item deleted successfully!');
                closeModal();
                location.reload();
            } else {
                alert('Error deleting item: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error deleting item:', error);
            alert('Error deleting item: ' + error.message);
        });
    }
    
    function displayFormErrors(errors) {
        let errorHtml = '<div class="alert alert-danger"><ul>';
        for (const field in errors) {
            errors[field].forEach(error => {
                errorHtml += `<li>${field}: ${error}</li>`;
            });
        }
        errorHtml += '</ul></div>';
        modalBody.insertAdjacentHTML('afterbegin', errorHtml);
    }
    
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

    // Scroll animation implementation
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
    
    const handleScrollAnimation = () => {
        scrollElements.forEach((el) => {
            if (elementInView(el, 1.2)) {
                displayScrollElement(el);
            }
        });
    };
    
    // Initial check
    handleScrollAnimation();
    window.addEventListener('scroll', handleScrollAnimation);
});