document.addEventListener("DOMContentLoaded", () => {
    // จำตำแหน่ง scroll
    const scrollPos = sessionStorage.getItem("scrollPos");

    if (scrollPos !== null) {
        window.scrollTo(0, parseInt(scrollPos));
    }

    window.addEventListener("beforeunload", () => {
        sessionStorage.setItem("scrollPos", window.scrollY);
    });

    // SEARCH ROOM / EQUIPMENT
    const searchInput = document.getElementById("searchInput");

    const cards = document.querySelectorAll(
        "#placeContainer .card, #equipmentContainer .card",
    );

    const noResult = document.createElement("div");

    noResult.innerHTML = `
        <div class="text-center text-muted mt-4" id="noResult">
            <i class="bi bi-search"></i><br>
            ไม่พบข้อมูล
        </div>
    `;

    const main = document.querySelector("main");

    searchInput.addEventListener("input", () => {
        const keyword = searchInput.value.toLowerCase().trim();

        let found = 0;

        cards.forEach((card) => {
            const name = card.querySelector("h5").innerText.toLowerCase();

            if (name.includes(keyword)) {
                card.style.display = "";
                found++;
            } else {
                card.style.display = "none";
            }
        });

        const exist = document.getElementById("noResult");

        if (found === 0) {
            if (!exist) {
                main.appendChild(noResult);
            }
        } else {
            if (exist) {
                exist.remove();
            }
        }
    });

    // ตรวจ total / available
    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", (e) => {
            const total = form.querySelector("[name='total_quantity']");
            const available = form.querySelector("[name='available_quantity']");

            if (total && available) {
                if (parseInt(available.value) > parseInt(total.value)) {
                    alert("จำนวนที่ว่างต้องไม่มากกว่าจำนวนทั้งหมด");

                    e.preventDefault();
                }
            }
        });
    });

    // quipment quantity control
    document.querySelectorAll(".equipment-row").forEach((row) => {
        const checkbox = row.querySelector(".equipment-check");
        const qtyInput = row.querySelector(".qty-input");
        const badge = row.querySelector(".stock-badge");

        const used = parseInt(qtyInput.value) || 0;
        const originalStock = parseInt(badge.dataset.stock) + used;

        checkbox.addEventListener("change", () => {
            if (!checkbox.checked) {
                qtyInput.value = 0;
                badge.textContent = "เหลือ " + originalStock;
            }
        });

        qtyInput.addEventListener("input", () => {
            let qty = parseInt(qtyInput.value) || 0;

            if (qty > 0) {
                checkbox.checked = true;
            }

            let remain = originalStock - qty;

            if (remain < 0) {
                remain = 0;
                qtyInput.value = originalStock;
            }

            badge.textContent = "เหลือ " + remain;
        });
    });
});