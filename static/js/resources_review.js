let items = [];

async function loadData() {
    const placesRes = await fetch("/api/places");
    const places = await placesRes.json();

    const eqRes = await fetch("/api/equipments");
    const equipments = await eqRes.json();

    items = [];

    // ROOM
    places.forEach((p) => {
        items.push({
            type: "room",
            roomNum: p.name,
            description: p.description,
            roomContact: `${p.officer_name} (${p.officer_phone})`,
            status: Number(p.status) === 1 ? "เปิดใช้งาน" : "ปิดใช้งาน",
            image: p.image || "https://via.placeholder.com/200x170",
            tools: p.equipments
                .filter((e) => e && e.name && e.quantity > 0)
                .map((e) => `${e.name} (${e.quantity})`),
        });
    });

    // EQUIPMENT
    equipments.forEach((e) => {
        items.push({
            type: "tool",
            toolCode: e.code,
            toolType: e.name,
            category: e.category,
            total: e.total_quantity,
            available: e.available_quantity,
            department: e.department,
        });
    });

    renderItems();
}

function renderItems() {
    const container = document.getElementById("dataContainer");
    const empty = document.getElementById("emptyState");
    const search = document.getElementById("searchInput").value.toLowerCase();

    container.innerHTML = "";

    const filtered = items.filter((item) => {
        if (item.type === "room") {
            return (item.roomNum || "").toLowerCase().includes(search);
        }

        if (item.type === "tool") {
            return (
                (item.toolType || "").toLowerCase().includes(search) ||
                (item.toolCode || "").toLowerCase().includes(search)
            );
        }

        return true;
    });

    if (filtered.length === 0) {
        empty.classList.remove("hidden");
        return;
    }

    empty.classList.add("hidden");

    filtered.forEach((item, index) => {
        const div = document.createElement("div");
        div.className = "card mb-3 shadow-sm p-3";

        let statusColor = item.status === "เปิดใช้งาน" ? "bg-success" : "bg-danger";

        if (item.type === "room") {
            div.innerHTML = `

<div class="d-flex gap-4">

<div>
<img src="${item.image}"
style="
width:200px;
height:170px;
object-fit:cover;
border-radius:10px;
">
</div>

<div style="flex:1">

<h5 class="mb-1">
${item.roomNum}
</h5>

<p class="mb-2">
<i class="bi bi-info-circle"></i> 
<span class="detail-title">รายละเอียด:</span>
${item.description || ""}
</p>

<p class="mb-2">
<i class="bi bi-person"></i> 
<span class="detail-title">ผู้ดูแล:</span>
${item.roomContact}
</p>

<div class="mb-2">
<i class="bi bi-tools"></i> 
<span class="detail-title">อุปกรณ์:</span>
${item.tools
                    .map((t) => `<span class="badge bg-primary me-1">${t}</span>`)
                    .join("")}

</div>

<i class="bi bi-check-circle"></i>
<span class="detail-title">สถานะ:</span>
<span class="badge ${statusColor} mb-2">
${item.status}
</span>

<br>

<div class="text-end">
<button class="btn btn-outline-primary btn-sm mt-2"
onclick="openRoom(${index})">
ดูรายละเอียด
</button>
</div>

</div>

</div>
`;
        }

        if (item.type === "tool") {
            const percent = (item.available / item.total) * 100;

            let color = "bg-success";

            if (percent <= 30) {
                color = "bg-danger";
            } else if (percent <= 70) {
                color = "bg-warning";
            }

            div.innerHTML = `

<div class="d-flex flex-column">

<h5 class="mb-2">
ชื่ออุปกรณ์ : ${item.toolType}
</h5>

<div class="text-muted mb-2">
รหัสอุปกรณ์ : ${item.toolCode} <br>
หมวดหมู่ : ${item.category} <br>
จำนวนทั้งหมด : ${item.total} <br>
ว่าง : ${item.available} <br>
หน่วยงานที่รับผิดชอบ : ${item.department}
</div>

<div class="d-flex align-items-center justify-content-between mt-2">

<div class="progress mb-2" style="height:10px;width:300px;">
<div class="progress-bar ${color}" role="progressbar"
style="width:${percent}%">
</div>
</div>

<span class="badge bg-success fs-6 ms-3">
${item.available} ว่าง
</span>

</div>

</div>

`;
        }

        container.appendChild(div);
    });
}

function openRoom(index) {
    const room = items[index];

    document.getElementById("modalRoomTitle").innerText = "" + room.roomNum;

    document.getElementById("modalRoomDesc").innerText = room.description;

    document.getElementById("modalRoomContact").innerText = room.roomContact;

    document.getElementById("modalRoomImage").src = room.image;

    const statusEl = document.getElementById("modalRoomStatus");

    statusEl.innerText = room.status;

    if (room.status === "เปิดใช้งาน") {
        statusEl.className = "badge bg-success fs-6";
    } else {
        statusEl.className = "badge bg-danger fs-6";
    }

    const tools = document.getElementById("modalRoomTools");

    tools.innerHTML = "";

    room.tools.forEach((t) => {
        tools.innerHTML += `
<span class="badge bg-primary me-1">${t}</span>
`;
    });

    new bootstrap.Modal(document.getElementById("roomModal")).show();
}

document.addEventListener("DOMContentLoaded", () => {
    loadData();
});