$(document).ready(function(){
	$('#pencil').click(function() {
		var id = $('meta[name=id]').attr('content');
		self.location = basePath + '/post/editpost/'+id+'/';
	});

	$('#like').click(function() {
		var isLogin = $('meta[name=isLogin]').attr('content');
		if(isLogin == 'false'){
			$('.ui.small.modal.login-tip').modal('show');
			return false;
		}
		
		var object_type = $('meta[name=type]').attr('content');
		var object_id = $('meta[name=id]').attr('content');
		var author = $('meta[name=author]').attr('content');
		var url = basePath+"/like";

		if(object_type == 'post') {
			object_type = 1;
		}
		else if(object_type == 'album') {
			object_type = 2;
		} else {
			return;
		}		

		if($(this).hasClass('empty')){
			url += '/do/';
			$(this).removeClass().addClass('red heart icon');
		}
		else {
			url += '/undo/';
			$(this).removeClass().addClass('empty red heart icon');
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
			if(SUCCESS_POST_LIKE == data.status) {
				$(this).addClass('red');
			}
			else if(SUCCESS_POST_UNLIKE == data.status) {
				$(this).removeClass('red');
			}
			else {
				return
			}
		})
	});

	$('#trash').live('click', function(){
		$('.trash-tip')
		  .modal({
		    closable  : true,
		    onDeny    : function(){
		      return true;
		    },
		    onApprove : function() {
				var id = $('meta[name=id]').attr('content');
				alert(id);
				$.ajax({
					url: basePath + '/post/delpost/'+id + '/',
					type: 'GET',
					dataType: 'json'
				})
				.done(function(data){
					if(data.status == SUCCESS_POST_DELETE) {
						self.location = basePath;
					}
				});
		    }
		  })
		  .modal('show');
	});
});