$(document).ready(function() {
    const email = document.getElementById('yourEmail');
    const newPasswordInput = document.getElementById('yourPassword');
    const confirmPasswordInput = document.getElementById('yourcPassword');
    const saveButton = document.getElementById('submitBtn');
    const pmis = document.getElementById('pmis');

    function updateSaveButtonState() {
        const newPassword = newPasswordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (newPassword !== confirmPassword) {
            pmis.style.display = 'block';
            saveButton.disabled = true;
        } else {
            pmis.style.display = 'none';
            saveButton.disabled = false;
        }
    }

    newPasswordInput.addEventListener('input', updateSaveButtonState);
    confirmPasswordInput.addEventListener('input', updateSaveButtonState);

    $('form[id="signupForm"]').validate({
        rules: {
            
            name:{
                required: true,

            },

            email:{

                required:true,
                pattern: /^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/,   

            },
            phone: {
                required: true,
                number: true,
                minlength: 10,
            },


            oldpassword: {
                required: true,
                minlength: 8,
            },
            newpassword: {
                required: true,
                minlength: 8,
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$/,
            },
            confirmpassword: {
                equalTo: '#yourPassword',
            },
        },
        messages: {

            email:{
                required:'Please enter your email',
                pattern:'Invalid email'
            
            },

            phone: {
                required: 'Please enter your phone number',
                number: 'Please enter a valid phone number',
                minlength: 'Phone number must be at least 10 digits',
            },

            oldpassword: {
                minlength: 'Password must be at least 8 characters long',
            },
            newpassword: {
                minlength: 'Password must be at least 8 characters long',
                pattern: 'Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character (@$!%*?&)',
            },
            confirmpassword: {
                equalTo: 'Passwords do not match',
            },
        },
        submitHandler: function(form) {
            form.submit();

            const emailValue = email.value;
            $.ajax({
                url: '/myapp/check_email_uniqueness/', // Change to your server endpoint
                type: 'GET',
                data: { email: emailValue },
                dataType: 'json',
                success: function(response) {
                    if (response.is_unique) {
                        form.submit();
                    } else {
                        alert('Email is already taken. Please choose another.');
                        

                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error checking email uniqueness:', error);
                }
            });
        }
    });


});
