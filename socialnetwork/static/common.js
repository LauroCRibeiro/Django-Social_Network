$(document).ready(function(){
    $(".change-image").hide();
    $(".left-image").hover(function(){
        $(".change-image").toggle();
    });
});