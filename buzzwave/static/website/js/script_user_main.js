// 메인 Value 섹션 슬라이드
const swiper = new Swiper(".serviceSwiper", {
    effect: "fade",
    centeredSlides: true,
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});

// 메인 Price 섹션 금액
const priceElements = document.querySelectorAll(".price");

setDefaultClass();

priceElements.forEach((item) => {
    item.addEventListener("mouseenter", () => {
        priceElements.forEach((el) => el.classList.remove("default"));
    });

    item.addEventListener("mouseleave", () => {
        setDefaultClass();
    });
});

function setDefaultClass() {
    let hasDefault = false;

    priceElements.forEach((el) => {
        if (el.dataset.default) {
            el.classList.add("default");
            hasDefault = true;
        } else {
            el.classList.remove("default");
        }
    });

    if (!hasDefault && priceElements.length > 0) {
        priceElements[0].classList.add("default");
    }
}
// 서비스 모달
const startBtn = document.querySelectorAll(".start");
const serviceModal = document.querySelector(".service_modal");
const serviceModalInner = document.querySelector(".service_modal_inner");
const contactBtn = document.querySelector(".btn_contact");

window.addEventListener("click", (e) => {
    if (e.target === serviceModal) {
        serviceModal.classList.remove("show");
    }
});

startBtn.forEach((btn) => {
    btn.addEventListener("click", () => {
        serviceModal.classList.add("show");
    });
});

contactBtn.addEventListener("click", () => {
    const mainContact = document.querySelector(".main_contact");
    serviceModal.classList.remove("show");

    window.scrollTo({
        top: mainContact.offsetTop - header.clientHeight,
        behavior: "smooth",
    });
});


const btn_submit = document.getElementById("btn_submit");
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
const btn_subscribe = document.getElementById('btn_subscription');

const reg_email = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;

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
        btn_submit.innerHTML='문의하기';
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
        alert('잘못된 이메일 형식입니다.')
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
            btn_subscribe.innerHTML='구독하기';
        },
        error: function(error) {
            alert(error.responseJSON.message);
            btn_subscribe.disabled=false;
            btn_subscribe.innerHTML='구독하기';
        },
    });
    
});

function validation(){
    error_name.innerText='';
    error_email.innerText='';
    error_phone.innerText='';
    error_message.innerText='';
    
    let tf = true;

    if(input_name.value==''){
        error_name.innerText = '이름을 입력해주세요.';
        tf = false;        
    }
    if(input_email.value==''){
        error_email.innerText = '이메일을 입력해주세요.';
        tf = false;
    }
    if(!reg_email.test(input_email.value)){
        error_email.innerText = '유효하지 않은 이메일 형식입니다.';
        tf = false;
    }         
    if(input_phone.value==''){
        error_phone.innerText = '휴대폰번호를 입력해주세요.';
        tf = false;  
    }
    if(input_message.value==''){
        error_message.innerText = '문의내용을 입력해주세요.';
        tf = false;
    }
    return tf;
}