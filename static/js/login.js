const inputPassword = document.querySelector("#input_Password");
const inputConfirmPassword = document.querySelector("#input_ConfirmPassword");
const confirmPassMessage = document.querySelector(".confirm-pass-message");


var check = function () {
  if (inputPassword.value == inputConfirmPassword.value) {
    confirmPassMessage.style.color = "#81f581";
    confirmPassMessage.textContent  = "password matched";
  } else {
    confirmPassMessage.style.color = "#ff8181";
    confirmPassMessage.textContent  = "password did not match";
  }
};
