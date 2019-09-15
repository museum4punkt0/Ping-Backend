$(document).ready(function () {
    function toogle_author(value){
        if (value == true) {
            $('.author').show();
        } else {
            $('.author').hide();
        }
    }
    toogle_author($('#id_vip').val());
    $('#id_vip').on('change', function (event) {
        console.log($(this).prop("checked"))
        toogle_author($(this).prop("checked"))
    });
});
