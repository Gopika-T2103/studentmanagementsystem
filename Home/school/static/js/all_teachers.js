function openEditModal( tname,tid,temail,tdept,tassign) {
    document.getElementById("editModal").style.display = "block";

    // Fill form fields
    document.getElementById("edit_name").value = tname;
    document.getElementById("edit_id").value = tid;

    document.getElementById("edit_email").value = temail;
    document.getElementById("edit_dept").value = tdept;
    document.getElementById("edit_assign").value =tassign;

    // Update form action
    document.getElementById("editTeacherForm").action = "/update_teacher/" + id + "/";
}

function closeModal() {
    document.getElementById("editModal").style.display = "none";
}

function deleteRow(element) {
    if (confirm("Are you sure you want to remove this student from the list? This will NOT delete from database.")) {
        // Remove the entire row
        element.closest("tr").remove();
    }
}


