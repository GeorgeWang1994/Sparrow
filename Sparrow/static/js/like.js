$(document).ready(function(){
	$('.heart.icon').live('click', function(){
		var isLogin = $('meta[name=isLogin]').attr('content');
		if(isLogin == 'false') {
			$('.ui.small.modal.login-tip').modal('show');
			return false;
		}

		var author = $(this).attr('author');
		var object_type = $(this).attr('object_type');
		var object_id = $(this).attr('object_id');
		var url = basePath + "/like";
		var like_count = parseInt($(this).next().text());

		//已经喜欢 点击取消喜欢
		if($(this).hasClass('red')){
			url += '/undo/';
		} 
		//还未喜欢 点击喜欢
		else{
			url += '/do/';
		}

		$.ajax({
			url: url,
			type: 'POST',
			dataType: 'json',
			data:{
				author:author,
				object_type: object_type,
				object_id: object_id
			}
		})
		.success(function(data){
			if(SUCCESS_POST_LIKE == data.status || SUCCESS_ALBUM_LIKE == data.status) {
				$(this).addClass('red');
				$(this).next().text(like_count+1);
			}
			else if(SUCCESS_POST_UNLIKE == data.status || SUCCESS_ALBUM_UNLIKE == data.status) {
				$(this).removeClass('red');
				$(this).next().text(like_count-1);
			}
			else {
				alert("服务器出错了")
			}
		})
	});
});