// Handle flash messages
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Initialize ticket type management
    initTicketTypeManager();
});

// Form validation
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('border-red-500');
        } else {
            input.classList.remove('border-red-500');
        }
    });

    return isValid;
}

// Add form validation to all forms
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!validateForm(this)) {
            e.preventDefault();
            alert('Please fill in all required fields.');
        }
    });
});

// Password strength indicator
const passwordInput = document.querySelector('input[type="password"]');
if (passwordInput) {
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        const strength = calculatePasswordStrength(password);
        updatePasswordStrengthIndicator(strength);
    });
}

function calculatePasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/)) strength++;
    if (password.match(/[A-Z]/)) strength++;
    if (password.match(/[0-9]/)) strength++;
    if (password.match(/[^a-zA-Z0-9]/)) strength++;
    return strength;
}

function updatePasswordStrengthIndicator(strength) {
    const indicator = document.getElementById('password-strength');
    if (indicator) {
        const strengthText = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong'];
        const strengthClass = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-green-500', 'bg-green-600'];
        
        indicator.textContent = strengthText[strength - 1];
        indicator.className = `px-2 py-1 text-xs text-white rounded ${strengthClass[strength - 1]}`;
    }
}

// Ticket Type Management
function initTicketTypeManager() {
    const addTicketBtn = document.getElementById('add-ticket-type');
    const ticketTypesContainer = document.getElementById('ticket-types');
    
    if (addTicketBtn && ticketTypesContainer) {
        addTicketBtn.addEventListener('click', function() {
            const ticketTypeTemplate = `
                <div class="ticket-type bg-gray-50 p-4 rounded-lg mb-4">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="form-label">Ticket Name</label>
                            <input type="text" name="ticket_names[]" class="form-input" required>
                        </div>
                        <div>
                            <label class="form-label">Price ($)</label>
                            <input type="number" name="ticket_prices[]" class="form-input" min="0" step="0.01" required>
                        </div>
                        <div>
                            <label class="form-label">Quantity</label>
                            <input type="number" name="ticket_quantities[]" class="form-input" min="1" required>
                        </div>
                        <div>
                            <label class="form-label">Description</label>
                            <input type="text" name="ticket_descriptions[]" class="form-input">
                        </div>
                    </div>
                    <button type="button" class="mt-2 text-red-600 hover:text-red-800" onclick="removeTicketType(this)">
                        <i class="fas fa-trash"></i> Remove Ticket Type
                    </button>
                </div>
            `;
            
            ticketTypesContainer.insertAdjacentHTML('beforeend', ticketTypeTemplate);
        });
    }
}

function removeTicketType(button) {
    button.closest('.ticket-type').remove();
}

// Preview uploaded image
function previewImage(input) {
    const preview = document.getElementById('image-preview');
    if (preview && input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.style.backgroundImage = `url('${e.target.result}')`;
            preview.classList.remove('hidden');
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Initialize date pickers with min date
document.addEventListener('DOMContentLoaded', function() {
    const dateInputs = document.querySelectorAll('input[type="datetime-local"]');
    const today = new Date().toISOString().slice(0, 16);
    
    dateInputs.forEach(input => {
        input.min = today;
    });
});
