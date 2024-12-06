const btn_submit = document.getElementById("cfsubmit");
const input_name = document.getElementById('name');
const input_email = document.getElementById('email');
const input_phone = document.getElementById('phone');
const input_message = document.getElementById('message');
const input_company = document.getElementById('company');
const input_job = document.getElementById('job');

const error_name = document.getElementById('name-error');
const error_email = document.getElementById('email-error');
const error_phone = document.getElementById('phone-error');
const error_message = document.getElementById('message-error');

const semail = document.getElementById("semail");
const btn_subscribe = document.getElementById('subscription-form-submit');

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

window.onload = function(){
    let hash = window.location.hash;
    let duration = 1000;
    if (hash !== null && hash !== '') { // it was indeed ending in -st
        if($(hash).length == 0){
            return;
        }
        $('html, body').animate({
            scrollTop: $(hash).offset().top - 50
        }, duration);
    }
}

btn_submit.addEventListener("click", async() => {
    if(!validation()){
        return false;
    }
    const data =new FormData(document.getElementById("contactForm"));
    input_name.disabled = true;
    input_email.disabled = true;
    input_phone.disabled = true;
    input_message.disabled = true;
    input_company.disabled = true;
    input_job.disabled = true;
    btn_submit.disabled = true;
    btn_submit.innerHTML='<i class="fa fa-spinner" aria-hidden="true"></i> Loading...';

    const response = await fetch('/contact/',{
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: data
    })
    try{
        const result = await response.json()
        if (!response.ok) {
            throw new Error(`${result.message}`);
        }
        alert(result.message);
        window.location.reload();
    }
    catch(error){
        alert(error);
        input_name.disabled = false;
        input_email.disabled = false;
        input_phone.disabled = false;
        input_message.disabled = false;
        input_company.disabled = false;
        input_job.disabled = false;
        btn_submit.disabled = false;
        btn_submit.innerHTML='Send Message';
        return false;
    }
});

function enterkey(event) {
    if (window.event.keyCode == 13) {
        btn_subscribe.click()
    }   
}


btn_subscribe.addEventListener("click", () => {
    if(semail.value == ''){
        semail.focus();
        return;
    }
    if(!reg_email.test(semail.value)){
        alert('Invalid email format.')
        return;
    }
    btn_subscribe.disabled=true;
    btn_subscribe.innerHTML='<i class="fa fa-cog fa-spin"></i> Wait...';
    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        url: "/subscribe/",
        dataType: 'json',
        data: {email:semail.value},
        success: function(result) {
            alert(result.message);
            semail.value = '';
            btn_subscribe.disabled=false;
            btn_subscribe.innerHTML='Submit';
        },
        error: function(error) {
            alert(error.responseJSON.message);
            btn_subscribe.disabled=false;
            btn_subscribe.innerHTML='Submit';
        },
    });
    
});

const reg_email = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;
function validation(){
    error_name.innerText='';
    error_email.innerText='';
    error_phone.innerText='';
    error_message.innerText='';
    
    let tf = true;

    if(input_name.value==''){
        error_name.innerText = 'Please enter your name.';
        tf = false;        
    }
    if(input_email.value==''){
        error_email.innerText = 'Please enter your email.';
        tf = false;
    }
    if(!reg_email.test(input_email.value)){
        error_email.innerText = 'Invalid email format.';
        tf = false;
    }         
    if(input_phone.value==''){
        error_phone.innerText = 'Please enter your phone.';
        tf = false;  
    }
    if(input_message.value==''){
        error_message.innerText = 'Please enter your message.';
        tf = false;
    }
    return tf;
}