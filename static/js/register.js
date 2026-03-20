document.addEventListener("DOMContentLoaded", function () {
    // ----------------------
    // ELEMENTS
    // ----------------------
    const form = document.getElementById("registerForm");
    const roleSelect = document.getElementById("role");

    const studentForm = document.getElementById("studentForm");
    const clubForm = document.getElementById("clubForm");
    const staffForm = document.getElementById("staffForm");

    const msg = document.getElementById("msg");

    const inputs = {
        name: document.getElementById("name"),
        email: document.getElementById("email"),
        username: document.getElementById("username"),
        phone: document.getElementById("phone"),
        password: document.getElementById("password"),
        confirmPassword: document.getElementById("confirmPassword"),
    };

    // ----------------------
    // CHANGE ROLE
    // ----------------------
    function changeRole() {
        const role = roleSelect?.value;

        [studentForm, clubForm, staffForm].forEach((form) => {
            if (form) form.style.display = "none";
        });

        if (role === "student" && studentForm) {
            studentForm.style.display = "block";
        } else if (role === "club" && clubForm) {
            clubForm.style.display = "block";
        } else if (role === "staff" && staffForm) {
            staffForm.style.display = "block";
        }
    }

    roleSelect?.addEventListener("change", changeRole);

    // ----------------------
    // VALIDATION
    // ----------------------
    function validateForm() {
        for (let key in inputs) {
            if (inputs[key] && !inputs[key].value.trim()) {
                showMessage("กรุณากรอกข้อมูลให้ครบถ้วน", "danger");
                return false;
            }
        }

        if (inputs.password.value !== inputs.confirmPassword.value) {
            showMessage("รหัสผ่านไม่ตรงกัน", "warning");
            return false;
        }

        return true;
    }

    // ----------------------
    // SUBMIT
    // ----------------------
    form?.addEventListener("submit", function (e) {
        e.preventDefault();
        msg.innerHTML = "";

        if (!validateForm()) return;

        let status =
            roleSelect?.value === "student"
                ? "ใช้งานได้ทันที"
                : "รอการอนุมัติจากเจ้าหน้าที่";

        showMessage(`สมัครสมาชิกสำเร็จ (${status})`, "success");

        // form.submit(); // ใช้ตอนต่อ Backend
    });

    // ----------------------
    // MESSAGE FUNCTION
    // ----------------------
    function showMessage(text, type) {
        msg.innerHTML = `
      <div class="alert alert-${type} mt-3">
        ${text}
      </div>
    `;
        msg.scrollIntoView({ behavior: "smooth" });
    }
});

// ----------------------
// TOGGLE PASSWORD (ต้องอยู่นอก DOMContentLoaded)
// ----------------------
function togglePassword(fieldId, icon) {
    const input = document.getElementById(fieldId);

    if (!input) return;

    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("bi-eye-slash");
        icon.classList.add("bi-eye");
    } else {
        input.type = "password";
        icon.classList.remove("bi-eye");
        icon.classList.add("bi-eye-slash");
    }
}