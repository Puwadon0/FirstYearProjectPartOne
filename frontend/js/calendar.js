// Sample Events Data
let events = [
    
];

let calendar;
let selectedEventId = null;

document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    
    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'th',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,listWeek'
        },
        events: events,
        selectable: true,
        eventClick: (info) => showEventDetail(info.event),
        select: (info) => openAddModal(info.start, info.end),
        eventDidMount: function(info) {
            const type = info.event.extendedProps.type;
            if (type === 'activity') info.el.classList.add('badge-activity');
            else if (type === 'meeting') info.el.classList.add('badge-meeting');
            else if (type === 'deadline') info.el.classList.add('badge-deadline');
        }
    });
    
    calendar.render();
    updateUpcomingEvents();
});

function openAddModal(start, end) {
    document.getElementById('eventStartDate').value = start.toISOString().split('T')[0];
    if(end) document.getElementById('eventEndDate').value = end.toISOString().split('T')[0];
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