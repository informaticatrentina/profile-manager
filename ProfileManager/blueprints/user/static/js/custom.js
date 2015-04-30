$(function($) {

    // helper function to fix the url prepending http
    function fixURL(url){
	var r = url.match(/^(https?:\/\/)?(.*)$/);
	return ((r[1] ? r[1] : 'http://') + r[2]);
    }

    // check for proper http in the url
    $("form").submit(function() {
        if (! $("#website").hasClass('hint')) {
	    $("#website").val(fixURL($("#website").val()));
	}
    });
    // check for max chars in textarea

    $('textarea').maxlength({
	'feedback' : '.charsLeft',
	'useInput' : true
    });

    $('#nickname').focusout(function() {
      var nickname = $.trim($('#nickname').val());
      if (nickname != '') {
        checkNickNameAvailability(nickname);
      }
    });
});

function  checkNickNameAvailability(nickname) {
  $.ajax({
    url: '/checknickname',
    data: {
      nickname: nickname,
      userid: $('#user-id').val()
    },
    type: 'GET',
    success: function(response) {
      if (response.available === 'Y') {
        $('#nickname-availability').html('Nickname available').css('color', 'green');
        $('#nickname-availability').show();
        $('#update-profile').removeAttr('disabled');
      } else {
         $('#update-profile').attr('disabled', 'disabled');
        $('#nickname-availability').show();
        $('#nickname-availability').html('Nickname is already in use. Please choose another.').css('color', 'red');
        ;
      }
    },
    error: function() {
      $('#update-profile').attr('disabled', 'disabled');
      $('#nickname-availability').hide();
      $('#nickname-availability').html('');
    }
  });
}
