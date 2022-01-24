jQuery(function($) {
    $("input[type='password']").each(function(index, elem){
        $(elem).addClass('vTextField')
        $(elem).after('<a href="#" id="'+$(elem).attr('id')+'-link" class="password-view-control"></a>');
    });

    $('body').on('click', '.password-view-control', function(){
        let clicked_input_id = $(this).attr('id').replace('-link', '');
        if ($('#'+ clicked_input_id).attr('type') == 'password'){
            $(this).addClass('no-view');
            $('#'+ clicked_input_id).attr('type', 'text');
        } else {
            $(this).removeClass('no-view');
            $('#'+ clicked_input_id).attr('type', 'password');
        }
        return false;
    });
});