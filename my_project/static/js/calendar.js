let calendar;
let currentEventId = null;
let userMode = localStorage.getItem('userMode') || 'staff';

document.addEventListener('DOMContentLoaded', function () {
    // 1. แสดงวันที่ปัจจุบันที่หน้าจอ (ถ้ามี element currentDateDisplay)
    const today = new Date();
    const dateDisplay = document.getElementById('currentDateDisplay');
    if (dateDisplay) {
        dateDisplay.innerText = "วันนี้: " + today.toLocaleDateString('th-TH', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
    }

    // 2. ตั้งค่า FullCalendar (โหลดทันทีที่มี element #calendar ในหน้าใดๆ)
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
                
                // แสดงผลวันเริ่มกิจกรรม
                document.getElementById('viewStart').innerText = info.event.start.toLocaleDateString('th-TH');
                
                // จัดการแสดงผลวันจบกิจกรรม (รองรับกรณีหาย)
                const viewEndEl = document.getElementById('viewEnd');
                if (viewEndEl) {
                    if (info.event.allDay && info.event.end) {
                        // FullCalendar เก็บวันจบแบบ Exclusive (+1 วัน) จึงต้องลบออก 1 วันเพื่อแสดงผลจริง
                        let displayEnd = new Date(info.event.end);
                        displayEnd.setDate(displayEnd.getDate() - 1);
                        viewEndEl.innerText = displayEnd.toLocaleDateString('th-TH');
                    } else if (info.event.end) {
                        viewEndEl.innerText = info.event.end.toLocaleDateString('th-TH');
                    } else {
                        // หากไม่มีวันจบ ให้แสดงวันเดียวกันกับวันเริ่ม
                        viewEndEl.innerText = info.event.start.toLocaleDateString('th-TH');
                    }
                }

                document.getElementById('viewLocation').innerText = info.event.extendedProps.location || '-';
                document.getElementById('viewDesc').innerText = info.event.extendedProps.description || '-';
                
                // ซ่อนปุ่มลบหากเป็นโหมดนักศึกษา
                const delBtn = document.getElementById('delBtn');
                if (delBtn) delBtn.style.display = (userMode === 'student') ? 'none' : 'block';
                
                new bootstrap.Modal(document.getElementById('eventDetailModal')).show();
            }
        });
        calendar.render();
    }
    
    // 3. เรียกฟังก์ชันอัปเดตข้อมูล UI ตามโหมดที่เลือก
    updateSidebarList();
    applyModeSettings();
});

// ฟังก์ชันสลับโหมดผู้ใช้งาน (Staff, Club, Student)
function changeMode(role) {
    userMode = role;
    localStorage.setItem('userMode', role);
    location.reload();
}

// ฟังก์ชันจัดการ UI และรายการเมนูตามสิทธิ์ (Role-based Navigation)
function applyModeSettings() {
    const addBtn = document.getElementById('addEventBtn');
    const addNewsBtn = document.getElementById('addNewsBtn');
    const roleProfileText = document.getElementById('userRoleProfile');
    const modeText = document.getElementById('currentModeText');
    const expandedContainer = document.getElementById('expandedFunctions');
    const megaMenu = document.getElementById('megaMenuContent');

    // อัปเดตข้อความแสดงสถานะที่โปรไฟล์
    if (roleProfileText) {
        if (userMode === 'staff') roleProfileText.innerText = "เจ้าหน้าที่";
        else if (userMode === 'club') roleProfileText.innerText = "นักศึกษาสโมสร";
        else roleProfileText.innerText = "นักศึกษา";
    }

    // อัปเดตข้อความที่ปุ่ม Switcher มุมล่างซ้าย
    if (modeText) modeText.innerText = (userMode === 'staff') ? "Staff Mode" : (userMode === 'club' ? "Club Mode" : "Student Mode");
    
    // จัดการการแสดงผลปุ่ม "เพิ่ม" (นักศึกษาจะไม่มีสิทธิ์เห็น)
    if (addBtn) addBtn.style.display = (userMode === 'student') ? 'none' : 'block';
    if (addNewsBtn) addNewsBtn.style.display = (userMode === 'student') ? 'none' : 'block';

    const path = window.location.pathname;
    
    // ลิงก์มาตรฐานที่แสดงใน Navbar หลัก (ถ้าไม่ใช่หน้า Dashboard)
    let commonLinks = `
        <a class="nav-link ${path==='/news'?'active':''}" href="/news"><i class="bi bi-megaphone me-2"></i>ข่าวประชาสัมพันธ์</a>
        <a class="nav-link ${path==='/calendar'?'active':''}" href="/calendar"><i class="bi bi-calendar3 me-2"></i>ปฏิทินกิจกรรม</a>
    `;

    // เตรียมรายการเมนูย่อยตามบทบาท
    let roleLinks = "";
    if (userMode === 'staff') {
        // เมนูสำหรับโหมดเจ้าหน้าที่ (Staff)
        roleLinks = `
            <a class="dropdown-item" href="#"><i class="bi bi-file-earmark-check me-2"></i>ตรวจทานเอกสาร</a>
            <a class="dropdown-item" href="/officer"><i class="bi bi-clipboard-check me-2"></i>ตรวจสอบคำขอกิจกรรม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-people me-2"></i>รายชื่อผู้เข้าร่วมจิตอาสา</a>
            <a class="dropdown-item" href="/officer"><i class="bi bi-journal-plus me-2"></i>คำขอสร้างกิจกรรม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-chat-dots me-2"></i>Q&A เจ้าหน้าที่</a>
        `;
    } else if (userMode === 'club') {
        // เมนูสำหรับโหมดสโมสร (Club)
        roleLinks = `
            <a class="dropdown-item" href="/create-activity"><i class="bi bi-plus-circle me-2"></i>สร้างกิจกรรม</a>
            <a class="dropdown-item" href="/club_status_activity"><i class="bi bi-list-check me-2"></i>สถานะคำขอ</a>
            <a class="dropdown-item" href="#"><i class="bi bi-cash-stack me-2"></i>บันทึกค่าใช้จ่าย</a>
            <a class="dropdown-item" href="#"><i class="bi bi-geo-alt me-2"></i>ข้อมูลสถานที่</a>
            <a class="dropdown-item" href="#"><i class="bi bi-file-earmark-text me-2"></i>สร้างฟอร์ม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-person-plus me-2"></i>รับสมัครอาสา</a>
            <a class="dropdown-item" href="#"><i class="bi bi-chat-dots me-2"></i>Q&A เจ้าหน้าที่</a>
        `;
    } else {
        // เมนูสำหรับโหมดนักศึกษา (Student)
        roleLinks = `
            <a class="dropdown-item" href="#"><i class="bi bi-list-ul me-2"></i>รายชื่อกิจกรรม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-images me-2"></i>ภาพกิจกรรม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-star me-2"></i>ประเมินกิจกรรม</a>
            <a class="dropdown-item" href="#"><i class="bi bi-question-circle me-2"></i>Q&A เจ้าหน้าที่</a>
        `;
    }

    // กรณีหน้า Dashboard: ใส่ลงใน Mega Menu (Dropdown)
    if (megaMenu) megaMenu.innerHTML = roleLinks;
    
    // กรณีหน้าอื่นๆ: ใส่ลงใน Hamburger Menu (Grid)
    if (expandedContainer) {
        expandedContainer.innerHTML = commonLinks + roleLinks.replaceAll('dropdown-item', 'nav-link');
    }
}

// ฟังก์ชันอัปเดตรายการกิจกรรมภาพรวม (Sidebar)
function updateSidebarList() {
    const list = document.getElementById('eventOverviewList');
    if (!list) return;

    fetch('/api/get_events')
        .then(res => res.json())
        .then(events => {
            if (events.length === 0) {
                list.innerHTML = '<p class="text-muted text-center py-3">ไม่มีกิจกรรม</p>';
                return;
            }
            events.sort((a, b) => new Date(a.start) - new Date(b.start));
            list.innerHTML = events.slice(0, 5).map(ev => `
                <div class="d-flex align-items-center mb-3 border-bottom pb-2">
                    <div style="width: 4px; height: 32px; background:${ev.backgroundColor}; border-radius:10px" class="me-3"></div>
                    <div>
                        <div class="fw-bold" style="font-size:0.9rem">${ev.title}</div>
                        <small class="text-muted">${new Date(ev.start).toLocaleDateString('th-TH', {day:'numeric', month:'short'})}</small>
                    </div>
                </div>
            `).join('');
        });
}

// ฟังก์ชันเปิด Modal ยืนยันการลบ
function deleteEvent() { 
    bootstrap.Modal.getInstance(document.getElementById('eventDetailModal')).hide(); 
    new bootstrap.Modal(document.getElementById('deleteConfirmModal')).show(); 
}

// ฟังก์ชันดำเนินการลบข้อมูลผ่าน API
function executeDelete() { 
    if (!currentEventId) return;
    fetch(`/api/delete_event_json/${currentEventId}`, { method: 'DELETE' })
        .then(res => res.json())
        .then(result => {
            if (result.status === 'success') location.reload();
        });
}

// ฟังก์ชันบันทึกกิจกรรมใหม่
function saveEventData() {
    const data = {
        title: document.getElementById('eventTitleInput').value,
        start_date: document.getElementById('eventStartInput').value,
        end_date: document.getElementById('eventEndInput').value,
        type: document.getElementById('eventTypeInput').value,
        location: document.getElementById('eventLocationInput').value,
        description: document.getElementById('eventDescInput').value
    };
    
    if (!data.title || !data.start_date) return alert('กรุณาระบุชื่อและวันที่กิจกรรม');
    
    fetch('/api/save_event', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' }, 
        body: JSON.stringify(data) 
    })
    .then(res => res.json())
    .then(result => { 
        if (result.status === 'success') location.reload(); 
    });
}