$(function(){
    $('#btnRegisterService').click(function(){
        showElem('loader');
        $.ajax({
            url: '/newservice',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
                if(response.responseCode == 200) {
                    $('#toastContent').html(response.responseMessage);
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