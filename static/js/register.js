$(function(){
    $('#btnRegisterCustomer').click(function(){
        showElem('loader');
        $.ajax({
            url: '/registerCustomer',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
                if(response.responseCode == 200) {
                    $('#toastContent').html(response.responseMessage);
                }
                else if(response.responseCode == 400){
                    $('#toastContent').html(response.responseMessage);
                }
                else if(response.responseCode == 500){
                    $('#toastContent').html("Error: " + response.responseMessage);
                }
            },
            error: function(error){
                console.log(error);
                $('#toastContent').html('Ha ocurrido un error inesperado.');
            },
            complete: function() {
                hideElem('loader');
                $('.toast').toast('show');
            }
        });
    });

    $('#btnRegisterOwner').click(function(){
        showElem('loader');
        $.ajax({
            url: '/registerOwner',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
                if(response.responseCode == 200) {
                    $('#toastContent').html(response.responseMessage);
                }
                else if(response.responseCode == 400){
                    $('#toastContent').html(response.responseMessage);
                }
                else if(response.responseCode == 500){
                    $('#toastContent').html("Error: " + response.responseMessage);
                }
            },
            error: function(error){
                console.log(error);
                $('#toastContent').html('Ha ocurrido un error inesperado.');
            },
            complete: function() {
                hideElem('loader');
                $('.toast').toast('show');
            }
        });
    });
});






