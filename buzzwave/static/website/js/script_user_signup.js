const membername = document.getElementById("membername");
const birth = document.getElementById("birth");
const email = document.getElementById("email");
const username = document.getElementById("username");
const password1 = document.getElementById("password");
const password2 = document.getElementById("re-password");
const phone = document.getElementById("phone");
const company = document.getElementById("company");

const message_membername = document.getElementById("message-membername");
const message_email = document.getElementById("message-email");
const message_username = document.getElementById("message-username");
const message_birth = document.getElementById("message-birth");
const message_phone = document.getElementById("message-phone");
const message_password = document.getElementById("message-password");

const error_signup = document.getElementById("signup-error");

const btn_submit = document.getElementById("btn-submit");
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function checkEmail() {
    message_email.innerText = ''
    message_email.className = 'error';
    email.value = email.value.trim();
    const data = {
        'email': email.value
    }
    $.ajax({
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        url: "/check-email/",
        data: data,
        datatype: "JSON",
        success: function (data) {
            email.value = data.email;
            message_email.className = 'success';
            message_email.innerText = data.message;
        },
        error: function (error) {
            email.focus();
            message_email.innerText = error.responseJSON.message;
        },
    });
}

function checkUsername() {
    message_username.innerText = ''
    message_username.className = 'error';
    username.value = username.value.trim();
    const data = {
        'username': username.value
    }
    $.ajax({
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        url: "/check-username/",
        data: data,
        datatype: "JSON",
        success: function (data) {
            username.value = data.username;
            message_username.className = 'success';
            message_username.innerText = data.message;
        },
        error: function (error) {
            username.focus();
            message_username.innerText = error.responseJSON.message;
        },
    });
}

function checkBirth() {
    message_birth.innerText = ''
    message_birth.className = 'error';
    const data = {
        'birth': birth.value
    }
    $.ajax({
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        url: "/check-birth/",
        data: data,
        datatype: "JSON",
        success: function (data) {
            birth.value = data.birth;
        },
        error: function (error) {
            birth.focus();
            message_birth.innerText = error.responseJSON.message;
        },
    });
}

function checkPassword(){
    message_password.innerText = ''
    message_password.className = 'error';
    if(password1.value == '' && password2.value == ''){
        message_password.innerText = '비밀번호를 입력해주세요.';
        password1.focus();
        return;
    }
    else if(password1.value != '' && password2.value == ''){
        if (!regPassword(password1.value)) {
            message_password.innerText = '비밀번호는 8-16자 영문, 숫자를 포함해야합니다.';
            password1.focus();
        }
        return;
    }
    else if(password1.value != '' && password2.value != ''){
        if (password1.value != password2.value) {
            message_password.innerText = '비밀번호가 일치하지 않습니다.';
            password1.focus();
            return
        }
        else{
            if (!regPassword(password1.value)) {
                message_password.innerText = '비밀번호는 8-16자 영문, 숫자를 포함해야합니다.';
                password1.focus();
                return
            }
        }
    }
    else if(password1.value == '' && password2.value != ''){
        if (!regPassword(password2.value)) {
            message_password.innerText = '비밀번호는 8-16자 영문, 숫자를 포함해야합니다.';
            password2.focus();
            return;
        }
        else{
            message_password.innerText = '비밀번호를 입력해주세요.';
            password1.focus();
            return;
        }
    }
    message_password.className = 'success';
    message_password.innerText = '사용가능한 비밀번호입니다.';
    return;
}

btn_submit.addEventListener("click", () => {
    const data = new FormData(document.getElementById("signupForm"));
    if (validation() == false) {
        return;
    }
    membername.disabled = true;
    username.disabled = true;
    email.disabled = true;
    password1.disabled = true;
    password2.disabled = true;
    phone.disabled = true;
    birth.disabled = true;
    company.disabled = true;
    btn_submit.disabled = true;
    btn_submit.innerHTML = '<i class="fa fa-spinner" aria-hidden="true"></i> Loading...';

    $.ajax({
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        url: "",
        data: data,
        enctype: "multipart/form-data", //form data 설정
        processData: false, //프로세스 데이터 설정 : false 값을 해야 form data로 인식
        contentType: false, //헤더의 Content-Type을 설정 : false 값을 해야 form data로 인식
        success: function (data) {
            location.href=data.url;
        },
        error: function (error) {
            error_signup.innerText = error.responseJSON.message;
            membername.disabled = false;
            username.disabled = false;
            email.disabled = false;
            password1.disabled = false;
            password2.disabled = false;
            phone.disabled = false;
            birth.disabled = false;
            company.disabled = false;
            btn_submit.disabled = false;
            btn_submit.innerHTML = '회원가입';
        },
    });


});


//유효성 체크 함수
function validation() {
    if (membername.value == "") {
        message_membername.innerText = '이름을 입력해주세요.';
        membername.focus();
        return false;
    }
    if (email.value == "") {
        message_email.innerText = '이메일을 입력해주세요.';
        email.focus();
        return false;
    }
    if (username.value == "") {
        message_username.innerText = '아이디를 입력해주세요.';
        username.focus();
        return false;
    }
    if (birth.value == "") {
        message_birth.innerText = '생년월일을 입력해주세요.';
        birth.focus();
        return false;
    }
    if (phone.value == "") {
        message_phone.innerText = '휴대폰번호를 입력해주세요.';
        phone.focus();
        return false;
    }
    if (password1.value == "") {
        message_password.innerText = '비밀번호를 입력해주세요.';
        password1.focus();
        return false;
    }
    if (password2.value == "") {
        message_password.innerText = '비밀번호를 재 입력해주세요.';
        password2.focus();
        return false;
    }
    if (password1.value != password2.value) {
        message_password.innerText = '비밀번호가 일치하지 않습니다.';
        password1.focus();
        return false;
    }
    if (!regPassword(password1.value)) {
        message_password.innerText = '비밀번호는 8-16자 영문, 숫자를 포함해야합니다.';
        password1.focus();
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
