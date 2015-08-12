var div = null;
var timerToggle = null;
var startStop = null;
var choice = "stop";
var leftTimer = null;
var cursorX = null;
var cursorY = null;

function choose() {
  if(choice == "stop") {
    choice = "start";
	}
  else{
    choice = "stop";
	}
  moveLeft();
}
    
function moveRight() {
  if (choice == "start") {
    div.style.left = parseInt(div.style.left)+2+'px';
    timerToggle = setTimeout(moveRight, 20);
	
	if (parseInt(div.style.left) > 1500) {
	    window.clearInterval(timerToggle);
        moveLeft();
	}
  }
  
  else {
    window.clearTimeout(timerToggle);
	}
}

function moveLeft() {
  if (choice == "start") {
    div.style.left = (parseInt(div.style.left)-2)+'px';
    leftTimer = setTimeout(moveLeft, 20);
    if (parseInt(div.style.left) < 2) { 
      window.clearInterval(leftTimer);
	  moveRight();
	}
  }
  
  else {
    window.clearInterval(leftTimer);
  }
  
}
  
function init() {
  div = document.getElementById("message");
  div.style.left = '0px'; 
  choose();
  }


  


  
    