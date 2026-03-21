let calendar;
let currentEventId = null;
// ยึดโครงสร้างชุดแรก: อ่าน role จาก data-role บน <body> ที่ Flask inject มาให้
let userMode = document.body.getAttribute('data-role') || 'guest';

document.addEventListener('DOMContentLoaded', function () {
    const today = new Date();
    const dateDisplay = document.getElementById('currentDateDisplay');
    if (dateDisplay) {
        dateDisplay.innerText = "วันนี้: " + today.toLocaleDateString('th-TH', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
    }

    // โหลดปฏิทิน
    var calendarEl = document.getElementById('calendar');
    if (calendarEl) {
        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'th',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,listMonth'
            },
            // ใช้ Logic การ Fetch และ Filter จากชุดที่สอง
            events: function(fetchInfo, successCallback, failureCallback) {
                fetch('/api/get_events')
                    .then(response => response.json())
                    .then(data => {
                        const events = data.filter(ev => {
                            // Logic กรองกิจกรรมสำหรับนักศึกษา
                            if (userMode === 'student') {
                                if (ev.type === "ประชุม") return false;
                                if (ev.type === "กำหนดส่ง") return false;
                                if (ev.status !== "อนุมัติแล้ว") return false;
                            }
                            return true;
                        }).map(ev => {
                            // กำหนดสีตามประเภทกิจกรรมจากชุดที่สอง
                            let color = "#3788d8";
                            if (ev.type === "กิจกรรม") color = "#28a745";
                            else if (ev.type === "ประชุม") color = "#ffc107";
                            else if (ev.type === "กำหนดส่ง") color = "#dc3545";

                            return {
                                id: ev.id,
                                title: ev.title,
                                start: ev.start,
                                end: ev.end,
                                backgroundColor: color,
                                borderColor: color,
                                extendedProps: {
                                    type: ev.type,
                                    location: ev.location,
                                    status: ev.status,
                                    description: ev.description
                                }
                            };
                        });
                        successCallback(events);
                    });
            },
            eventClick: function (info) {
                currentEventId = info.event.id;
                document.getElementById('viewTitle').innerText = info.event.title;

                // แสดงวันที่เริ่ม-จบ
                document.getElementById('viewStart').innerText = info.event.start.toLocaleDateString('th-TH');
                const viewEndEl = document.getElementById('viewEnd');
                if (viewEndEl) {
                    if (info.event.allDay && info.event.end) {
                        let displayEnd = new Date(info.event.end);
                        displayEnd.setDate(displayEnd.getDate() - 1);
                        viewEndEl.innerText = displayEnd.toLocaleDateString('th-TH');
                    } else if (info.event.end) {
                        viewEndEl.innerText = info.event.end.toLocaleDateString('th-TH');
                    } else {
                        viewEndEl.innerText = info.event.start.toLocaleDateString('th-TH');
                    }
                }

                document.getElementById('viewLocation').innerText = "สถานที่: " + (info.event.extendedProps.location || "-");
                
                // แสดงรายละเอียดตามสิทธิ์ (ชุดที่สอง)
                if (userMode === 'student') {
                    document.getElementById('viewDesc').innerText = "ประเภท: " + (info.event.extendedProps.type || "-");
                } else {
                    document.getElementById('viewDesc').innerText = 
                        "ประเภท: " + (info.event.extendedProps.type || "-") + 
                        " | สถานะ: " + (info.event.extendedProps.status || "-") +
                        "\nคำอธิบาย: " + (info.event.extendedProps.description || "-");
                }

                // การแสดงผลปุ่ม ลบ และ อนุมัติ
                const delBtn = document.getElementById('delBtn');
                if (delBtn) delBtn.style.display = (userMode === 'student') ? 'none' : 'block';

                const approveBtn = document.getElementById('approveBtn');
                if (approveBtn) approveBtn.style.display = (userMode === 'staff' || userMode === 'officer') ? 'block' : 'none';

                new bootstrap.Modal(document.getElementById('eventDetailModal')).show();
            }
        });
        calendar.render();
    }

    updateSidebarList();
    applyModeSettings();
});

function applyModeSettings() {
    const addBtn = document.getElementById('addEventBtn');
    const addNewsBtn = document.getElementById('addNewsBtn');
    const roleProfileText = document.getElementById('userRoleProfile');
    const modeText = document.getElementById('currentModeText');
    const expandedContainer = document.getElementById('expandedFunctions');
    const megaMenu = document.getElementById('megaMenuContent');

    const roleLabels = { staff: 'เจ้าหน้าที่', officer: 'เจ้าหน้าที่', club: 'นักศึกษาสโมสร', student: 'นักศึกษา', guest: 'ผู้เยี่ยมชม' };
    if (roleProfileText) roleProfileText.innerText = roleLabels[userMode] || 'ผู้เยี่ยมชม';
    if (modeText) modeText.innerText = roleLabels[userMode] || 'ลงชื่อเข้าใช้';

    if (addBtn) addBtn.style.display = (userMode === 'student' || userMode === 'guest') ? 'none' : 'block';
    if (addNewsBtn) addNewsBtn.style.display = (userMode === 'student' || userMode === 'guest') ? 'none' : 'block';

    const path = window.location.pathname;
    let commonLinks = `
        <a class="nav-link ${path === '/news' ? 'active' : ''}" href="/news"><i class="bi bi-megaphone me-2"></i>ข่าวประชาสัมพันธ์</a>
        <a class="nav-link ${path === '/calendar' ? 'active' : ''}" href="/calendar"><i class="bi bi-calendar3 me-2"></i>ปฏิทินกิจกรรม</a>
    `;

    let roleLinks = "";
    if (userMode === 'staff' || userMode === 'officer') {
        roleLinks = `
            <a class="dropdown-item" href="/club_status_activity"><i class="bi bi-clipboard-check me-2"></i>ตรวจโครงการ</a>
            <a class="dropdown-item" href="/officer"><i class="bi bi-journal-plus me-2"></i>คำขอสร้างกิจกรรม</a>
            <a class="dropdown-item" href="/activity/list"><i class="bi bi-person-lines-fill me-2"></i>รายชื่อผู้ลงทะเบียน</a>
            <a class="dropdown-item" href="/expense/list"><i class="bi bi-receipt me-2"></i>สรุปรายจ่าย</a>
            <a class="dropdown-item" href="/resources/manage"><i class="bi bi-geo-alt me-2"></i>ข้อมูลสถานที่</a>
            <a class="dropdown-item" href="/qa/answer"><i class="bi bi-chat-dots me-2"></i>Q&A เจ้าหน้าที่</a>
        `;  
    } else if (userMode === 'club') {
        roleLinks = `
            <a class="dropdown-item" href="/create-activity"><i class="bi bi-plus-circle me-2"></i>สร้างกิจกรรม</a>
            <a class="dropdown-item" href="/club_status_activity"><i class="bi bi-clipboard-check me-2"></i>สถานะคำขอของฉัน</a>
            <a class="dropdown-item" href="/expense/create"><i class="bi bi-cash-stack me-2"></i>บันทึกค่าใช้จ่าย</a>
            <a class="dropdown-item" href="/activity/register"><i class="bi bi-person-plus me-2"></i>ลงทะเบียนกิจกรรม</a>
            <a class="dropdown-item" href="/resources/manage"><i class="bi bi-geo-alt me-2"></i>ข้อมูลสถานที่</a>
            <a class="dropdown-item" href="/qa/answer"><i class="bi bi-chat-dots me-2"></i>Q&A เจ้าหน้าที่</a>
        `;
    } else {
        roleLinks = `
            <a class="dropdown-item" href="/activity/register"><i class="bi bi-person-plus me-2"></i>ลงทะเบียนกิจกรรม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-star me-2"></i>ประเมินกิจกรรม</a>
            <a class="dropdown-item" href="/qa/questions"><i class="bi bi-question-circle me-2"></i>Q&A เจ้าหน้าที่</a>
        `;
    }

    if (megaMenu) megaMenu.innerHTML = roleLinks;
    if (expandedContainer) expandedContainer.innerHTML = commonLinks + roleLinks.replaceAll('dropdown-item', 'nav-link');
}

function updateSidebarList() {
    const list = document.getElementById('eventOverviewList');
    if (!list) return;
    fetch('/api/get_events').then(res => res.json()).then(events => {
        events.sort((a, b) => new Date(a.start) - new Date(b.start));
        list.innerHTML = events.slice(0, 5).map(ev => {
            // ใช้สีเดียวกับปฏิทินใน Sidebar
            let color = "#3788d8";
            if (ev.type === "กิจกรรม") color = "#28a745";
            else if (ev.type === "ประชุม") color = "#ffc107";
            else if (ev.type === "กำหนดส่ง") color = "#dc3545";
            
            return `<div class="d-flex align-items-center mb-3 border-bottom pb-2">
                <div style="width: 4px; height: 32px; background:${color}; border-radius:10px" class="me-3"></div>
                <div>
                    <div class="fw-bold" style="font-size:0.9rem">${ev.title}</div>
                    <small class="text-muted">${new Date(ev.start).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' })}</small>
                </div>
            </div>`;
        }).join('');
    });
}

function deleteEvent() {
    bootstrap.Modal.getInstance(document.getElementById('eventDetailModal')).hide();
    new bootstrap.Modal(document.getElementById('deleteConfirmModal')).show();
}

function executeDelete() {
    fetch(`/api/delete_event_json/${currentEventId}`, { method: 'DELETE' }).then(() => location.reload());
}

function saveEventData() {
    const data = {
    event_title: document.getElementById('eventTitleInput').value,
    start_date: document.getElementById('eventStartInput').value,
    end_date: document.getElementById('eventEndInput').value,
    event_type: document.getElementById('eventTypeInput').value,
    location: document.getElementById('eventLocationInput').value
};
    if (!data.event_title || !data.start_date) return alert('กรุณาระบุชื่อและวันที่');
    fetch('/api/save_event', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
    location.reload();
});
}

function approveEvent() {
    fetch(`/api/approve_event/${currentEventId}`, { method: 'POST' })
        .then(res => res.json()).then(() => location.reload());
}