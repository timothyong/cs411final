// Here we will just keep track of the state of the input forms
// in order to make sure the user runs into as little errors as possible
// during registration.

// Get all the input forms
var inputs = document.querySelectorAll('input');
var fullname     = inputs[0];
var username     = inputs[1];
var password     = inputs[2];
var passwordConf = inputs[3];

// Get all tooltips
var fn_tooltip = document.querySelector('div.fullname-tooltip'),
    u_tooltip  = document.querySelector('div.username-tooltip'),
    p_tooltip  = document.querySelector('div.password-tooltip'),
    pc_tooltip = document.querySelector('div.passwordConf-tooltip');

// Reposition tooltips
fn_tooltip.style.top  = fullname.offsetTop;
fn_tooltip.style.left = fullname.offsetLeft + fullname.offsetWidth + 12;
u_tooltip.style.top   = username.offsetTop;
u_tooltip.style.left  = username.offsetLeft + username.offsetWidth + 12;
p_tooltip.style.top   = password.offsetTop;
p_tooltip.style.left  = password.offsetLeft + password.offsetWidth + 12;
pc_tooltip.style.top  = passwordConf.offsetTop;
pc_tooltip.style.left = passwordConf.offsetLeft + passwordConf.offsetWidth + 12;

// Full name
fullname.oninput = function() {
  if (fullname.value.length == 0 || fullname.value.length >= 3) {
    fullname.style.border = '1px solid rgb(125, 136, 255)';
    fn_tooltip.style.opacity = 0;
  }
}
fullname.onblur = function() {
  if (fullname.value.length == 0 || fullname.value.length >= 3) {
    fullname.style.border = '1px solid rgba(125, 136, 255, 0.5)';
  } else {
    fullname.style.border = '1px solid rgb(255, 112, 112)';

    fn_tooltip.style.opacity = 1;
    fullname.focus();
  }
}
fullname.onfocus = function() {
  if (fullname.value.length == 0 || fullname.value.length >= 3) {
    fullname.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    fullname.style.border = '1px solid rgb(255, 112, 112)';
  }
}

// Username
username.oninput = function() {
  if (username.value.length == 0 || username.value.length >= 4) {
    username.style.border = '1px solid rgb(125, 136, 255)';
    u_tooltip.style.opacity = 0;
  }
}
username.onblur = function() {
  if (username.value.length == 0 || username.value.length >= 4) {
    username.style.border = '1px solid rgba(125, 136, 255, 0.5)';
  } else {
    username.style.border = '1px solid rgb(255, 112, 112)';

    u_tooltip.style.opacity = 1;
    username.focus();
  }
}
username.onfocus = function() {
  if (username.value.length == 0 || username.value.length >= 4) {
    username.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    username.style.border = '1px solid rgb(225, 112, 112)';
  }
}

// Password
password.oninput = function() {
  if (password.value.length == 0 || password.value.length >= 6) {
    password.style.border = '1px solid rgb(125, 136, 255)';
    p_tooltip.style.opacity = 0;
  }
}
password.onblur = function() {
  if (password.value.length == 0 || password.value.length >= 6) {
    password.style.border = '1px solid rgba(125, 136, 255, 0.5)';
  } else {
    password.style.border = '1px solid rgb(225, 112, 112)';

    p_tooltip.style.opacity = 1;
    password.focus();
  }
}
password.onfocus = function() {
  if (password.value.length == 0 || password.value.length >= 6) {
    password.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    password.style.border = '1px solid rgb(225, 112, 112)';
  }
}

// Password Confirmation
passwordConf.oninput = function() {
  if (passwordConf.value.length == 0 || (passwordConf.value.length >= 6 &&
      passwordConf.value == password.value)) {
    passwordConf.style.border = '1px solid rgb(125, 136, 255)';
    pc_tooltip.style.opacity = 0;
  }
}
passwordConf.onblur = function() {
  if (passwordConf.value.length == 0 || (passwordConf.value.length >= 6 &&
      passwordConf.value == password.value)) {
    passwordConf.style.border = '1px solid rgba(125, 136, 255, 0.5)';
  } else {
    passwordConf.style.border = '1px solid rgb(225, 112, 112)';

    pc_tooltip.style.opacity = 1;
    passwordConf.focus();
  }
}
passwordConf.onfocus = function() {
  if (passwordConf.value.length == 0 || (passwordConf.value.length >= 6 &&
      passwordConf.value == password.value)) {
    passwordConf.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    passwordConf.style.border = '1px solid rgb(225, 112, 112)';
  }
}

