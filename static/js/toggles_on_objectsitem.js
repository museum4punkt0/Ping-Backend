$(document).ready(function () {
    function toogle_author(value){
        if (value == true) {
            $('.author').show(300);
        } else {
            $('.author').hide(300);
        }
    }
    toogle_author($('#id_vip').prop("checked"));
    $('#id_vip').on('change', function (event) {
        toogle_author($(this).prop("checked"))
    });



    function toogle_chat_line(value){
        if (value == 'multichoice') {
            $("#id_chat_designer-0-single_line-0-multichoice" ).prop( "disabled", false );
            $('#id_chat_designer-0-single_line-0-redirect').val(0);
            $("#id_chat_designer-0-single_line-0-redirect" ).hide(300);

        } else {
            $("#id_chat_designer-0-single_line-0-redirect" ).prop( "disabled", false );
            $("#id_chat_designer-0-single_line-0-multichoice" ).prop( "disabled", true );
            $("#id_chat_designer-0-single_line-0-multichoice option:selected").removeAttr("selected");
            $("#id_chat_designer-0-single_line-0-redirect" ).show(300);
        }
    }

    toogle_chat_line($('#id_chat_designer-0-single_line-0-line_type option:selected').val())
    $('#id_chat_designer-0-single_line-0-line_type').on('change', function (event) {
        toogle_chat_line($(this).find(":selected").val())
    });
});
