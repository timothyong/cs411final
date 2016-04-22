document.querySelector('a.answer-button').onclick = function() {
  document.querySelector('div.answer-form-wrapper').className += " show-form";
  document.querySelector('a.answer-button').className += " unclickable";
  document.querySelector('div.answer-form-wrapper textarea').focus();
}

document.querySelector('a.cancel-write').onclick = function() {
  document.querySelector('div.answer-form-wrapper').className =
    document.querySelector('div.answer-form-wrapper').className.replace(
      " show-form", "");
  document.querySelector('a.answer-button').className =
    document.querySelector('a.answer-button').className.replace(
      " unclickable", "");
  document.querySelector('div.answer-form-wrapper textarea').value = "";
}

document.querySelector('form.answer-form textarea').oninput = function() {
  var count = parseInt(document.querySelector(
    'div.answer-form-wrapper textarea').value.length);
  document.querySelector('span.character-count').innerHTML = count;

  if (count == 1) {
    document.querySelector('span#cc').innerHTML = " character";
  } else {
    document.querySelector('span#cc').innerHTML = " characters";
  }
}
