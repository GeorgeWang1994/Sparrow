$(document).ready(function(){
	$('#registerBtn').live('click', function() {
		//clear tips
		$('div.error').removeClass('error');
		$('span.tip').text('');

		var username = $('#username').val();
		var email = $('#email').val();
		var password = $('#password').val();
		var cfmPwd = $('#cfmPwd').val();

		if (username === "") {
			$('#usernameTip').text('请输入用户名');
			$('#username').parent('div.field:first').addClass('error');
			return ;
		}
		if (email === "") {
			$('#emailTip').text('请输入邮箱地址');
			$('#email').parent('div.field:first').addClass('error');
			return ;
		}
		if (password === "") {
			$('#passwordTip').text('请输入密码');
			$('#password').parent('div.field:first').addClass('error');
			return ;
		}
		if (cfmPwd == "") {
			$('#cfmPwdTip').text('请再次输入密码');
			$('#cfmPwdTip').parent('div.field:first').addClass('error');
			return ;
		}
		else if (password !== cfmPwd) {
			$('#passwordTip').text('密码输入不一致');
			$('#password').parent('div.field:first').addClass('error');
			$('#cfmPwd').parent('div.field:first').addClass('error');
			return ;
		}

		var that = this;
		$(this).addClass('loading');

		$.ajax({
			url: basePath+'/account/signup/',
			type: 'POST',
			dataType: 'json',
			data: { username:username,
					email: email,
				   password: password,
				   cfmPwd: cfmPwd}
		})
		.success(function(data) {
			$(that).removeClass('loading');
			if(data.status == SUCCESS_ACCOUNT_REG) {
				// self.location = basePath + 'account/activation/?email='+email;
				// $.ajax({
				// 	url: basePath+'account/activation/',
				// 	type: 'POST',
				// 	dataType: 'json',
				// 	data: {
				// 		email: email
				// 	}
				// }).success(function (data) {
				//
				// });
			} else { //error
				var status = data.status;
				switch(status.charAt(2)) {
					case '0':  //username error
						if(status === ERROR_USERNAME_EXIST) { //user name exist
							username = '';
							$('#usernameTip').text('用户名已存在');
						} else if(status === ERROR_USERNAME_EMPTY) { //user name empty
							$('#usernameTip').text('请输入用户名');
						}
						$('#username').parent('div.field:first').addClass('error');
						break;

					case '1':  //email error
						if(status == ERROR_EMAIL_EXIST) {
							$('#emailTip').text('邮箱已注册 <a href="#">登录</a>');
						} else if(status === ERROR_EMAIL_EMPTY) {
							$('#emailTip').text('请输入邮箱地址');
						} else if(status === ERROR_EMAIL_FORMAT) {
							$('#emailTip').text('请输入正确的邮箱地址');
						} 
						$('#email').parent('div.field:first').addClass('error');
						break;

					case '2':  //password error
						if(status == ERROR_PWD_EMPTY) {  //password empty
							$('#passwordTip').text('请输入密码');
						}
						$('#password').parent('div.field:first').addClass('error');
						break;

					case '3':  //confirm password error
						if(status == ERROR_CFMPWD_EMPTY) {
							$('#cfmPwdTip').text('请再次输入密码');
							$('#cfmPwdTip').parent('div.field:first').addClass('error');
						} else if(status == ERROR_CFMPWD_NOTAGREE) {
							$('#passwordTip').text('密码输入不一致');
							$('#password').parent('div.field:first').addClass('error');
							$('#cfmPwd').parent('div.field:first').addClass('error');
						}
						break;
					case '4':
						if(status == ERROR_ACCOUNT_INACTIVE) {
							var activationUrl = basePath + '/account/activation/?email='+email;
							$('#emailTip').html('<a href="'+activationUrl+'">已注册,请激活</a>');
						}
						$('#email').parent('div.field:first').addClass('error');
						break;
					default:
						break;
				}
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