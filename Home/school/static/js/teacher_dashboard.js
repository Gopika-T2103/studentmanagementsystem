// Sidebar toggle for mobile
function toggleSidebar(){
  document.querySelector(".sidebar_teacher").classList.toggle("active");
}

// Dropdown controls
document.querySelectorAll(".dropdown-btn").forEach(btn => {
  btn.addEventListener("click", function(){
    const next = this.nextElementSibling;
    const arrow = this.querySelector(".arrow");
    if(!next) return;
    if(next.style.display === "flex"){
      next.style.display = "none";
      arrow.classList.remove("rotate");
    } else {
      next.style.display = "flex";
      arrow.classList.add("rotate");
    }
  });
});

// ACTION placeholders (replace with real routes)

function viewAttendance(){ alert("Open Attendance / Mark Attendance"); }

function viewTimetable(){ alert("Open Timetable view"); }

function viewHours(){ alert("Open Teaching Hours"); }

function applyLeave(){ alert("Apply for Leave - open form"); }

function viewProfile(){ alert("Open Profile / Edit Profile"); }

function logout(){ alert("Logging out... (wire this to your logout view)"); }


// PIE CHART 

document.addEventListener("DOMContentLoaded", function(){
  const ctx = document.getElementById('resultPieChart').getContext('2d');

  // Read JSON safely from the hidden script tags
  const resultData = JSON.parse(document.getElementById('result-data').textContent);
  const labels = JSON.parse(document.getElementById('result-labels').textContent);

  const myChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: resultData,
        backgroundColor: [
          '#2f80ed', '#f44336', '#22c55e',
          '#f59e0b', '#9b59b6', '#fa07ad', '#e3f70a'
        ],
        borderColor: '#fff',
        borderWidth: 2
      }]
    },
    plugins: [ChartDataLabels],
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right' },
        datalabels: {
          color: '#000',
          formatter: function(value, ctx) {
            const total = ctx.chart.data.datasets[0].data.reduce((a,b)=>a+b,0);
            if (total === 0) return '0%';
            return ((value / total) * 100).toFixed(1) + '%';
          },
          font: { size: 12, weight: '600' }
        }
      }
    }
  });
});



//--------------------------------------------- edit popup-------------------------------------//
function openEditModal(id, roll, name, math, bio, phy, chem, mal, eng, hin) {
    const modal = document.getElementById('editModal');
    if (!modal) {
        console.error('editModal element not found');
        return;
    }

    // Fill the form
    document.getElementById('editStudentId').value = id;
    document.getElementById('editRoll').value = roll;
    document.getElementById('editName').value = name;
    document.getElementById('editMath').value = math;
    document.getElementById('editBio').value = bio;
    document.getElementById('editPhy').value = phy;
    document.getElementById('editChem').value = chem;
    document.getElementById('editMal').value = mal;
    document.getElementById('editEng').value = eng;
    document.getElementById('editHin').value = hin;

    // Show popup
    modal.style.display = "flex";
}

function closeEditModal() {
    const modal = document.getElementById('editModal');
    if (!modal) return;
    modal.style.display = "none";
}
