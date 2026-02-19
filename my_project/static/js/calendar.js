let calendar;
let currentEventId = null;
let userMode = localStorage.getItem('userMode') || 'staff';

document.addEventListener('DOMContentLoaded', function () {
    // แสดงวันที่ปัจจุบัน
    const today = new Date();
    const dateDisplay = document.getElementById('currentDateDisplay');
    if (dateDisplay) {
        dateDisplay.innerText = "วันนี้: " + today.toLocaleDateString('th-TH', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
    }

    // แก้ไข: โหลดปฏิทินทันทีที่มี element #calendar โดยไม่สนเส้นทาง
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
            events: '/api/get_events',
            eventClick: function (info) {
                currentEventId = info.event.id;
                document.getElementById('viewTitle').innerText = info.event.title;
                document.getElementById('viewStart').innerText = info.event.start.toLocaleDateString('th-TH');
                document.getElementById('viewEnd').innerText = info.event.end ? info.event.end.toLocaleDateString('th-TH') : info.event.start.toLocaleDateString('th-TH');
                document.getElementById('viewLocation').innerText = info.event.extendedProps.location || '-';
                document.getElementById('viewDesc').innerText = info.event.extendedProps.description || '-';
                
                const delBtn = document.getElementById('delBtn');
                if (delBtn) delBtn.style.display = (userMode === 'student') ? 'none' : 'block';
                
                new bootstrap.Modal(document.getElementById('eventDetailModal')).show();
            }
        });
        calendar.render();
    }
    
    updateSidebarList();
    applyModeSettings();
});

function changeMode(role) {
    userMode = role;
    localStorage.setItem('userMode', role);
    location.reload();
}

function applyModeSettings() {
    const addBtn = document.getElementById('addEventBtn');
    const addNewsBtn = document.getElementById('addNewsBtn');
    const roleProfileText = document.getElementById('userRoleProfile');
    const modeText = document.getElementById('currentModeText');
    
    // จัดการทั้ง Hamburger (Grid) และ Horizontal (Mega Menu)
    const expandedContainer = document.getElementById('expandedFunctions');
    const megaMenu = document.getElementById('megaMenuContent');

    if (roleProfileText) {
        if (userMode === 'staff') roleProfileText.innerText = "เจ้าหน้าที่";
        else if (userMode === 'club') roleProfileText.innerText = "นักศึกษาสโมสร";
        else roleProfileText.innerText = "นักศึกษา";
    }

    if (modeText) modeText.innerText = (userMode === 'staff') ? "Staff Mode" : (userMode === 'club' ? "Club Mode" : "Student Mode");
    if (addBtn) addBtn.style.display = (userMode === 'student') ? 'none' : 'block';
    if (addNewsBtn) addNewsBtn.style.display = (userMode === 'student') ? 'none' : 'block';

    const path = window.location.pathname;
    let menuItems = `
        <a class="nav-link ${path === '/news' ? 'active' : ''}" href="/news"><i class="bi bi-megaphone me-2"></i>ข่าวประชาสัมพันธ์</a>
        <a class="nav-link ${path === '/calendar' ? 'active' : ''}" href="/calendar"><i class="bi bi-calendar3 me-2"></i>ปฏิทินกิจกรรม</a>
    `;

    let roleLinks = "";
    if (userMode === 'staff') {
        roleLinks = `
            <a class="dropdown-item" href="#"><i class="bi bi-file-earmark-check me-2"></i>ตรวจทานเอกสาร</a>
            <a class="dropdown-item" href="#"><i class="bi bi-clipboard-check me-2"></i>ตรวจโครงการ</a>
            <a class="dropdown-item" href="#"><i class="bi bi-chat-dots me-2"></i>Q&A เจ้าหน้าที่</a>
        `;
    } else if (userMode === 'club') {
        roleLinks = `
            <a class="dropdown-item" href="#"><i class="bi bi-plus-circle me-2"></i>สร้างกิจกรรม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-cash-stack me-2"></i>บันทึกค่าใช้จ่าย</a>
            <a class="dropdown-item" href="#"><i class="bi bi-geo-alt me-2"></i>ข้อมูลสถานที่</a>
            <a class="dropdown-item" href="#"><i class="bi bi-file-earmark-text me-2"></i>สร้างฟอร์ม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-person-plus me-2"></i>รับสมัครอาสา</a>
            <a class="dropdown-item" href="#"><i class="bi bi-tools me-2"></i>ข้อมูลอุปกรณ์</a>
            <a class="dropdown-item" href="#"><i class="bi bi-chat-dots me-2"></i>Q&A เจ้าหน้าที่</a>
        `;
    } else {
        roleLinks = `
            <a class="dropdown-item" href="#"><i class="bi bi-list-ul me-2"></i>รายชื่อกิจกรรม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-images me-2"></i>ภาพกิจกรรม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-star me-2"></i>ประเมินกิจกรรม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-question-circle me-2"></i>Q&A เจ้าหน้าที่</a>
        `;
    }

    if (megaMenu) megaMenu.innerHTML = roleLinks;
    if (expandedContainer) expandedContainer.innerHTML = menuItems + roleLinks.replaceAll('dropdown-item', 'nav-link');
}

function updateSidebarList() {
    const list = document.getElementById('eventOverviewList');
    if (!list) return;
    fetch('/api/get_events').then(res => res.json()).then(events => {
        events.sort((a, b) => new Date(a.start) - new Date(b.start));
        list.innerHTML = events.slice(0, 5).map(ev => `<div class="d-flex align-items-center mb-3 border-bottom pb-2"><div style="width: 4px; height: 32px; background:${ev.backgroundColor}; border-radius:10px" class="me-3"></div><div><div class="fw-bold" style="font-size:0.9rem">${ev.title}</div><small class="text-muted">${new Date(ev.start).toLocaleDateString('th-TH', {day:'numeric', month:'short'})}</small></div></div>`).join('');
    });
}

function deleteEvent() { bootstrap.Modal.getInstance(document.getElementById('eventDetailModal')).hide(); new bootstrap.Modal(document.getElementById('deleteConfirmModal')).show(); }
function executeDelete() { fetch(`/api/delete_event_json/${currentEventId}`, { method: 'DELETE' }).then(() => location.reload()); }
function saveEventData() {
    const data = {
        title: document.getElementById('eventTitleInput').value,
        start_date: document.getElementById('eventStartInput').value,
        end_date: document.getElementById('eventEndInput').value,
        type: document.getElementById('eventTypeInput').value,
        location: document.getElementById('eventLocationInput').value,
        description: document.getElementById('eventDescInput').value
    };
    if (!data.title || !data.start_date) return alert('กรุณาระบุชื่อและวันที่');
    fetch('/api/save_event', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
    .then(res => res.json()).then(result => { if (result.status === 'success') location.reload(); });
}