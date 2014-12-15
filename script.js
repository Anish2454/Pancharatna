var div = null;
var timerToggle = null;
var startStop = null;

function moveRight() {
  div.style.left = parseInt(div.style.left)+1+'px';
  timerToggle = setTimeout(moveRight,80);
  }
  
function init() {
  div = document.getElementById("message");
  div.style.left = '0px'; 
  moveRight();
  }


  
    