var canvas = document.getElementById("canvasChart").getContext('2d');

var chartConfig = {
    type: 'pie',
    data: {
        labels: ["Network", "Registry actions", "Files actions", "Processes", "DLL's", "Command line"],
        datasets: [{
            label: 'Data in white-list',
            data: [connections_number, registry_actions_number, file_actions_number, process_number, dll_number, command_line_number],
            backgroundColor: [
                'rgba(255, 99, 131, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(21, 137, 255, 0.8)',
                'rgba(55, 55, 55, 0.8)'
            ],
            borderColor: [
                'white',
                'white',
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

var chartObject = new Chart(canvas, chartConfig);
