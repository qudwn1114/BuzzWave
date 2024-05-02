const new_password1 = document.getElementById("new-password1");
const new_password2 = document.getElementById("new-password2");
const password_error = document.getElementById('password-error');
const btn_submit = document.getElementById("btn-submit");

btn_submit.addEventListener("click", () =>{
    const form = document.getElementById("passwordForm");
    if(!validation()){
        return false;
    }
    btn_submit.disabled = true;
    form.submit();
})

function validation(){
    if (new_password1.value == "") {
        password_error.innerText = 'Please enter your password.';
        new_password1.focus();
        return false;
    }
    if (new_password2.value == "") {
        password_error.innerText = 'Please re enter your password.';
        new_password2.focus();
        return false;
    }
    if (new_password1.value != new_password2.value) {
        password_error.innerText = 'Passwords do not match.';
        new_password1.focus();
        return false;
    }
    if (!regPassword(new_password1.value)) {
        password_error.innerText = 'Minimum 8 characters Maximum 16 characters, at least one letter and one number.';
        new_password1.focus();
        return false;
    }
    return true;
}

//비밀번호 정규식
function regPassword(str) {
    if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d~#?!@$%^&*-+]{8,16}$/.test(str)) {
        return false;
    }
    return true;
}