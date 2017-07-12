$(document).ready(function(){
	$('.interest').live('click', function(event) {
		var isLogin = $('meta[name=isLogin]').attr('content');

		if(isLogin == 'false'){
			$('.ui.small.modal').modal('show');
			return false;
		}

		var tag_id = $(this).attr('tag_id');
		var url = '';
		var that = $(this);

		if(!$(this).hasClass('basic')) {
			url = basePath + '/follow/tag/do/';
		}
		else {
			url = basePath + '/follow/tag/undo/';
		}

		$.ajax({
			url: url,
			type: 'POST',
			dataType: 'json',
			data: { tag_id: tag_id }
		})
		.done(function(data) {
			if(SUCCESS_INTEREST == data.status) {
				$(that).text('已关注');
				$(that).removeClass('yellow');
				$(that).removeClass('inverted');
				$(that).addClass('basic');
			} else if(SUCCESS_INTEREST_UNDO == data.status) {
				$(that).text('+关注');
				$(that).removeClass('basic');
				$(that).addClass('yellow');
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