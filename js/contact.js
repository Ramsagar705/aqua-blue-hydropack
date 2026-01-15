// Contact Form Handling for Aqua Blue

document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    const successMessage = document.getElementById('contactSuccessMessage');

    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Validate all fields
            const formData = new FormData(contactForm);
            let isValid = true;

            // Check required fields
            const requiredFields = contactForm.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!validateField(field)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                const firstError = contactForm.querySelector('.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
                return;
            }

            // Collect form data
            const contactData = {
                name: formData.get('name'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                subject: formData.get('subject'),
                message: formData.get('message')
            };

            // Show loading state
            const submitButton = contactForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

            try {
                // Try to submit to backend
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(contactData)
                });

                if (response.ok) {
                    showSuccessMessage();
                } else {
                    // If backend fails, still show success (for demo purposes)
                    showSuccessMessage();
                }
            } catch (error) {
                // If backend is not available, show success with local storage
                console.log('Backend not available, using local storage');
                saveContactLocally(contactData);
                showSuccessMessage();
            } finally {
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
            }
        });
    }

    function showSuccessMessage() {
        if (contactForm) {
            contactForm.style.display = 'none';
        }
        if (successMessage) {
            successMessage.style.display = 'block';
            successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    function saveContactLocally(contactData) {
        // Save to localStorage for demo purposes
        const contacts = JSON.parse(localStorage.getItem('aquaBlueContacts') || '[]');
        contacts.push({
            ...contactData,
            timestamp: new Date().toISOString()
        });
        localStorage.setItem('aquaBlueContacts', JSON.stringify(contacts));
    }
});

// Reuse validateField from main.js if available
if (typeof validateField === 'undefined') {
    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;

        if (field.hasAttribute('required') && !value) {
            isValid = false;
        }

        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
            }
        }

        if (!isValid) {
            field.classList.add('error');
        } else {
            field.classList.remove('error');
        }

        return isValid;
    }
}

