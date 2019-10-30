$(function(){
        $.ajax({
            url: '/getSubsector',
            type: 'GET',
            success: function(response){
                if(response.responseCode == 200) {
                    var div = $('<div>').attr('class', 'list-group').append($('<a>')
                    .attr('class', 'list-group-item active')
                    .append($('<h4>').attr('class', 'list-group-item-heading'),
                    $('<p>').attr('class', 'list-group-item-text')));
                    console.log(response);

                    var subsector = '';
                    $(response.responseObject).each(function(index, item){
                        subsector = $(div).clone();
                        $(subsector).find('h4').text(item.sector);
                        $(subsector).find('p').text(item.name);
                        $('.jumbotron').append(subsector);
                    })
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