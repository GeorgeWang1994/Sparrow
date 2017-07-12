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
        plainPaste: true,
        imageButtons: ['display', 'align', "linkImage", "replaceImage", "removeImage"],
        imageUploadURL: "/album/upload/postphoto",
        imageUploadParam: "uploader_input",
        imageUploadParams: {csrfmiddlewaretoken: getCookie('csrftoken')}
    });

    $('#send').click(function() {
        var that = this;
        $(this).addClass('loading');
        var title = $('#title').val();
        var content = $('#content').val();

        var visible_status = $('input[name="visible_status"]:checked').val();
        var comment_status = $('input[name="comment_status"]:checked').val();
        var id = $('meta[name=id]').attr('content');

        $.ajax({
            url: basePath + '/post/editpost/' + id +'/',
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
            //var author = data.post.post_author;
            switch (status) {
                case SUCCESS_POST_UPDATE:
                    self.location = basePath;
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