$(document).ready(function($) {

    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });

    $("#filtr").on("click", function(){
        $("#filtr-content").fadeToggle();
    });

});