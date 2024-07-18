const title = document.getElementById("title");
const btn_edit = document.getElementById("btn_edit");

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

btn_edit.addEventListener("click", () => {
    if(!validation()){
        return false;
    }
    if (!confirm("수정 하시겠습니까?")) {
        return;
    }
    const data =new FormData(document.getElementById("data-form"));
    btn_edit.disabled=true;
    $.ajax({
        type: "POST",
        url: "",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: data,
        enctype: "multipart/form-data", //form data 설정
        processData: false, //프로세스 데이터 설정 : false 값을 해야 form data로 인식
        contentType: false, //헤더의 Content-Type을 설정 : false 값을 해야 form data로 인식
        success: function(data) {
            location.href = data.url;
        },
        error: function(error) {
            btn_edit.disabled=false;
            if(error.status == 401){
                alert('로그인 해주세요.');
            }
            else if(error.status == 403){
                alert('권한이 없습니다!');
            }
            else{
                alert(error.status + JSON.stringify(error.responseJSON));
            }
        },
    });
})


function validation(){
    if(title.value === ""){
        title.focus();
        return false;
    }
    return true;
}
