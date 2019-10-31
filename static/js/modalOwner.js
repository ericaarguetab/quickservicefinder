  $(function(){
    $('.btnSendRequest').click(function(){
        var boton = $(this);
 
        showElem('loader');
        $.ajax({
            url: '/modalRequest',
            data: $(boton).parents('.modal').find('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
                if(response.responseCode == 200) {
                    $('#toastContent').html(response.responseMessage);
                    $(boton).parents('.modal').modal('hide');
                    $(boton).parents('.modal').find('textarea').val('');
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