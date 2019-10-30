$(function(){
    $.ajax({
        url: '/listServices',
        type: 'GET',
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