// Here we will just keep track of the state of the input forms
// in order to make sure the user runs into as little errors as possible
// during registration.
// Get all the input forms
var inputs = document.querySelectorAll('input');
var fullname     = inputs[0];
var username     = inputs[1];
var password     = inputs[2];
var passwordConf = inputs[3];

// Full name
fullname.oninput = function() {
  if (fullname.value.length == 0 || fullname.value.length >= 3) {
    fullname.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    fullname.style.border = '1px solid red';
  }
}
fullname.onblur = function() {
  if (fullname.value.length == 0 || fullname.value.length >= 3) {
    fullname.style.border = '1px solid rgba(125, 136, 255, 0.5)';
  } else {
    fullname.style.border = '1px solid red';
  }
}
fullname.onfocus = function() {
  if (fullname.value.length == 0 || fullname.value.length >= 3) {
    fullname.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    fullname.style.border = '1px solid red';
  }
}

// Username
username.oninput = function() {
  if (username.value.length == 0 || username.value.length >= 4) {
    username.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    username.style.border = '1px solid red';
  }
}
username.onblur = function() {
  if (username.value.length == 0 || username.value.length >= 4) {
    username.style.border = '1px solid rgba(125, 136, 255, 0.5)';
  } else {
    username.style.border = '1px solid red';
  }
}
username.onfocus = function() {
  if (username.value.length == 0 || username.value.length >= 4) {
    username.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    username.style.border = '1px solid red';
  }
}


// Passwords
password.oninput = function() {
  if (password.value.length == 0 || password.value.length >= 6) {
    password.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    password.style.border = '1px solid red';
  }
}
password.onblur = function() {
  if (password.value.length == 0 || password.value.length >= 6) {
    password.style.border = '1px solid rgba(125, 136, 255, 0.5)';
  } else {
    password.style.border = '1px solid red';
  }
}
password.onfocus = function() {
  if (password.value.length == 0 || password.value.length >= 6) {
    password.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    password.style.border = '1px solid red';
  }
}

passwordConf.oninput = function() {
  if (passwordConf.value.length == 0 || (passwordConf.value.length >= 6 &&
      passwordConf.value == password.value)) {
    passwordConf.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    passwordConf.style.border = '1px solid red';
  }
}
passwordConf.onblur = function() {
  if (passwordConf.value.length == 0 || (passwordConf.value.length >= 6 &&
      passwordConf.value == password.value)) {
    passwordConf.style.border = '1px solid rgba(125, 136, 255, 0.5)';
  } else {
    passwordConf.style.border = '1px solid red';
  }
}
passwordConf.onfocus = function() {
  if (passwordConf.value.length == 0 || (passwordConf.value.length >= 6 &&
      passwordConf.value == password.value)) {
    passwordConf.style.border = '1px solid rgb(125, 136, 255)';
  } else {
    passwordConf.style.border = '1px solid red';
  }
}
