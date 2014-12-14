var div = null;

function moveRight() {
  div.style.left = parseInt(div.style.left)+1+'px';
  setTimeout(moveRight,80);
  }
  
function moveLeft() {
  div.style.left = (parseInt(div.style.left) - 2) + 'px';
  setTimeout(moveLeft, 80);
  }
  
function init() {
  div = document.getElementById("message");
  div.style.left = '0px'; 
  moveRight();
  }
window.onload = init;