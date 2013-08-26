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

});
