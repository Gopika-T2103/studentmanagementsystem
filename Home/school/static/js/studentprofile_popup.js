let popup = document.getElementById("popup");
let closeBtn = document.querySelector(".close");

document.querySelectorAll(".open-popup").forEach(item => {
    item.addEventListener("click", function () {

        let id = this.dataset.stid;

        document.getElementById("pname").textContent = this.dataset.name;
        document.getElementById("pclass").textContent = this.dataset.class;
        document.getElementById("pteacher").textContent = this.dataset.teacher;

        document.getElementById("pguardian").textContent = this.dataset.guardian;
        document.getElementById("pphone").textContent = this.dataset.phone;
        document.getElementById("paddress").textContent = this.dataset.address;

        document.getElementById("attLink").href = `/student/${id}/attendance/`;
        document.getElementById("markLink").href = `/student/${id}/marks/`;

        popup.style.display = "block";
    });
});

closeBtn.addEventListener("click", () => popup.style.display = "none");
window.addEventListener("click", e => {
    if (e.target == popup) popup.style.display = "none";
});
