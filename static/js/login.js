function login() {
  const identifier = document
    .querySelector("input[name='identifier']")
    .value.trim();
  const password = document
    .querySelector("input[name='password']")
    .value.trim();
  const msg = document.getElementById("msg");

  // เคลียร์ข้อความก่อน
  msg.innerHTML = "";

  // ✅ เช็คว่ากรอกครบไหม
  if (!identifier || !password) {
    msg.innerHTML =
      '<div class="alert alert-danger">กรุณากรอกข้อมูลให้ครบถ้วน</div>';
    return;
  }

  // จำลองฐานข้อมูล
  const users = [
    { id: "68123456", password: "123456", role: "student" },
    { id: "club@ubu.ac.th", password: "123456", role: "club" },
    { id: "admin@ubu.ac.th", password: "123456", role: "staff" },
  ];

  const foundUser = users.find(
    (user) => user.id === identifier && user.password === password,
  );

  if (foundUser) {
    msg.innerHTML =
      '<div class="alert alert-success text-center">เข้าสู่ระบบสำเร็จ!</div>';

    //setTimeout(() => {
    //window.location.href = "/dashboard";
    //}, 1000);
  } else {
    msg.innerHTML =
      '<div class="alert alert-danger text-center">ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง!</div>';
  }
}

function togglePassword(fieldId, icon) {
  const input = document.getElementById(fieldId);

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
