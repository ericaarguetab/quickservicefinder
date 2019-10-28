function showElem(elemId){
    $('#' + elemId).fadeIn(500);
}

function hideElem(elemId){
    $('#' + elemId).fadeOut(500);
}

$(function(){
    $('.toast').toast('show');
});