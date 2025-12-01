let dropdowns = document.querySelectorAll(".dropdown-btn");

dropdowns.forEach(dropdown => {
    dropdown.addEventListener("click", function () {

        // the dropdown menu right after the clicked button
        let submenu = this.nextElementSibling;

        // arrow inside clicked dropdown
        let arrow = this.querySelector(".arrow");

        // toggle dropdown menu
        submenu.style.display = submenu.style.display === "block" ? "none" : "block";

        // rotate arrow
        arrow.classList.toggle("rotate");
    });
});



// --------------------------ADDING NEW TEACHER---------------------------//

const tableSection=document.getElementById("teacherTableSection");
const addSection=document.getElementById("addTeacherSection");

const addTeacherMenu = document.getElementById("menuAddTeacher");
if (addTeacherMenu) {
    addTeacherMenu.onclick = () => {
        tableSection.style.display = "none";
        addSection.style.display = "block";
    };
}


const menuEditTeacher = document.getElementById("menuEditTeacher");
if (menuEditTeacher) {
    menuEditTeacher.onclick = () => {
        addSection.style.display = "none";
        tableSection.style.display = "none";
    };
}



const openAddTeacherForm = document.getElementById("openAddTeacherForm");
if (openAddTeacherForm) {
    openAddTeacherForm.onclick = () => {
        tableSection.style.display = "none";
        addSection.style.display = "block";
    };
}


// document.getElementById("menuAddTeacher").onclick = () =>{
//     tableSection.style.display="none";
//     addSection.style.display="block";
// };

// document.getElementById("menuEditTeacher").onclick =() =>{
//     addSection.style.display="none";
//     tableSection.style.display="none";
// };

// document.getElementById("openAddTeacherForm").onclick = () => {
//     tableSection.style.display = "none";
//     addSection.style.display = "block";
// };


// ADD TEACHER FUNCTION
document.getElementById("addTeacherForm").onsubmit = function() {
   return true;
};




// --------------------------Edit PopUp------------------------------//


    document.addEventListener("DOMContentLoaded", function() {

    // OPEN EDIT POPUP
    document.querySelectorAll(".edit-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            const modal = document.getElementById("editmodal");
            modal.style.display = "block";

            document.getElementById("edit_name").value = this.dataset.name ;
            document.getElementById("edit_id").value = this.dataset.id;
            document.getElementById("edit_email").value = this.dataset.email;
            document.getElementById("edit_dept").value = this.dataset.dept;
            document.getElementById("edit_assign").value = this.dataset.assign;

            // set form action to update url (use id from data-id)
            document.getElementById("editTeacherForm").action = 
            `/update_teacher/${this.dataset.id}/`;
        });
    });

    // CLOSE POPUP
    // const closeBtn = document.getElementById("closeedit");
    // if (closeBtn) {
    //     closeBtn.onclick = () => {
    //         const modal = document.getElementById("editmodal");
    //         if (modal) modal.style.display = "none";
    //     };
    // }

    document.getElementById("closeedit").onclick = function () {
        document.getElementById("editmodal").style.display = "none";
    }


    // Close when clicking outside modal content
    window.onclick = function(e)  {
        const modal = document.getElementById("editmodal");
        if (e.target === modal) {
            modal.style.display = "none";
        }
    };

    // DELETE: add confirm to any .delete-link (we will create delete links in the template)
    document.querySelectorAll(".delete-link").forEach(link => {
        link.addEventListener("click", function(e) {
            if (!confirm("Are you sure you want to delete this teacher?")) {
                e.preventDefault();
            }
        });
    });

});


