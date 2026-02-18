let calendar;
let currentEventId = null;
// ดึงบทบาทจากหน่วยความจำบราวเซอร์ (ถ้าไม่มีให้เริ่มต้นที่ 'staff')
let userMode = localStorage.getItem('userMode') || 'staff';

document.addEventListener('DOMContentLoaded', function () {
    // 1. แสดงวันที่ปัจจุบันใต้หัวข้อหน้าปฏิทิน
    const today = new Date();
    const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
    const dateDisplay = document.getElementById('currentDateDisplay');
    if (dateDisplay) {
        dateDisplay.innerText = "วันนี้: " + today.toLocaleDateString('th-TH', options);
    }

    // 2. ตั้งค่าการทำงานของ FullCalendar
    var calendarEl = document.getElementById('calendar');
    if (calendarEl) {
        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'th',
            titleFormat: { year: 'numeric', month: 'long' },
            headerToolbar: { 
                left: 'prev,next today', 
                center: 'title', 
                right: 'dayGridMonth,listMonth' 
            },
            events: '/api/get_events',
            nowIndicator: true,
            eventClick: function (info) {
                currentEventId = info.event.id;
                const props = info.event.extendedProps;
                
                // ใส่ข้อมูลลงใน Modal รายละเอียดกิจกรรม
                document.getElementById('viewTitle').innerText = info.event.title;
                document.getElementById('viewStart').innerText = info.event.start.toLocaleDateString('th-TH');
                document.getElementById('viewEnd').innerText = info.event.end ? 
                    info.event.end.toLocaleDateString('th-TH') : info.event.start.toLocaleDateString('th-TH');
                document.getElementById('viewLocation').innerText = props.location || '-';
                document.getElementById('viewDesc').innerText = props.description || '-';

                // ควบคุมการแสดงผลปุ่มลบ (นักศึกษาไม่มีสิทธิ์ลบ)
                const delBtn = document.getElementById('delBtn');
                if (delBtn) {
                    delBtn.style.display = (userMode === 'student') ? 'none' : 'block';
                }
                
                new bootstrap.Modal(document.getElementById('eventDetailModal')).show();
            }
        });
        calendar.render();
    }

    // 3. เรียกฟังก์ชันอัปเดตรายการภาพรวมกิจกรรมด้านข้าง
    updateEventList();
    
    // 4. ตั้งค่าสิทธิ์และการแสดงผลเมนูตามบทบาททันทีเมื่อโหลดหน้า
    applyModeSettings();
});

// ฟังก์ชันสลับบทบาทผู้ใช้งาน
function changeMode(role) {
    userMode = role;
    localStorage.setItem('userMode', role);
    location.reload(); // รีโหลดหน้าเพื่ออัปเดตสิทธิ์และ UI ทั้งหมด
}

// ฟังก์ชันควบคุมสิทธิ์และการแสดงผลเมนูเพิ่มเติม
function applyModeSettings() {
    const addBtn = document.getElementById('addEventBtn'); // ปุ่มเพิ่มกิจกรรมหน้าปฏิทิน
    const addNewsBtn = document.getElementById('addNewsBtn'); // ปุ่มเพิ่มข่าวหน้าประชาสัมพันธ์
    const modeText = document.getElementById('currentModeText');
    const menuContainer = document.getElementById('megaMenuContent');
    const roleProfileText = document.getElementById('userRoleProfile');

    // 1. อัปเดตชื่อบทบาทในโปรไฟล์ดรอปดาวน์
    if (roleProfileText) {
        if (userMode === 'staff') roleProfileText.innerText = "เจ้าหน้าที่";
        else if (userMode === 'club') roleProfileText.innerText = "นักศึกษาสโมสร";
        else roleProfileText.innerText = "นักศึกษา";
    }

    // 2. อัปเดตข้อความที่ปุ่มสลับโหมดมุมล่างซ้าย
    if (modeText) {
        modeText.innerText = (userMode === 'staff') ? "Staff Mode" : 
                            (userMode === 'club' ? "Club Mode" : "Student Mode");
    }
    
    // 3. ซ่อนหรือแสดงปุ่มเพิ่มข้อมูล (นักศึกษา View Only)
    if (addBtn) addBtn.style.display = (userMode === 'student') ? 'none' : 'block';
    if (addNewsBtn) addNewsBtn.style.display = (userMode === 'student') ? 'none' : 'block';
    
    // 4. จัดการเนื้อหาเมนู "เพิ่มเติม" แบบ 3 คอลัมน์ตามโหมด
    if (menuContainer) {
        if (userMode === 'staff') {
            // เมนูสำหรับเจ้าหน้าที่ (Staff)
            menuContainer.innerHTML = `
                <div class="col-md-4 border-end-md">
                    <li><a class="dropdown-item py-3" href="#"><i class="bi bi-file-earmark-check me-2 text-warning"></i>ตรวจทานเอกสาร</a></li>
                </div>
                <div class="col-md-4 border-end-md">
                    <li><a class="dropdown-item py-3" href="#"><i class="bi bi-clipboard-check me-2 text-warning"></i>ตรวจทานรายงานโครงการ</a></li>
                </div>
                <div class="col-md-4">
                    <li><a class="dropdown-item py-3" href="#"><i class="bi bi-chat-dots me-2 text-warning"></i>Q&A เจ้าหน้าที่</a></li>
                </div>`;
        } else if (userMode === 'club') {
            // เมนูสำหรับนักศึกษาสโมสร (Club) - แก้ไขให้ตรงตามความต้องการ
            menuContainer.innerHTML = `
                <div class="col-md-4 border-end-md">
                    <li><a class="dropdown-item py-2" href="#"><i class="bi bi-plus-circle me-2 text-warning"></i>สร้างกิจกรรม</a></li>
                    <li><a class="dropdown-item py-2" href="#"><i class="bi bi-cash-stack me-2 text-warning"></i>บันทึกค่าใช้จ่าย</a></li>
                    <li><a class="dropdown-item py-2" href="#"><i class="bi bi-geo-alt me-2 text-warning"></i>ข้อมูลสถานที่</a></li>
                </div>
                <div class="col-md-4 border-end-md">
                    <li><a class="dropdown-item py-2" href="#"><i class="bi bi-file-earmark-text me-2 text-warning"></i>สร้างฟอร์มลงทะเบียน</a></li>
                    <li><a class="dropdown-item py-2" href="#"><i class="bi bi-person-plus me-2 text-warning"></i>รับสมัครจิตอาสา</a></li>
                    <li><a class="dropdown-item py-2" href="#"><i class="bi bi-tools me-2 text-warning"></i>ข้อมูลอุปกรณ์</a></li>
                </div>
                <div class="col-md-4">
                    <li><a class="dropdown-item py-2" href="#"><i class="bi bi-chat-dots me-2 text-warning"></i>Q&A เจ้าหน้าที่</a></li>
                </div>`;
        } else {
            // เมนูสำหรับนักศึกษา (Student) - แก้ไขให้ตรงตามความต้องการ
            menuContainer.innerHTML = `
                <div class="col-md-6 border-end-md">
                    <li><a class="dropdown-item py-3" href="#"><i class="bi bi-list-ul me-2 text-warning"></i>รายชื่อกิจกรรม</a></li>
                    <li><a class="dropdown-item py-3" href="#"><i class="bi bi-images me-2 text-warning"></i>ภาพกิจกรรม</a></li>
                </div>
                <div class="col-md-6">
                    <li><a class="dropdown-item py-3" href="#"><i class="bi bi-star me-2 text-warning"></i>ประเมินกิจกรรม</a></li>
                    <li><a class="dropdown-item py-3" href="#"><i class="bi bi-question-circle me-2 text-warning"></i>Q&A เจ้าหน้าที่</a></li>
                </div>`;
        }
    }
}

// ฟังก์ชันอัปเดตรายการกิจกรรมแบบลิสต์ (Sidebar)
function updateEventList() {
    fetch('/api/get_events')
        .then(res => res.json())
        .then(events => {
            const listContainer = document.getElementById('eventOverviewList');
            if (!listContainer) return;
            
            if (events.length === 0) {
                listContainer.innerHTML = '<p class="text-muted text-center py-3">ไม่มีกิจกรรมในขณะนี้</p>';
                return;
            }

            // เรียงลำดับตามวันที่จากใกล้สุดไปไกลสุด
            events.sort((a, b) => new Date(a.start) - new Date(b.start));

            // แสดงสูงสุด 5 กิจกรรมล่าสุด
            listContainer.innerHTML = events.slice(0, 5).map(ev => {
                const dateStr = new Date(ev.start).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });
                return `
                    <div class="d-flex align-items-start mb-3 border-bottom pb-2">
                        <div style="width: 4px; height: 35px; background:${ev.backgroundColor}; border-radius:10px" class="me-3"></div>
                        <div>
                            <div class="fw-bold text-dark" style="font-size:0.9rem">${ev.title}</div>
                            <div class="text-muted small">
                                <i class="bi bi-clock me-1"></i> ${dateStr}
                            </div>
                        </div>
                    </div>`;
            }).join('');
        });
}

// ฟังก์ชันบันทึกข้อมูลกิจกรรมใหม่ (สำหรับหน้าปฏิทิน)
function saveEventData() {
    const data = {
        title: document.getElementById('eventTitleInput').value,
        start_date: document.getElementById('eventStartInput').value,
        end_date: document.getElementById('eventEndInput').value,
        type: document.getElementById('eventTypeInput').value,
        location: document.getElementById('eventLocationInput').value,
        description: document.getElementById('eventDescInput').value
    };

    if (!data.title || !data.start_date) {
        return alert('กรุณาระบุชื่อกิจกรรมและวันที่เริ่มกิจกรรม');
    }

    fetch('/api/save_event', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' }, 
        body: JSON.stringify(data) 
    })
    .then(response => res.json())
    .then(result => {
        if (result.status === 'success') {
            // ปิดหน้าต่างเพิ่มกิจกรรม
            bootstrap.Modal.getInstance(document.getElementById('addModal')).hide();
            // แสดงหน้าต่างสำเร็จ
            new bootstrap.Modal(document.getElementById('saveSuccessModal')).show();
        } else {
            alert('เกิดข้อผิดพลาด: ' + result.message);
        }
    })
    .catch(error => console.error('Error saving event:', error));
}

// ฟังก์ชันเปิดหน้าต่างยืนยันการลบ
function deleteEvent() {
    if (!currentEventId) return;
    
    // ปิด Modal รายละเอียดก่อน
    const detailModal = bootstrap.Modal.getInstance(document.getElementById('eventDetailModal'));
    if (detailModal) detailModal.hide();
    
    // เปิด Modal ยืนยันการลบแบบกึ่งกลางหน้าจอ
    new bootstrap.Modal(document.getElementById('deleteConfirmModal')).show();
}

// ฟังก์ชันลบกิจกรรมจริงหลังจากกดยืนยัน
function executeDelete() {
    if (!currentEventId) return;

    fetch(`/api/delete_event_json/${currentEventId}`, { method: 'DELETE' })
    .then(response => res.json())
    .then(result => {
        if (result.status === 'success') {
            location.reload(); // รีโหลดเพื่ออัปเดตปฏิทิน
        } else {
            alert('เกิดข้อผิดพลาดในการลบ: ' + result.message);
        }
    })
    .catch(error => console.error('Error deleting event:', error));
}