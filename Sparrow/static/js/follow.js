$(document).ready(function(){
	$('.follow').live('click', function(event) {
		var isLogin = $('meta[name=isLogin]').attr('content');
		if(isLogin == 'false') {
			$('.ui.small.modal.login-tip').modal('show');
			return false;
		}
		
		var following_user_id = $(this).attr('following');
		var url = '';
		var that = $(this);

		if(!$(this).hasClass('basic')) {
			url = basePath + '/follow/do/';
		} else {
			url = basePath + '/follow/undo/';
		}

		$.ajax({
			url: url,
			type: 'POST',
			dataType: 'json',
			data: { follow_id: following_user_id }
		})
		.done(function(data) {
			if(SUCCESS_FOLLOW == data.status) {
				$(that).text('已关注');
				$(that).removeClass('yellow');
				$(that).removeClass('inverted');
				$(that).addClass('basic');
			} else if(SUCCESS_FOLLOW_UNDO == data.status) {
				$(that).text('+关注');
				$(that).removeClass('basic');
				$(that).addClass('yellow');
			}
			else if (ERROR_HAVE_FOLLOWED == data.status) {
				alert("你已经关注了");
			}
			else {
				alert("出了点出错误");
			}
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
	});
});