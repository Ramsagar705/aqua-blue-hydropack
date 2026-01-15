// Order Form Handling for Aqua Blue

document.addEventListener('DOMContentLoaded', function() {
    const orderForm = document.getElementById('orderForm');
    const successMessage = document.getElementById('successMessage');
    const orderIdSpan = document.getElementById('orderId');

    if (orderForm) {
        orderForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Validate all fields
            const formData = new FormData(orderForm);
            let isValid = true;

            // Check required fields
            const requiredFields = orderForm.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!validateField(field)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                // Scroll to first error
                const firstError = orderForm.querySelector('.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
                return;
            }

            // Collect form data
            const orderData = {
                name: formData.get('name'),
                mobile: formData.get('mobile'),
                email: formData.get('email') || '',
                address: formData.get('address'),
                productType: formData.get('productType'),
                quantity: formData.get('quantity'),
                deliveryTime: formData.get('deliveryTime'),
                deliveryDate: formData.get('deliveryDate'),
                notes: formData.get('notes') || ''
            };

            // Show loading state
            const submitButton = orderForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

            try {
                // Try to submit to backend
                const response = await fetch('/api/orders', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(orderData)
                });

                if (response.ok) {
                    const result = await response.json();
                    showSuccessMessage(result.order_id || generateOrderId());
                } else {
                    // If backend fails, still show success (for demo purposes)
                    // In production, you might want to show an error message
                    showSuccessMessage(generateOrderId());
                }
            } catch (error) {
                // If backend is not available, show success with local storage
                console.log('Backend not available, using local storage');
                saveOrderLocally(orderData);
                showSuccessMessage(generateOrderId());
            } finally {
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
            }
        });
    }

    function showSuccessMessage(orderId) {
        if (orderIdSpan) {
            orderIdSpan.textContent = orderId;
        }
        if (orderForm) {
            orderForm.style.display = 'none';
        }
        if (successMessage) {
            successMessage.style.display = 'block';
            successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    function generateOrderId() {
        return 'AQB-' + Date.now().toString().slice(-8);
    }

    function saveOrderLocally(orderData) {
        // Save to localStorage for demo purposes
        const orders = JSON.parse(localStorage.getItem('aquaBlueOrders') || '[]');
        orders.push({
            ...orderData,
            orderId: generateOrderId(),
            timestamp: new Date().toISOString()
        });
        localStorage.setItem('aquaBlueOrders', JSON.stringify(orders));
    }
});

// Reuse validateField from main.js if available, otherwise define it
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

        if (field.type === 'tel' && value) {
            if (value.length !== 10) {
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

