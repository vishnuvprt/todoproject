$(document).ready(function() {
    var newPasswordInput = $('#yourPassword');
    var confirmPasswordInput = $('#yourCPassword');
    var saveButton = $('#saveButton');
    var pmis = $('#pmis');
    pmis.hide();

    function updateSaveButtonState() {
        var newPassword = newPasswordInput.val();
        var confirmPassword = confirmPasswordInput.val();

        if (newPassword !== confirmPassword) {
            pmis.show();
            saveButton.prop('disabled', true);
        } else {
            pmis.hide();
            saveButton.prop('disabled', false);
        }
    }

    newPasswordInput.on('input', updateSaveButtonState);
    confirmPasswordInput.on('input', updateSaveButtonState);

    $('form[id="cpform"]').validate({
        rules: {
            
            oldpassword:{
                required: true,

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
