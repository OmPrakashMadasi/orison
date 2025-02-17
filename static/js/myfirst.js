setTimeout(() => {
    const alertElement = document.getElementById('custom-alert');
    if (alertElement) {
        alertElement.classList.remove('show');
        alertElement.classList.add('fade');
    }
},10000);

// Registration Form Script


document.getElementById('registerForm').addEventListener('submit', function (e) {
        let isValid = true;

        // Clear all errors
        document.querySelectorAll('.error').forEach(err => err.textContent = '');

        // Form Validation
        const fields = [
            { id: 'username', errorId: 'usernameError', pattern: null, message: 'Username is required.' },
            { id: 'email', errorId: 'emailError', pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, message: 'Please enter a valid email address.' },
            { id: 'mobile', errorId: 'mobileError', pattern: /^[0-9]{10}$/, message: 'Please enter a valid 10-digit mobile number.' },
            { id: 'password', errorId: 'passwordError', pattern: /.{6,}/, message: 'Password must be at least 6 characters long.' },
        ];

        fields.forEach(field => {
            const input = document.getElementById(field.id);
            if (!input.value.trim() || (field.pattern && !field.pattern.test(input.value))) {
                document.getElementById(field.errorId).textContent = field.message;
                isValid = false;
            }
        });

        if (document.getElementById('password').value !== document.getElementById('confirmPassword').value) {
            document.getElementById('confirmPasswordError').textContent = 'Passwords do not match.';
            isValid = false;
        }

        // Prevent form submission if invalid
        if (!isValid) e.preventDefault();
    });
