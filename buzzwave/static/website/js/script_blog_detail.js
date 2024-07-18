const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function deletePost(elem){
    if (!confirm("삭제 하시겠습니까?")) {
        return;
    }
    elem.disabled=true;
    $.ajax({
        type: "DELETE",
        url: "",
        headers: {
            'X-CSRFToken': csrftoken
        },
        datatype: "JSON",
        success: function(data) {
            location.href=data.url;
        },
        error: function(error) {
            elem.disabled=false;
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

}