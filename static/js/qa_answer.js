function addView(code) {
    fetch(`/qa/questions/${code}/view`, {
        method: "POST",
    })
        .then((res) => res.json())
        .then((data) => {
            console.log("view:", data.view_count);
        });
}

function toggleFaq(el, code) {
    const card = el.closest(".faq-card");
    if (!card) return;

    const answer = card.querySelector(".answer-box");
    if (!answer) return;

    const icon = el.querySelector(".toggle-icon");
    const isOpening = !answer.classList.contains("active");

    if (isOpening) {
        // เปิด
        answer.classList.add("active");

        if (icon) {
            icon.classList.remove("bi-chevron-down");
            icon.classList.add("bi-chevron-up");
        }

        // view
        if (!card.dataset.viewed) {
            addView(code);
            card.dataset.viewed = "true";
        }

    } else {
        // ปิดเฉพาะอันนี้
        answer.classList.remove("active");

        if (icon) {
            icon.classList.remove("bi-chevron-up");
            icon.classList.add("bi-chevron-down");
        }
    }
}

// เปิด/ปิด form ตอบ
function toggleAnswerForm(code) {
    const form = document.getElementById("form-" + code);

    if (!form) {
        console.warn("ไม่พบ form:", code);
        return;
    }

    form.classList.toggle("active");
}

// เปิด/ปิดการ์ด (answer)
function openAnswer(code) {
    const card = document.getElementById("form-" + code)?.closest(".faq-card");
    if (!card) return;

    const answerBox = card.querySelector(".answer-box");
    const isOpen = answerBox.classList.contains("active");

    // ปิดทุกอันก่อน
    document.querySelectorAll(".answer-box").forEach(a => a.classList.remove("active"));
    document.querySelectorAll(".answer-form").forEach(f => {
        f.classList.remove("active");
        f.style.display = "none";
    });

    // toggle การ์ด
    if (!isOpen) {
        answerBox.classList.add("active");

        // view
        if (!card.dataset.viewed) {
            addView(code);
            card.dataset.viewed = "true";
        }
    }
}


// ปุ่ม "ตอบ"
function toggleAnswerForm(code) {
    const form = document.getElementById("form-" + code);
    const card = form?.closest(".faq-card");
    if (!form || !card) return;

    const answerBox = card.querySelector(".answer-box");

    // ถ้าการ์ดยังไม่เปิด → เปิดก่อน
    if (!answerBox.classList.contains("active")) {
        openAnswer(code);
    }

    // toggle form
    const isOpen = form.classList.contains("active");

    if (isOpen) {
        form.classList.remove("active");
        form.style.display = "none";
    } else {
        form.style.display = "block";
        setTimeout(() => {
            form.classList.add("active");
        }, 10);
    }
}

function editAnswer(code) {
    const form = document.getElementById("form-" + code);
    const card = form?.closest(".faq-card");
    if (!form || !card) return;

    const answerBox = card.querySelector(".answer-box");
    const answerTextEl = card.querySelector(".answer-text");

    // เปิดการ์ดก่อน (ถ้ายังไม่เปิด)
    if (!answerBox.classList.contains("active")) {
        answerBox.classList.add("active");
    }

    // เอาคำตอบเดิมใส่ textarea
    const textarea = form.querySelector("textarea");
    if (answerTextEl && textarea) {
        textarea.value = answerTextEl.innerText.trim();
    }

    // เปิด form
    form.style.display = "block";
    setTimeout(() => {
        form.classList.add("active");
        textarea.focus(); // โฟกัสเลย
    }, 10);
}

// จำตำแหน่ง scroll ก่อนออก
window.addEventListener("beforeunload", function () {
    localStorage.setItem("scrollY", window.scrollY);
});

window.addEventListener("load", function () {
    const scrollY = localStorage.getItem("scrollY");
    if (scrollY !== null) {
        window.scrollTo(0, parseInt(scrollY));
    }
});

document.getElementById("searchInput").addEventListener("keyup", function () {
    const keyword = this.value.toLowerCase();

    const cards = document.querySelectorAll(".faq-card");
    const noResult = document.getElementById("noResult");

    let found = false;

    cards.forEach(card => {
        const q = card.dataset.question;
        const a = card.dataset.answer;

        if (q.includes(keyword) || a.includes(keyword)) {
            card.style.display = "";
            found = true;
        } else {
            card.style.display = "none";
        }
    });

    noResult.style.display = found ? "none" : "block";
});