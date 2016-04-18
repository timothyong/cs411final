
// document.querySelector('span.logo a').onclick = function() {
//   console.log(document.querySelector('div.notification').offsetHeight);
//   console.log("logo clicked!");
//   var modal = document.querySelector('div.modal');
//   modal.className += " moveUp";
//   setTimeout(function() {
//     modal.className = modal.className.replace(" moveUp", "");
//   }, 2000);
// }

var displayNotif = function() {
  alert("hello");
}

document.querySelector('span.logo a').onclick = function() {

  var notif = document.querySelector('div.notification');
  notif.className += " notif-active";
  setTimeout(function() {
    notif.className = notif.className.replace(" notif-active", "");
  }, 3000);
}


