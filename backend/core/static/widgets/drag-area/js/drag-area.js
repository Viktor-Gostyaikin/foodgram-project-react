jQuery(function($) {
    $('input[type="file"]').each(function(index,elem){
        $elem_id = $(elem).attr('id');
        $drag_area_id = 'drag-area-for-' + $elem_id;

        $(elem).css('display', 'none');
        $(elem).next('.help').css('display', 'none');
        $(elem).after('<div id="' + $drag_area_id + '" class="drag-area">' +
                            gettext('Drag and drop or click to select') +
                      '</div>');
    
        $('html').on('dragover', function(e) {
            e.preventDefault();
            e.stopPropagation();
            $('#' + $drag_area_id).text(gettext('Drag here'));
        });

        $('html').on('drop', function(e) { 
            e.preventDefault();
            e.stopPropagation();
        });

        $('#' + $drag_area_id).on('dragenter dragover', function (e) {
            e.stopPropagation();
            e.preventDefault();
            $(this).text(gettext('Drop here'));
        });

        $('#' + $drag_area_id).on('drop', function (e) {
            elem.files = e.originalEvent.dataTransfer.files;
            $('#' + $drag_area_id).prev('.drag-area-file-name').remove();
            if(elem.files.length != 0) {
                $('#' + $drag_area_id).before('<p class="drag-area-file-name">' +
                                                    gettext('Selected file: ') + elem.files[0].name + 
                                              '</p>');
            }
            e.stopPropagation();
            e.preventDefault();
            $(this).text(gettext('Drag and drop or click to select'));
        });

        $('#' + $drag_area_id).on('click', function (e) {
            $(elem).click();
        });

        $(elem).on('change', function (e) {
            $('#' + $drag_area_id).prev('.drag-area-file-name').remove();
            if(elem.files.length != 0) {
                $('#' + $drag_area_id).before('<p class="drag-area-file-name">' +
                                                    gettext('Selected file: ') + elem.files[0].name + 
                                              '</p>');
            }
        });
    });
});