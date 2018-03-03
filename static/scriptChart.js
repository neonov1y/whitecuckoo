var canvas = document.getElementById("canvasChart").getContext('2d');

var chartConfig = {
    type: 'pie',
    data: {
        labels: ["Network", "Registry actions", "Files actions", "Processes"],
        datasets: [{
            label: 'Data in white-list',
            data: [connections_number, registry_actions_number, file_actions_number, process_number],
            backgroundColor: [
                'rgba(255, 99, 131, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(75, 192, 192, 0.8)'
            ],
            borderColor: [
                'white',
                'white',
                'white',
                'white'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        legend: {
            position: 'top'
        },
        title: {
            display: true,
            text: 'White list data chart'
        },
        animation: {
            animateScale: true,
            animateRotate: true
        }
    }
}
/*
// Bar Chart
var chartData = {
    type: 'bar',
    data: {
        labels: ["Network", "Registry", "Files", "Processes"],
        datasets: [{
            label: 'Data in white-list',
            data: [connections_number, registry_actions_number, file_actions_number, process_number],
            backgroundColor: [
                'rgba(230, 239, 194, 0.7)',
                'rgba(240, 226, 194, 0.7)',
                'rgba(208, 240, 194, 0.7)',
                'rgba(240, 203, 194, 0.7)'
            ],
            borderColor: [
                'rgba(230, 239, 194, 1)',
                'rgba(240, 226, 194, 1)',
                'rgba(208, 240, 194, 1)',
                'rgba(240, 203, 194, 1)'
            ],
            borderWidth: 2
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
}
*/
var chartObject = new Chart(canvas, chartConfig);
