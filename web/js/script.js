$(document).ready(function(){

var imgCounter = 0;
var direction = "down";
$(".logo").click(function() {
    $('html, body').animate({
        scrollTop: $("#hero-block").offset().top
    }, 1000);
});

$(".project-button").click(function() {
    $('html, body').animate({
        scrollTop: $("#project").offset().top
    }, 1000);
});

$(".team-button").click(function() {
    $('html, body').animate({
        scrollTop: $("#team").offset().top
    }, 1000);
});
$(".demo-day-button").click(function() {
    $('html, body').animate({
        scrollTop: $("#demo-day").offset().top
    }, 1000);
});

$(".citations-button").click(function() {
    $('html, body').animate({
        scrollTop: $("#citations").offset().top
    }, 1000);
});

//element animaitons triggered by scrolling points
$(window).scroll(function(){
 	function elementScrolled(elem)
 	{
		var docViewTop = $(window).scrollTop();
		var docViewBottom = docViewTop + $(window).height();
		var elemTop = $(elem).offset().top;
		return ((elemTop <= docViewBottom) && (elemTop >= docViewTop));
	}
	console.log(direction);	
	if(elementScrolled("#text2")){
		if(direction == "down"){	
			$(".menu-fixed").css("opacity", "0.9");
			direction = "up";
		}
	}
	if(elementScrolled(".menu")){
		if(direction == "up"){
			$(".menu-fixed").css("opacity", "0");
			direction = "down";
		}
	}
	  
	if(elementScrolled("#project")) {
		$("#project #img1").show(1500);
		$("#project #img2").css("opacity", "1");
		$("#project #text1").css("opacity", "1");
		$("#project #text2").css("opacity", "1");
	}
});

$("#quazi")
	.mouseenter(function(){
		$("#quazi .overlay").css("transition", "opacity 0.5s");
		$("#quazi .overlay").css("opacity", "0.7");
		$("#quazi .overlay p").html("Team Leader/Design Engineer<br><br>Elec");
	})
	.mouseleave(function(){
		$("#quazi .overlay").css("opacity", "0");
	})
;
$("#anuraag")
	.mouseenter(function(){
		$("#anuraag .overlay").css("transition", "opacity 0.5s");
		$("#anuraag .overlay").css("opacity", "0.7");
		$("#anuraag .overlay p").html("Computer Engineer/System Engineer<br><br>CEng");
	})
	.mouseleave(function(){
		$("#anuraag .overlay").css("opacity", "0");
	})
;
$("#kevin")
	.mouseenter(function(){
		$("#kevin .overlay").css("transition", "opacity 0.5s");
		$("#kevin .overlay").css("opacity", "0.7");
		$("#kevin .overlay p").html("Design Engineer/Financial Manager<br><br>CEng");
	})
	.mouseleave(function(){
		$("#kevin .overlay").css("opacity", "0");
	})
;
$("#trison")
	.mouseenter(function(){
		$("#trison .overlay").css("transition", "opacity 0.5s");
		$("#trison .overlay").css("opacity", "0.8");
		$("#trison .overlay p").html("Software Engineer/Web Developer<br><br>SEng");
	})
	.mouseleave(function(){
		$("#trison .overlay").css("opacity", "0");
	})
;
$("#ava")
	.mouseenter(function(){
		$("#ava .overlay").css("transition", "opacity 0.5s");
		$("#ava .overlay").css("opacity", "0.8");
		$("#ava .overlay p").html("Electrical Engineer/Presenter<br><br>Elec");
	})
	.mouseleave(function(){
		$("#ava .overlay").css("opacity", "0");
	})
;
$("#xiang")
	.mouseenter(function(){
		$("#xiang .overlay").css("transition", "opacity 0.5s");
		$("#xiang .overlay").css("opacity", "0.8");
		$("#xiang .overlay p").html("Electrical Engineer/Software Developer<br><br>Elec");
	})
	.mouseleave(function(){
		$("#xiang .overlay").css("opacity", "0");
	})
;

$("#button-left").click(function(){
	imgCounter--;
	if(imgCounter<0){
		imgCounter=5;
	}
	$("#img-gallery img").attr("src", "assets/img/demo"+imgCounter+".jpg");	
});
$("#button-right").click(function(){
	imgCounter++;
	if(imgCounter>5){
		imgCounter=0;
	}
	$("#img-gallery img").attr("src", "assets/img/demo"+imgCounter+".jpg");	
});

var allowedKeys = {
  37: 'left',
  38: 'up',
  39: 'right',
  40: 'down',
  65: 'a',
  66: 'b'
};

var konamiCode = ['up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a'];
var konamiCodePosition = 0;

document.addEventListener('keydown', function(e) {
  var key = allowedKeys[e.keyCode];
  var requiredKey = konamiCode[konamiCodePosition];

  if (key == requiredKey) {
    konamiCodePosition++;
    if (konamiCodePosition == konamiCode.length)
      activateCheats();
  } else
    konamiCodePosition = 0;
});

function activateCheats() {
  window.location = "https://www.youtube.com/embed/mwEfTCWjrg8?rel=0&autoplay=1";
}
});
