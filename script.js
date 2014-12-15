var div = null;
var timerToggle = null;
var startStop = null;
var choice = "stop";

function choose () {
  if(choice == "stop") {
    choice = "start";
	}
  else{
    choice = "stop";
	}
  init();
}
    



function moveRight() {
  if(choice == "start") {
  div.style.left = parseInt(div.style.left)+2+'px';
  timerToggle = setTimeout(moveRight,80);
  }
  else {
    window.clearTimeout(timerToggle);
	}
}
  
function init() {
  div = document.getElementById("message");
  div.style.left = '0px'; 
  moveRight();
  }


  
    