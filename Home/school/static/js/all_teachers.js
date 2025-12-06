
function closePopup() {
    document.getElementById("editPopup").style.display = "none";
}

// EDIT BUTTON CLICK
document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", function () {

        document.getElementById("edit_id").value = this.dataset.id;
        document.getElementById("edit_name").value = this.dataset.name;
        document.getElementById("edit_tid").value = this.dataset.tid;
        document.getElementById("edit_email").value = this.dataset.email;
        document.getElementById("edit_dept").value = this.dataset.dept;
        document.getElementById("edit_assign").value = this.dataset.assign;
        document.getElementById("edit_status").value = this.dataset.status;

        document.getElementById("editPopup").style.display = "block";
    });
});

// DELETE BUTTON CLICK — updates status only
document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", function () {
        const teacherId = this.dataset.id;

        if (confirm("Are you sure you want to mark this teacher as Resigned?")) {
            window.location.href = `/resign_teacher/${teacherId}/`;
        }
    });
});

