$(document).ready(function () {
    $('form[id="editprofileform"]').validate({
        rules: {
            name: {
                required: true,
            },
            phone: {
                required: true,
                number: true,
                minlength: 10, 
                maxlength: 10, 
            },
        },
        messages: {
            name: {
                required: 'Please enter your name',
            },
            phone: {
                required: 'Please enter your phone number',
                number: 'Please enter a valid phone number',
                minlength: 'Phone number must be at least 10 digits',
            },
        },
        submitHandler: function (form) {
            form.submit();
        }
    });
});