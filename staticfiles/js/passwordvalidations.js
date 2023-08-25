$(document).ready(function() {
    const newPasswordInput = document.getElementById('yourPassword');
    const confirmPasswordInput = document.getElementById('yourCPassword');
    const saveButton = document.getElementById('saveButton');
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

    $('form[id="cpform"]').validate({
        rules: {
            oldpassword: {
                required: true,
            },
            newpassword: {
                required: true,
                minlength: 8,
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$/,
            },
            confirmpassword: {
                equalTo: '#id_newpassword',
            },
        },
        messages: {
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
        }
    });
});
