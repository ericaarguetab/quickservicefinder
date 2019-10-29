$(function(){
    $('#btnRegisterService').click(function(){
        showElem('loader');
        $.ajax({
            url: '/newService',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
                if(response.responseCode == 200) {
                    $('#toastContent').html(response.responseMessage);
                    $('input[type=text]').val('');
                    $('select').val('default');
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