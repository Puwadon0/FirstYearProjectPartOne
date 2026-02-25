function openViewModal(btn) {
  const d = btn.dataset;
  document.getElementById("v_name").textContent       = d.name       || "-";
  document.getElementById("v_department").textContent = d.department || "-";
  document.getElementById("v_fiscalyear").textContent = d.fiscalyear || "-";
  document.getElementById("v_createdby").textContent  = d.createdby  || "-";
  document.getElementById("v_phone").textContent      = d.phone      || "-";
  document.getElementById("v_datetime").textContent   = d.datetime   || "-";
  document.getElementById("v_location").textContent   = d.location   || "-";
  document.getElementById("v_address").textContent    = d.address    || "-";
  document.getElementById("v_std").textContent        = d.std        || "0";
  document.getElementById("v_other").textContent      = d.other      || "0";
  document.getElementById("v_detail").textContent     = d.detail     || "-";
  document.getElementById("v_steps").textContent      = d.steps      || "-";
  document.getElementById("v_qa").textContent         = d.qa         || "-";
  const cost = parseFloat(d.cost) || 0;
  document.getElementById("v_cost").textContent =
    cost.toLocaleString("th-TH", { minimumFractionDigits: 0 }) + " บาท";

  const fileContainer = document.getElementById("v_file_container");
  if (d.file && d.file.trim() !== "") {
    fileContainer.innerHTML =
      `<a href="/static/uploads/${d.file}" target="_blank" 
         class="inline-flex items-center gap-1 text-blue-600 underline hover:text-blue-800 text-sm">
         📎 ดูไฟล์โครงการ
       </a>`;
  } else {
    fileContainer.innerHTML =
      `<span class="text-gray-400 text-sm">ไม่มีไฟล์แนบ</span>`;
  }

  const statusEl = document.getElementById("v_status");
  const statusMap = {
    pending:  { label: "รออนุมัติ",   cls: "px-3 py-1 rounded-full text-xs bg-yellow-100 text-yellow-700 font-bold" },
    approved: { label: "อนุมัติแล้ว", cls: "px-3 py-1 rounded-full text-xs bg-green-100 text-green-700 font-bold" },
    rejected: { label: "ไม่อนุมัติ",  cls: "px-3 py-1 rounded-full text-xs bg-red-100 text-red-700 font-bold" },
  };
  const s = statusMap[d.status] || { label: d.status || "-", cls: "px-3 py-1 rounded-full text-xs bg-gray-100 text-gray-600 font-bold" };
  statusEl.innerHTML = `<span class="${s.cls}">${s.label}</span>`;
  document.getElementById("viewModal").classList.remove("hidden");
}

function closeViewModal() {
  document.getElementById("viewModal").classList.add("hidden");
}
// ฟังก์ชันสำหรับกรองข้อมูลในตาราง
function filterStatus(status) {
    const rows = document.querySelectorAll('.activity-row');
    const buttons = document.querySelectorAll('.filter-btn');

    // 1. จัดการเรื่องสีของปุ่ม (Active State)
    buttons.forEach(btn => {
        btn.classList.remove('bg-blue-600', 'bg-yellow-500', 'bg-green-500', 'bg-red-500', 'text-white');
        btn.classList.add('bg-gray-200', 'text-gray-700');
    });

    // ใส่สีให้ปุ่มที่ถูกกด (ตัวอย่างสีตามสถานะ)
    const activeBtn = document.getElementById('btn-' + status);
    activeBtn.classList.remove('bg-gray-200', 'text-gray-700');
    if(status === 'all') activeBtn.classList.add('bg-blue-600', 'text-white');
    if(status === 'pending') activeBtn.classList.add('bg-yellow-500', 'text-white');
    if(status === 'approved') activeBtn.classList.add('bg-green-500', 'text-white');
    if(status === 'rejected') activeBtn.classList.add('bg-red-500', 'text-white');

    // 2. กรองแถวในตาราง
    rows.forEach(row => {
        if (status === 'all') {
            row.style.display = ''; // แสดงทั้งหมด
        } else {
            if (row.getAttribute('data-status') === status) {
                row.style.display = ''; // ตรงกับสถานะ ให้แสดง
            } else {
                row.style.display = 'none'; // ไม่ตรง ให้ซ่อน
            }
        }
    });
}

// โค้ดเดิมของคุณ (openViewModal, closeViewModal) ให้คงไว้ด้านล่าง...

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("viewModal").addEventListener("click", function (e) {
    if (e.target === this) closeViewModal();
  });

  

  document.querySelectorAll(".view-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      openViewModal(this);
    });
  });
});

