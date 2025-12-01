// sidebar toggle
function toggleSidebar() {
    const sidebar = document.querySelector(".sidebar_teacher");
    sidebar.classList.toggle("active");
}



// pie chart


document.addEventListener("DOMContentLoaded", function() {

    const ctx = document.getElementById('resultPieChart').getContext('2d');

    const resultData = [5, 27, 3];   // Your class result numbers

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Outstanding', 'Pass', 'Fail'],
            datasets: [{
                data: resultData,
                backgroundColor: ['#4CAF50', '#2196F3', '#F44336'],
                borderWidth: 1
            }]
        },
        plugins: [ChartDataLabels],
        options: {
            responsive: true,
            maintainAspectRatio: false,

            animation: {
                animateRotate: true,   // ROTATION EFFECT
                animateScale: true,    // SCALE EFFECT
                duration: 1500         // TIME OF ANIMATION
            },

            plugins: {
                legend: { position: 'bottom' },
                datalabels: {
                    color: '#fff',
                    formatter: (value, context) => {
                        const total = context.chart.data.datasets[0].data
                            .reduce((a, b) => a + b, 0);
                        return ((value / total) * 100).toFixed(1) + '%';
                    },
                    font: { weight: 'bold', size: 14 }
                }
            }
        }
    });

});
