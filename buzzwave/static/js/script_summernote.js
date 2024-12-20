$(document).ready(function() {
    $('#content').summernote({
        lang: 'ko-KR',
        placeholder: '내용을 입력해주세요.. (필수)',
        tabsize: 2,
        height: 500,
        fontNames: ["나눔고딕", "나눔명조", "나눔바른고딕", "나눔바른펜", "나눔손글씨붓", "나눔손글씨펜", "나눔스퀘어", "맑은고딕"],
        fontSizes: ['8','9','10','11','12','14','16','18','20','22','24','28','30','36','50','72'],
        toolbar: [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline','strikethrough', 'clear']],
            ['fontname', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['height', ['hex`ight']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video', 'hr']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
        callbacks: {
            onPaste: function(e) {
                console.log('onPaste called'); // 붙여넣기 시 log 확인
                var bufferText = (e.originalEvent || e).clipboardData.getData('text/html');
                var cleanText = bufferText.replace(/style="[^"]*"/g, ''); // 인라인 스타일 제거
                e.preventDefault();
                $('#content').summernote('code', cleanText);
            },
            onImageUpload: function(files) {
                if (files.length > 0) {
                    const maxSize = 10 * 1024 * 1024; // 10MB
                    let formData = new FormData();
                    let filesToUpload = [];
            
                    // 파일 크기 체크
                    for (let i = 0; i < files.length; i++) {
                        const file = files[i];
            
                        if (file.size > maxSize) {
                            alert('파일 중 하나가 10MB를 초과합니다. 업로드를 중단합니다.');
                            return; // 업로드 중단
                        }
            
                        formData.append('files', file); // 여러 파일을 한 번에 추가
                        filesToUpload.push(file);
                    }
                    // 여러 파일을 서버로 업로드
                    $.ajax({
                        url: '/summernote/upload-image/', // Django에서 처리할 URL
                        method: 'POST',
                        data: formData,
                        processData: false,
                        contentType: false,
                        headers: {
                            'X-CSRFToken': csrftoken // CSRF 토큰
                        },
                        success: function(data) {
                            // 각 파일에 대한 응답 처리 (여기서는 data.url이 여러 파일의 URL을 포함하는 배열이라고 가정)
                            for (let i = 0; i < data.urls.length; i++) {
                                $('#content').summernote('insertImage', data.urls[i]); // 업로드된 이미지 삽입
                            }
                        },
                        error: function() {
                            alert('이미지 업로드 실패');
                        }
                    });
                }
            }
        }
    });
});