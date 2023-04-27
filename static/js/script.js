$(document).ready(function() {
    $('.messages .close').on('click', function() {
        $(this).parent().fadeOut();
    });
});
