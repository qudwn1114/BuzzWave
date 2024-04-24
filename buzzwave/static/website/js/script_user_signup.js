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
    message_email.className = 'text-danger';
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
            message_email.className = 'text-success';
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
    message_username.className = 'text-danger';
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
            message_username.className = 'text-success';
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
    message_birth.className = 'text-danger';
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
    message_password.className = 'text-danger';
    if(password1.value != '' && password2.value == ''){
        if (!regPassword(password1.value)) {
            message_password.innerText = 'Minimum 8 characters Maximum 16 characters, at least one letter and one number.';
            password1.focus();
        }
        return;
    }
    else if(password1.value != '' && password2.value != ''){
        if (password1.value != password2.value) {
            message_password.innerText = 'Passwords do not match.';
            password1.focus();
            return
        }
        else{
            if (!regPassword(password1.value)) {
                message_password.innerText = 'Minimum 8 characters Maximum 16 characters, at least one letter and one number.';
                password1.focus();
                return
            }
        }
    }
    else if(password1.value == '' && password2.value != ''){
        if (!regPassword(password2.value)) {
            message_password.innerText = 'Minimum 8 characters Maximum 16 characters, at least one letter and one number.';
            password2.focus();
            return;
        }
        else{
            message_password.innerText = 'Please enter your password.';
            password1.focus();
            return;
        }
    }
    message_password.className = 'text-success';
    message_password.innerText = '✔';
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
            btn_submit.innerHTML = 'Signup';
        },
    });


});


//유효성 체크 함수
function validation() {
    if (membername.value == "") {
        message_membername.innerText = 'Please enter your name.';
        membername.focus();
        return false;
    }
    if (email.value == "") {
        message_email.innerText = 'Please enter your email.';
        email.focus();
        return false;
    }
    if (username.value == "") {
        message_username.innerText = 'Please enter your username.';
        username.focus();
        return false;
    }
    if (birth.value == "") {
        message_birth.innerText = 'Please enter your birth.';
        birth.focus();
        return false;
    }
    if (phone.value == "") {
        message_phone.innerText = 'Please enter your mobile number.';
        phone.focus();
        return false;
    }
    if (password1.value == "") {
        message_password.innerText = 'Please enter your password.';
        password1.focus();
        return false;
    }
    if (password2.value == "") {
        message_password.innerText = 'Please re enter your password.';
        password2.focus();
        return false;
    }
    if (password1.value != password2.value) {
        message_password.innerText = 'Passwords do not match.';
        password1.focus();
        return false;
    }
    if (!regPassword(password1.value)) {
        message_password.innerText = 'Minimum 8 characters Maximum 16 characters, at least one letter and one number.';
        password1.focus();
        return false;
    }
    return true;
}

//비밀번호 정규식
function regPassword(str) {
    if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/.test(str)) {
        return false;
    }
    return true;
}
