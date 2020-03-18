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


    function toogle_chat_line(value, line_num=0){
        var multi = '[id$=' + (line_num) + '-multichoice' + ']' 
        var red = '[id$=' + (line_num) + '-redirect' + ']' 
        if (value == 'multichoice') {
            $(multi).prop( "disabled", false );
            $(red).val(0);
            $(red).hide(300);

        } else {
            $(red).prop( "disabled", false );
            $(multi).prop( "disabled", true );
            $(multi + 'option:selected').removeAttr("selected");
            $(red).show(300);
        }
    }

    toogle_chat_line($("[id$=line_type] option:selected").val())
    $('[id$=line_type]').on('change', function (event) {
        var line_num = this.id.split('-').slice(-2)[0]
        toogle_chat_line($(this).find(":selected").val(), line_num=line_num)
    });
});
