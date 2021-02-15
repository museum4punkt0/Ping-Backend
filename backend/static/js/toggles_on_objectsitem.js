function toogle_chat_line(value, line_num=null){
    var multi = '[id$=' + (line_num) + '-multichoice' + ']';
    var red = '[id$=' + (line_num) + '-redirect' + ']';
    var poll = '[id$=' + (line_num) + '-poll' + ']';

    if (value == 'multichoice') {
        $(multi).prop( "disabled", false );
        $(red).val(0).hide(300);
        $(poll).show(300);
    } else {
        $(red).prop( "disabled", false ).show(300);
        $(multi).prop( "disabled", true );
        $(multi + 'option:selected').removeAttr("selected");
        $(poll).prop('checked', false).hide(300);
    }
}


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


    $.each($("[id$=line_type]"), function( index, value ){
        var line_num = value.id.split('-').slice(-2)[0]
        toogle_chat_line(value.selectedOptions[0].value, line_num=line_num)
    });

});

$(document).on('click', '[id$=line_type]', function(){
    var line_num = this.id.split('-').slice(-2)[0]
    toogle_chat_line($(this).find(":selected").val(), line_num)
});
