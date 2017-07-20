$(document).ready(function(){

$("#logo").click(function() {
    $('html, body').animate({
        scrollTop: $("#hero-block").offset().top
    }, 1000);
});

$("#project-button").click(function() {
    $('html, body').animate({
        scrollTop: $("#project").offset().top
    }, 1000);
});

$("#team-button").click(function() {
    $('html, body').animate({
        scrollTop: $("#team").offset().top
    }, 1000);
});


$(window).scroll(function(){
 	function elementScrolled(elem)
 	{
		var docViewTop = $(window).scrollTop();
		var docViewBottom = docViewTop + $(window).height();
		var elemTop = $(elem).offset().top;
		return ((elemTop <= docViewBottom) && (elemTop >= docViewTop));
	}
	  
	if(elementScrolled("#project")) {
		$("#project #img1").show(1500);
//		$("#project #img2").show(2000);
		$("#project #img2").css("opacity", "1");
		$("#project #text1").css("opacity", "1");
		$("#project #text2").css("opacity", "1");
	}
});

$("#quazi")
	.mouseenter(function(){
		$(this).css("background-color", "red");
	})
	.mouseleave(function(){
		$(this).css("background-color", "white");
	})
;

var allowedKeys = {
  37: 'left',
  38: 'up',
  39: 'right',
  40: 'down',
  65: 'a',
  66: 'b'
};

// the 'official' Konami Code sequence
var konamiCode = ['up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a'];

// a variable to remember the 'position' the user has reached so far.
var konamiCodePosition = 0;

// add keydown event listener
document.addEventListener('keydown', function(e) {
  // get the value of the key code from the key map
  var key = allowedKeys[e.keyCode];
  // get the value of the required key from the konami code
  var requiredKey = konamiCode[konamiCodePosition];

  // compare the key with the required key
  if (key == requiredKey) {

    // move to the next key in the konami code sequence
    konamiCodePosition++;

    // if the last key is reached, activate cheats
    if (konamiCodePosition == konamiCode.length)
      activateCheats();
  } else
    konamiCodePosition = 0;
});

function activateCheats() {
  window.location = "https://www.youtube.com/embed/mwEfTCWjrg8?rel=0&autoplay=1";
}


});
