function addView(code) {
    fetch(`/qa/questions/${code}/view`, {
        method: "POST",
    });
}

function toggleFaq(el, code) {
    const card = el.closest(".faq-card");
    if (!card) return;

    const answer = card.querySelector(".answer-box");
    if (!answer) {
        console.warn("ไม่พบ .answer-box");
        return;
    }

    const icon = el.querySelector(".toggle-icon");

    const isOpening = !answer.classList.contains("active");

    // toggle ตัวนี้ตัวเดียว
    answer.classList.toggle("active");

    if (icon) {
        icon.classList.toggle("bi-chevron-up");
        icon.classList.toggle("bi-chevron-down");
    }

    if (isOpening && !card.dataset.viewed) {
        addView(code);
        card.dataset.viewed = "true";
    }
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
        const text = card.dataset.question;

        if (text.includes(keyword)) {
            card.style.display = "";
            found = true;
        } else {
            card.style.display = "none";
        }
    });

    if (!found) {
        noResult.style.display = "block";
    } else {
        noResult.style.display = "none";
    }
});