const btn_submit = document.getElementById("btn-submit");
const email = document.getElementById('email');
const error_email = document.getElementById('email-error');

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

btn_submit.addEventListener("click", () => {
    if(!validation()){
        return false
    }
    btn_submit.disabled=true;
    document.getElementById('resetform').submit();
    return;
});

function validation(){
    error_email.innerText='';
    if (!/[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}$/.test(email.value)) {
        error_email.innerText='Invalid email format.';
        email.focus();
        return false;
    }
    return true
}

function enterkey(event) {
    if (window.event.keyCode == 13) {
        btn_submit.click()
    }   
}