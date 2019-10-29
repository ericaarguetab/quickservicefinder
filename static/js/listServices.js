$(function(){
        $.ajax({
            url: '/listServices',
            type: 'GET',
            success: function(response){
                var div = $('div').attr('class', 'list-group').append($('<a>')
                .attr('class', 'list-group-item active')
                .append($('<h4>').attr('class', 'list-group-item-heading'),
                $('<p>').attr('class', 'list-group-item-text')));
                console.log(response);

                var subObj = JSON.parse(response);
                var subsector = '';

                $each(subObj, function(index, value){
                    subsector = $('div').clone();
                    $(subsector).find('h4').text(value.id);
                    $(subsector).find('p').text(value.sector);
                    $('.jumbotron').append(subsector)
                })
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