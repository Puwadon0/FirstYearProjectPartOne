let currentFilter = "student";

function loadUsers(role, btn = null) {
  currentFilter = role;

  document
    .querySelectorAll(".role-btn")
    .forEach((b) => b.classList.remove("active"));

  localStorage.setItem("selectedRole", role);

  if (btn) btn.classList.add("active");

  const url = role === "club" ? "/clubs/all" : `/admin/get-users/${role}`;

  fetch(url)
    .then((res) => res.json())
    .then((data) => {
      if (!Array.isArray(data)) {
        console.error("Server error:", data);
        alert(data.error || "เกิดข้อผิดพลาด");
        return;
      }

      const thead = document.querySelector("#userTable thead tr");
      const tbody = document.querySelector("#userTable tbody");

      tbody.innerHTML = "";

      if (role === "club") {
        thead.innerHTML = `
    <th>รหัสนักศึกษา</th>
    <th>ชื่อ-นามสกุล</th>
    <th>คณะ</th>
    <th>สาขา</th>
    <th>ชั้นปี</th>
    <th>Email</th>
    <th>เบอร์</th>
    <th>ตำแหน่ง</th>
    <th>เข้าใช้ล่าสุด</th>
    <th>สร้างเมื่อ</th>
    <th>จัดการ</th>
  `;
      } else if (role === "officer") {
        thead.innerHTML = `
    <th>รหัสเจ้าหน้าที่</th>
    <th>ชื่อ-นามสกุล</th>
    <th>หน่วยงาน</th>
    <th>Email</th>
    <th>เบอร์</th>
    <th>เข้าใช้ล่าสุด</th>
    <th>สร้างเมื่อ</th>
    <th>จัดการ</th>
  `;
      } else {
        thead.innerHTML = `
    <th>รหัสนักศึกษา</th>
    <th>ชื่อ-นามสกุล</th>
    <th>คณะ</th>
    <th>สาขา</th>
    <th>ชั้นปี</th>
    <th>Email</th>
    <th>เบอร์</th>
    <th>เข้าใช้ล่าสุด</th>
    <th>สร้างเมื่อ</th>
    <th>จัดการ</th>
  `;
      }
      if (role === "officer") {
        data.forEach((u) => {
          tbody.innerHTML += `
      <tr>
        <td>${u.officer_id}</td>
        <td>${u.full_name}</td>
        <td>${u.department || "-"}</td>
        <td>${u.email || "-"}</td>
        <td>${u.phone || "-"}</td>
        <td>${u.last_login || "-"}</td>
        <td>${u.created_at || "-"}</td>
        <td>
          <button class="btn btn-sm btn-edit-modern" 
          onclick='openEditModal(${JSON.stringify(u)})'>
              <i class="bi bi-pencil"></i>
          </button>
          
          <button class="btn btn-sm btn-delete-modern"
              onclick="deleteOfficer('${u.officer_id}')">
              <i class="bi bi-person-x-fill"></i>
          </button>
        </td>
      </tr>
    `;
        });

        setTimeout(() => {
          document.querySelectorAll(".edit-btn").forEach((btn) => {
            btn.addEventListener("click", function () {
              const user = JSON.parse(this.dataset.user);
              openEditModal(user);
            });
          });
        }, 0);

        return;
      }

      data.forEach((u) => {
        const name = u.first_name
          ? `${u.first_name} ${u.last_name || ""}`
          : u.name;

        tbody.innerHTML += `
          <tr>
            <td>${u.student_id}</td>
            <td>${name || "-"}</td>
            <td>${u.faculty || "-"}</td>
            <td>${u.major || "-"}</td>
            <td>${u.year || "-"}</td>
            <td>${u.email || "-"}</td>
            <td>${u.phone || "-"}</td>

            ${
              role === "club"
                ? `<td><span class="badge bg-primary">${u.position}</span></td>`
                : ""
            }

            <td>${u.last_login || "-"}</td>
            <td>${u.created_at || "-"}</td>

           <td>
              <button class="btn btn-sm btn-edit-modern me-1"
                onclick='openEditModal(${JSON.stringify(u)})'>
                <i class="bi bi-pencil"></i>
              </button>
              ${
                role === "club"
                  ? `<button class="btn btn-sm btn-delete-modern"
                      onclick="removeFromClub('${u.student_id}')">
                      <i class="bi bi-person-x-fill"></i>
                    </button>`
                  : `<button class="btn btn-sm btn-delete-modern"
                      onclick="deleteUser('${u.student_id}')">
                      <i class="bi bi-person-x-fill"></i>
                    </button>`
              }
           </td>
        </tr>
        `;
      });
    });
}

const roleSelect = document.getElementById("role");
const dynamicFields = document.getElementById("dynamicFields");

roleSelect.addEventListener("change", function () {
  const role = this.value;
  dynamicFields.innerHTML = "";

  if (role === "officer") {
    dynamicFields.innerHTML = `
    <div class="col-md-3">
      <input type="text" class="form-control" id="officer_id" placeholder="รหัสประจำตัวเจ้าหน้าที่" required>
    </div>
    <div class="col-md-3">
      <input type="text" class="form-control" id="full_name" placeholder="ชื่อ-นามสกุล" required>
    </div>
    <div class="col-md-3">
      <input type="text" class="form-control" id="department" placeholder="หน่วยงานที่สังกัด">
    </div>
    <div class="col-md-3">
      <input type="email" class="form-control" id="email" placeholder="Email">
    </div>
    <div class="col-md-3">
      <input type="text" class="form-control" id="phone" placeholder="เบอร์โทรศัพท์">
    </div>

<div class="col-md-3">
  <div class="input-group">
    <input type="password" class="form-control position-relative" id="password" placeholder="ตั้งรหัสผ่าน" required>
    <button class="btn border-0 toggle-password" type="button" data-target="password">
      <i class="bi bi-eye-slash"></i>
    </button>
  </div>
</div>

<div class="col-md-3">
  <div class="input-group">
    <input type="password" class="form-control" id="confirm_password" placeholder="ยืนยันรหัสผ่าน" required>
    <button class="btn border-0 toggle-password" type="button" data-target="confirm_password">
      <i class="bi bi-eye-slash"></i>
    </button>
  </div>
</div>
  `;
  }

  if (role === "student") {
    dynamicFields.innerHTML = `
    <div class="col-md-3">
      <input type="text" class="form-control" id="uid" placeholder="รหัสนักศึกษา" required>
    </div>
    <div class="col-md-3">
      <input type="text" class="form-control" id="name" placeholder="ชื่อ-นามสกุล" required>
    </div>
    <div class="col-md-3">
      <input type="text" class="form-control" id="faculty" placeholder="คณะ">
    </div>
    <div class="col-md-3">
      <input type="text" class="form-control" id="major" placeholder="สาขา">
    </div>
    <div class="col-md-2">
      <input type="text" class="form-control" id="year" placeholder="ชั้นปี">
    </div>
    <div class="col-md-2">
      <input type="email" class="form-control" id="email" placeholder="Email">
    </div>
    <div class="col-md-2">
      <input type="text" class="form-control" id="phone" placeholder="เบอร์โทรศัพท์">
    </div>

<div class="col-md-3">
  <div class="input-group">
    <input type="password" class="form-control" id="password" placeholder="ตั้งรหัสผ่าน" required>
    <button class="btn border-0 toggle-password" type="button" data-target="password">
      <i class="bi bi-eye-slash"></i>
    </button>
  </div>
</div>

<div class="col-md-3">
  <div class="input-group">
    <input type="password" class="form-control" id="confirm_password" placeholder="ยืนยันรหัสผ่าน" required>
    <button class="btn border-0 toggle-password" type="button" data-target="confirm_password">
      <i class="bi bi-eye-slash"></i>
    </button>
  </div>
</div>
    `;
  }

  if (role === "club") {
    dynamicFields.innerHTML = `
<div class="row g-3 p-3 border rounded bg-white shadow-sm">

      <div class="col-md-6">
        <label class="form-label fw-semibold text-primary">
          <i class="bi bi-person-vcard me-1"></i> เลือกนักศึกษา
        </label>

      <div class="position-relative">
        <select class="shadow-sm modern-select" id="uid" required>
          <option value="">-- เลือกนักศึกษา --</option>
        </select>
      </div>
    </div>

     <div class="col-md-4">
  <label class="form-label fw-semibold text-primary">
    <i class="bi bi-award me-1"></i> ตำแหน่ง
  </label>

  <div class="position-relative">
    <input type="text"
      class="form-control modern-input shadow-sm"
      id="position"
      placeholder="เช่น ประธาน / รองประธาน"
      required>
    <i class="bi bi-pencil-square input-icon"></i>
  </div>
</div>
</div>
  `;

    fetch("/admin/get-users/student")
      .then((res) => res.json())
      .then((data) => {
        const select = document.getElementById("uid");

        data.forEach((u) => {
          select.innerHTML += `
          <option value="${u.student_id}">
            ${u.student_id} - ${u.first_name}
          </option>`;
        });

        $("#uid").select2({
          placeholder: "ค้นหานักศึกษา",
          width: "100%",
        });
      });
  }
});

document.getElementById("userForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const role = document.getElementById("role").value;
  const password = document.getElementById("password")?.value;
  const confirmPassword = document.getElementById("confirm_password")?.value;

  // ===== STUDENT =====
  if (role === "student") {
    if (!password || !confirmPassword) {
      alert("กรุณากรอกรหัสผ่านให้ครบ");
      return;
    }

    if (password !== confirmPassword) {
      alert("รหัสผ่านไม่ตรงกัน");
      return;
    }

    const baseData = {
      student_id: document.getElementById("uid").value,
      first_name: document.getElementById("name").value,
      faculty: document.getElementById("faculty")?.value,
      major: document.getElementById("major")?.value,
      year: document.getElementById("year")?.value,
      email: document.getElementById("email")?.value,
      phone: document.getElementById("phone")?.value,
      password: password,
    };

    fetch("/admin/create-student", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(baseData),
    })
      .then((res) => res.json())
      .then((data) => {
        alert(data.message || data.error);
        this.reset();
        dynamicFields.innerHTML = "";
        loadUsers(currentFilter);
      });

    return;
  }

  // ===== OFFICER =====
  if (role === "officer") {
    if (!password || !confirmPassword) {
      alert("กรุณากรอกรหัสผ่านให้ครบ");
      return;
    }

    if (password !== confirmPassword) {
      alert("รหัสผ่านไม่ตรงกัน");
      return;
    }

    fetch("/admin/create-officer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        officer_id: document.getElementById("officer_id").value,
        full_name: document.getElementById("full_name").value,
        department: document.getElementById("department").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        password: password,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        alert(data.message || data.error);
        this.reset();
        dynamicFields.innerHTML = "";
        loadUsers(currentFilter);
      });

    return;
  }

  // ===== CLUB =====
  if (role === "club") {
    const studentId = document.getElementById("uid").value;
    const position = document.getElementById("position").value;

    if (!studentId) {
      alert("กรุณาเลือกนักศึกษา");
      return;
    }

    // เพิ่มตำแหน่งให้นศ มี ตำแหน่งเป็นของสโมสรนศ
    fetch("/clubs/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: studentId,
        position: position,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        alert(data.message || data.error);
        this.reset();
        dynamicFields.innerHTML = "";
        loadUsers("club");
      });

    return;
  }
});

function openEditModal(user) {
  // ===== OFFICER =====
  if (user.officer_id) {
    document.getElementById("edit_officer_id").value = user.officer_id;

    document.getElementById("edit_officer_name").value = user.full_name || "";

    document.getElementById("edit_officer_department").value =
      user.department || "";

    document.getElementById("edit_officer_email").value = user.email || "";

    document.getElementById("edit_officer_phone").value = user.phone || "";

    new bootstrap.Modal(document.getElementById("editOfficerModal")).show();

    return;
  }

  // ===== STUDENT / CLUB =====

  const studentId =
    user.student_id ||
    user.id ||
    (user.student ? user.student.student_id : "") ||
    "";

  document.getElementById("edit_student_id").value = studentId;

  document.getElementById("edit_student_code").value = user.student_id || "";

  document.getElementById("edit_name").value = user.first_name
    ? user.first_name + " " + (user.last_name || "")
    : user.full_name || user.name || "";

  document.getElementById("edit_faculty").value = user.faculty || "";
  document.getElementById("edit_major").value = user.major || "";
  document.getElementById("edit_year").value = user.year || "";
  document.getElementById("edit_email").value = user.email || "";
  document.getElementById("edit_phone").value = user.phone || "";

  // ===== CLUB POSITION =====
  if (currentFilter === "club") {
    document.getElementById("edit_position_wrapper").style.display = "block";
    document.getElementById("edit_position").value = user.position || "";
  } else {
    document.getElementById("edit_position_wrapper").style.display = "none";
  }

  new bootstrap.Modal(document.getElementById("editModal")).show();
}

function updateUser() {
  // ===== OFFICER =====
  if (currentFilter === "officer") {
    const officerId = document.getElementById("edit_officer_id").value;

    fetch(`/admin/update-officer/${officerId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        full_name: document.getElementById("edit_officer_name").value,
        department: document.getElementById("edit_officer_department").value,
        email: document.getElementById("edit_officer_email").value,
        phone: document.getElementById("edit_officer_phone").value,
      }),
    })
      .then((res) => res.json())
      .then((result) => {
        alert(result.message || result.error);

        bootstrap.Modal.getInstance(
          document.getElementById("editOfficerModal"),
        ).hide();

        loadUsers("officer");
      });

    return;
  }

  // ===== STUDENT =====
  const studentId = document.getElementById("edit_student_id").value;

  fetch(`/admin/update-user/${studentId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: document.getElementById("edit_name").value,
      faculty: document.getElementById("edit_faculty").value,
      major: document.getElementById("edit_major").value,
      year: document.getElementById("edit_year").value,
      email: document.getElementById("edit_email").value,
      phone: document.getElementById("edit_phone").value,
    }),
  })
    .then((res) => res.json())
    .then((result) => {
      alert(result.message || result.error);

      bootstrap.Modal.getInstance(document.getElementById("editModal")).hide();

      loadUsers(currentFilter);
    });
}

function removeFromClub(studentId) {
  if (!confirm("ต้องการนำออกจากสโมสรนักศึกษาใช่หรือไม่?")) return;

  fetch(`/clubs/remove/${studentId}`, {
    method: "DELETE",
  })
    .then((res) => res.json())
    .then((data) => {
      alert(data.message || data.error);
      loadUsers("club");
    });
}

// ลบนักศึกษาออกจากระบบ (รวมการลบจากสโมสรด้วย)
function deleteUser(studentId) {
  if (!confirm("ต้องการลบนักศึกษาคนนี้ใช่หรือไม่?")) return;

  fetch(`/admin/delete-user/${studentId}`, {
    method: "DELETE",
  })
    .then((res) => res.json())
    .then((data) => {
      alert(data.message || data.error);

      loadUsers(currentFilter);
    })
    .catch((err) => console.error(err));
}

// แก้ไขข้อมูลเจ้าหน้าที่
function updateOfficer() {
  const id = document.getElementById("edit_officer_id").value;

  fetch(`/admin/update-officer/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      full_name: document.getElementById("edit_officer_name").value,
      department: document.getElementById("edit_officer_department").value,
      email: document.getElementById("edit_officer_email").value,
      phone: document.getElementById("edit_officer_phone").value,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      alert(data.message || data.error);
      loadUsers("officer");

      bootstrap.Modal.getInstance(
        document.getElementById("editOfficerModal"),
      ).hide();
    });
}

// ลบเจ้าหน้าที่ออกจากระบบ
function deleteOfficer(id) {
  if (!confirm("ต้องการลบเจ้าหน้าที่คนนี้ใช่หรือไม่?")) return;

  fetch(`/admin/delete-officer/${id}`, {
    method: "DELETE",
  })
    .then((res) => res.json())
    .then((data) => {
      alert(data.message || data.error);
      loadUsers("officer");
    });
}

// โหลดข้อมูลตอนเข้าเพจครั้งแรก
document.addEventListener("DOMContentLoaded", function () {
  let savedRole = localStorage.getItem("selectedRole");

  const allowedRoles = ["student", "club", "officer"];

  if (!allowedRoles.includes(savedRole)) {
    savedRole = "student";
    localStorage.setItem("selectedRole", "student");
  }

  const buttons = document.querySelectorAll(".role-btn");

  buttons.forEach((btn) => {
    if (btn.getAttribute("onclick").includes(savedRole)) {
      btn.classList.add("active");
      loadUsers(savedRole, btn);
    }
  });
});

// ตาเปิดปิด ตั้งค่ารหัสผ่าน
document.addEventListener("click", function (e) {
  const btn = e.target.closest(".toggle-password");
  if (!btn) return;

  const targetId = btn.dataset.target;
  const input = document.getElementById(targetId);
  const icon = btn.querySelector("i");

  if (input.type === "password") {
    input.type = "text";
    icon.classList.remove("bi-eye-slash");
    icon.classList.add("bi-eye");
  } else {
    input.type = "password";
    icon.classList.remove("bi-eye");
    icon.classList.add("bi-eye-slash");
  }
});
