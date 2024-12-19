const btn_submit = document.getElementById("btn-submit");

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

btn_submit.addEventListener("click", () => {
    btn_submit.disabled=true;
    document.getElementById('resetform').submit();
    return;
});