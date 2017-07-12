/**
 * Created by wangdading on 17/6/13.
 */
$(document).ready(function() {
    $('#content').editable({
        language: 'zh_cn',
        inlineMode: false,
        autosave: true,
        autosaveInterval: 2500,
        spellcheck: true,
        pastePlain: true,
        imageButtons: ['display', 'align', "linkImage", "replaceImage", "removeImage"],
        imageUploadURL: "/album/upload/postphoto/",
        imageUploadParam: "uploader_input",
        imageUploadParams: {csrfmiddlewaretoken: getCookie('csrftoken')}
    });

    var a =

    $('#send').click(function() {
        var that = this;
        $(this).addClass('loading');
        var title = $('#title').val();
        var content = $('#content').val();

        var visible_status = $('input[name="visible_status"][checked]').val();
        var comment_status = $('input[name="comment_status"][checked]').val();

        $.ajax({
            url: basePath + '/post/newpost/',
            type: 'POST',
            dataType: 'json',
            data: {
                   content: content,
                   title: title,
                   tags: tags.join(' '),
                   visible_status: visible_status,
                   comment_status: comment_status,
                   csrfmiddlewaretoken: getCookie('csrftoken')
            }
        })
        .done(function(data) {
            $(that).removeClass('loading');
            var status = data.status;
            switch (status) {
                case SUCCESS_POST_CREATE:
                    self.location = '/';
                    break;
                default:
                    location.reload();
                    break;
            }
        })
        .fail(function() {
            console.log("error");
        })
        .always(function() {
            console.log("complete");
        });
    });

    $('#cancel').click(function(){
        $('.cancel-tip')
          .modal({
            closable  : true,
            onDeny    : function(){
              return true;
            },
            onApprove : function() {
                self.location = basePath;
            }
          })
          .modal('show');
    });
});