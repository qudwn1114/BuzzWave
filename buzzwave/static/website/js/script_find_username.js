const btn_submit = document.getElementById("btn-submit");
const email = document.getElementById('email');
const username_message = document.getElementById('username-message');

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

btn_submit.addEventListener("click", () => {
    const data =new FormData(document.getElementById("emailform"));
    if(!validation()){
        return false
    }
    btn_submit.disabled=true;
    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        url: "",
        data: data,
        enctype: "multipart/form-data", //form data 설정
        processData: false, //프로세스 데이터 설정 : false 값을 해야 form data로 인식
        contentType: false, //헤더의 Content-Type을 설정 : false 값을 해야 form data로 인식
        success: function(data) {
            username_message.className = 'success';
            username_message.innerText=data.message;
            btn_submit.disabled=false;
        },
        error: function(error) {
            if(error.status == 403){
                username_message.className = 'error';
                username_message.innerText=error.responseJSON.message;
                location.href = data.url;
            }else{
                username_message.className = 'error';
                username_message.innerText=error.responseJSON.message;
                btn_submit.disabled=false;
            }
        },
    });
});

//유효성 체크 함수
function validation(){
    username_message.innerText='';
    if(email.value == ''){
        email.focus();
        return false;
    }
    return true;
}

function enterkey(event) {
    if (window.event.keyCode == 13) {
        btn_submit.click()
    }
}