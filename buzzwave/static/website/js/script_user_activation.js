function resend(elem){
    elem.innerHTML = '<i class="fa fa-spinner" aria-hidden="true"></i> Loading...';
    elem.disabled=true;
    $.ajax({
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        url: "",
        datatype: "JSON",
        success: function (data) {
            alert(data.message);
            location.href = data.url;
        },
        error: function (error) {
            elem.innerHTML = '재전송';
            elem.disabled=false;
            alert(error.responseJSON.message);
        },
    });
}
