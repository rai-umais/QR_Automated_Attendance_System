function startQRRefresh(courseId) {
    const qrImage  = document.getElementById('qr-image');
    const qrStatus = document.getElementById('qr-status');

    function fetchQR() {
        fetch(`/teacher/get-qr?course_id=${courseId}`)
            .then(res => res.json())
            .then(data => {
                if (data.qr_image) {
                    qrImage.src = 'data:image/png;base64,' + data.qr_image;
                    qrStatus.textContent = 'Refreshed at ' +
                        new Date().toLocaleTimeString();
                } else {
                    qrStatus.textContent = data.error || 'Waiting...';
                }
            })
            .catch(() => {
                qrStatus.textContent = 'Connection error. Retrying...';
            });
    }

    fetchQR();
    setInterval(fetchQR, 5000);
}