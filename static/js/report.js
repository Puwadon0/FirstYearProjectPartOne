document.addEventListener("DOMContentLoaded", function () {
  const flashStatus = document.getElementById("flash-status");

  if (flashStatus && flashStatus.dataset.status === "upload_success") {
    const successModal = new bootstrap.Modal(
      document.getElementById("successModal"),
    );

    successModal.show();

    const confirmBtn = document.querySelector("#successModal .btn-success");

    confirmBtn.addEventListener("click", function () {
      successModal.hide();

      const reportSection = document.querySelector(".container.mb-5");

      if (reportSection) {
        reportSection.scrollIntoView({ behavior: "smooth" });
      }
    });
  }
});

const deleteModal = document.getElementById("deleteModal");

deleteModal.addEventListener("show.bs.modal", function (event) {
  const button = event.relatedTarget;
  const reportId = button.getAttribute("data-id");

  const form = document.getElementById("deleteForm");

  // route delete Report
  form.action = `/reports/delete/${reportId}`;
});
