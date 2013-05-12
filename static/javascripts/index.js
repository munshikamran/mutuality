
(function($) {

var carouselNumber = 1;
var count = 0;
var carouselInterval;
 $(window).on('load', function(){
	toggleMagnifyStates(0);
	carouselInterval = setInterval (function() {
		toggleMagnifyStates(carouselNumber);
		carouselNumber = carouselNumber + 1;
		if (carouselNumber === 3) {
			carouselNumber = 0
		}
	}, 3000);	
});

var toggleMagnifyStates = function (eq) {
	$('#homepage-ellipse').find('a').removeClass("active-ellipse");
	$('#homepage-ellipse a').eq(eq).addClass("active-ellipse");
	if (eq === 0) {
		$('#homepage-info-headline h6').html("No More Strangers")
		$('#homepage-info-body').html("Everyone you see is a friend-of-a-friend")
		$("#homepage-magnify").removeClass("ask-about-magnify");
		$("#homepage-magnify").removeClass("beacon-magnify");
		$("#homepage-magnify").addClass("meet-people-magnify");
	} else if (eq === 1) {
		$('#homepage-info-headline h6').html("Trust <em>and</em> Verify")
		$('#homepage-info-body').html("Ask a mutual friend about anyone to learn more")
		$("#homepage-magnify").removeClass("beacon-magnify");
		$("#homepage-magnify").removeClass("meet-people-magnify");
		$("#homepage-magnify").addClass("ask-about-magnify");
	} else {
		$('#homepage-info-headline h6').html("Connect with &quot;Beacons&quot;")
		$('#homepage-info-body').html("From Poker to Dog-walking, to Karaoke -- do fun things with people you trust")
		$("#homepage-magnify").removeClass("meet-people-magnify");
		$("#homepage-magnify").removeClass("ask-about-magnify");
		$("#homepage-magnify").addClass("beacon-magnify");
	}
}

$('#homepage-ellipse').on('click', 'a', function(){
	var eq = $(this).index();
	toggleMagnifyStates(eq);
	window.clearInterval(carouselInterval);
});

/* End Main Code */

})(jQuery);