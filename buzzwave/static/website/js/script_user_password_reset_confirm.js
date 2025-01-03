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
        password_error.innerText = '비밀번호를 입력해주세요.';
        new_password1.focus();
        return false;
    }
    if (new_password2.value == "") {
        password_error.innerText = '비밀번호를 확인해주세요.';
        new_password2.focus();
        return false;
    }
    if (new_password1.value != new_password2.value) {
        password_error.innerText = '비밀번호가 일치하지 않습니다.';
        new_password1.focus();
        return false;
    }
    if (!regPassword(new_password1.value)) {
        password_error.innerText = '비밀번호는 8-16자 영문, 숫자를 포함해야합니다.';
        new_password1.focus();
        return false;
    }
    return true;
}

//비밀번호 정규식
function regPassword(str) {
    const regex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_\-+={}\[\]:;"'<>,.?/~`|\\]{8,16}$/;
    if (!regex.test(str)) {
        return false;
    }
    return true;
}