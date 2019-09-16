$(document).ready(function () {
    function toogle_author(value){
        if (value == true) {
            $('.author').show();
        } else {
            $('.author').hide();
        }
    }
    toogle_author($('#id_vip').prop("checked"));
    $('#id_vip').on('change', function (event) {
        toogle_author($(this).prop("checked"))
    });
});
