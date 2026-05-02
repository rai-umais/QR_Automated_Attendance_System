function startQRRefresh(courseId) {
    const qrImage  = document.getElementById('qr-image');
    const qrStatus = document.getElementById('qr-status');
    let countdown  = 30;
    let countdownInterval = null;

    function fetchQR() {
        fetch(`/teacher/get-qr?course_id=${courseId}`)
            .then(res => res.json())
            .then(data => {
                if (data.qr_image) {
                    qrImage.src = 'data:image/png;base64,' + data.qr_image;
                    
                    // reset countdown
                    countdown = 30;
                    clearInterval(countdownInterval);
                    
                    // start countdown display
                    countdownInterval = setInterval(() => {
                        countdown--;
                        qrStatus.textContent = 
                            `Next QR in ${countdown}s`;
                        if (countdown <= 0) {
                            clearInterval(countdownInterval);
                        }
                    }, 1000);
                } else {
                    qrStatus.textContent = data.error || 'Waiting...';
                }
            })
            .catch(() => {
                qrStatus.textContent = 'Connection error. Retrying...';
            });
    }

    fetchQR();
    setInterval(fetchQR, 30000); // ← exactly 30 seconds
}