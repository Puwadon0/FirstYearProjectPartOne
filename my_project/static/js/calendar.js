// Sample Events Data
let events = [

];

let calendar;
let selectedEventId = null;

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'th',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,listMonth'
        },
        events: '/api/get_events', // ดึงข้อมูลจากฐานข้อมูล
        
        // แก้ไขส่วนนี้ครับ
        eventClick: function(info) {
            const event = info.event;
            const props = event.extendedProps;

            // นำข้อมูลจาก FullCalendar ไปใส่ใน Modal
            document.getElementById('viewTitle').innerText = event.title;
            document.getElementById('viewStart').innerText = event.start.toLocaleDateString('th-TH');
            
            if (event.end) {
                document.getElementById('viewEnd').innerText = event.end.toLocaleDateString('th-TH');
            } else {
                document.getElementById('viewEnd').innerText = event.start.toLocaleDateString('th-TH');
            }

            document.getElementById('viewLocation').innerText = props.location || '-';
            document.getElementById('viewDesc').innerText = props.description || '-';

            // สั่งเปิด Modal รายละเอียด
            var detailModal = new bootstrap.Modal(document.getElementById('eventDetailModal'));
            detailModal.show();
        }
    });
    calendar.render();
});
function openAddModal(start, end) {
    document.getElementById('eventStartDate').value = start.toISOString().split('T')[0];
    if (end) document.getElementById('eventEndDate').value = end.toISOString().split('T')[0];
    new bootstrap.Modal(document.getElementById('addEventModal')).show();
}

function showEventDetail(event) {
    selectedEventId = event.id;
    const props = event.extendedProps;
    const badgeClass = props.type === 'activity' ? 'badge-activity' : (props.type === 'meeting' ? 'badge-meeting' : 'badge-deadline');

    document.getElementById('eventDetailContent').innerHTML = `
        <div class="mb-3 text-center">
            <h4 class="fw-bold text-primary">${event.title}</h4>
            <span class="badge ${badgeClass} px-3 py-2">${props.type}</span>
        </div>
        <div class="p-3 bg-light rounded">
            <p><strong><i class="bi bi-geo-alt me-2"></i>สถานที่:</strong> ${props.location || '-'}</p>
            <p><strong><i class="bi bi-card-text me-2"></i>รายละเอียด:</strong> ${props.description || '-'}</p>
        </div>
    `;
    new bootstrap.Modal(document.getElementById('eventDetailModal')).show();
}

function saveEvent() {
    const title = document.getElementById('eventTitle').value;
    const start = document.getElementById('eventStartDate').value;
    const type = document.getElementById('eventType').value;

    if (!title || !start) return alert('กรุณากรอกข้อมูลที่จำเป็น');

    const newEvent = {
        id: Date.now(),
        title: title,
        start: start,
        end: document.getElementById('eventEndDate').value,
        type: type,
        location: document.getElementById('eventLocation').value,
        description: document.getElementById('eventDescription').value
    };

    events.push(newEvent);
    calendar.addEvent(newEvent);
    updateUpcomingEvents();
    bootstrap.Modal.getInstance(document.getElementById('addEventModal')).hide();
    document.getElementById('eventForm').reset();
}

function updateUpcomingEvents() {
    const container = document.getElementById('upcomingEvents');
    const upcoming = events.slice(0, 4);
    container.innerHTML = upcoming.map(ev => `
        <div class="upcoming-item d-flex justify-content-between align-items-center">
            <div>
                <div class="fw-bold">${ev.title}</div>
                <small class="text-muted">${ev.start}</small>
            </div>
            <span class="badge badge-${ev.type}">${ev.type}</span>
        </div>
    `).join('') || '<p class="text-center py-3 text-muted">ไม่มีกิจกรรม</p>';
}
function saveData() {
    // 1. ดึงค่าจากหน้าเว็บตาม ID ที่ตั้งไว้ข้างบน
    const eventData = {
        title: document.getElementById('title').value,
        start_date: document.getElementById('start').value,
        end_date: document.getElementById('end').value,
        type: document.getElementById('type').value,
        location: document.getElementById('location').value,
        description: document.getElementById('desc').value
    };

    // 2. ส่งข้อมูลไปที่ Backend (Flask)
    fetch('/api/save_event', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(eventData)
    })
        .then(response => response.json())
        .then(result => {
            alert('บันทึกสำเร็จ!'); // ถ้าสำเร็จจะขึ้นข้อความแจ้งเตือน
            location.reload();    // รีโหลดหน้าเพื่ออัปเดตข้อมูล
        })
        .catch(error => {
            console.error('Error:', error);
            alert('เกิดข้อผิดพลาดในการบันทึก');
        });
}
