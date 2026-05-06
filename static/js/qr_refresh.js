let countdown = 50;
let tickTimer = null;
let currentCourseId = null;

function startQRRefresh(courseId) {
    currentCourseId = courseId;
    fetchQR();
}

function fetchQR() {
    const qrStatus = document.getElementById('qr-status');
    const qrImage = document.getElementById('qr-image');
    const label = document.getElementById('refresh-label');

    console.log('Fetching new QR for course:', currentCourseId);
    fetch(`/teacher/get-qr?course_id=${currentCourseId}`)
        .then(res => res.json())
        .then(data => {
            console.log('QR data received:', data);
            if (data.qr_image) {
                qrImage.src = 'data:image/png;base64,' + data.qr_image;
                window._qrBase = data.seconds;
                if (label) label.textContent = `Refreshes in ${data.seconds}s`;
                resetCountdown(data.seconds);
            } else {
                qrStatus.textContent = data.error || 'Waiting...';
            }
        })
        .catch(err => {
            console.error('QR Fetch Error:', err);
            qrStatus.textContent = 'Connection error. Retrying...';
        });
}

function resetCountdown(secs) {
    clearTimeout(tickTimer);
    countdown = secs;
    tick();
}

function tick() {
    const fill = document.getElementById('countdown-fill');
    const qrStatus = document.getElementById('qr-status');
    const label = document.getElementById('refresh-label');
    
    if (label) label.textContent = `Refreshes in ${countdown}s`;
    
    if (fill && window._qrBase) {
        const percentage = (countdown / window._qrBase) * 100;
        fill.style.width = percentage + '%';
    }

    if (countdown <= 0) {
        fetchQR();
        return;
    }

    countdown--;
    tickTimer = setTimeout(tick, 1000);
}