$(function() {
    $(".datepicker").datepicker({
        dateFormat: "yy-mm-dd",
        showAnim: "slideDown"
    });
});

let chartInstance = null;

// Function to fetch data from the backend and update the chart
function fetchDataAndUpdateChart(startDate, endDate) {
    $.ajax({
        url: 'fetch_statistics.php', // PHP endpoint that returns the statistics
        type: 'POST',
        data: {
            startDate: startDate,
            endDate: endDate
        },
        dataType: 'json',
        success: function(response) {
            // Extract labels (week date ranges) and data for requests and offers
            const requestLabels = response.requests.map(item => `${item.weekStart} - ${item.weekEnd}`);
            const offerLabels = response.offers.map(item => `${item.weekStart} - ${item.weekEnd}`);
            const labels = requestLabels.length > offerLabels.length ? requestLabels : offerLabels;

            const newRequests = response.requests.map(item => item.newRequests);
            const completedRequests = response.requests.map(item => item.completedRequests);
            const newOffers = response.offers.map(item => item.newOffers);
            const completedOffers = response.offers.map(item => item.completedOffers);

            // Define the data for the chart
            const data = {
                labels: labels, // Weeks will be shown on the x-axis with date ranges
                datasets: [
                    {
                        label: 'Νέα αιτήματα',
                        data: newRequests,
                        borderColor: '#FA4343',
                        backgroundColor: '#FA4343',
                        fill: false
                    },
                    {
                        label: 'Ολοκληρωμένα αιτήματα',
                        data: completedRequests,
                        borderColor: '#4BC0C0',
                        backgroundColor: '#4BC0C0',
                        fill: false
                    },
                    {
                        label: 'Νέες προσφορές',
                        data: newOffers,
                        borderColor: '#36A2EB',
                        backgroundColor: '#36A2EB',
                        fill: false
                    },
                    {
                        label: 'Ολοκληρωμένες προσφορές',
                        data: completedOffers,
                        borderColor: '#FFCE56',
                        backgroundColor: '#FFCE56',
                        fill: false
                    }
                ]
            };

            // Update the chart or create a new one if it doesn't exist
            const chartContainer = document.getElementById('chartContainer');
            chartContainer.style.display = 'block'; // Show the chart container

            if (chartInstance) {
                chartInstance.destroy();  // Destroy the old chart instance if it exists
            }

            const ctx = document.getElementById('lineChart').getContext('2d');
            chartInstance = new Chart(ctx, {
                type: 'line',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                        },
                    },
                    hover: {
                        mode: 'nearest',
                        intersect: true
                    },
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Weeks (Start - End Dates)'
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Count'
                            }
                        }
                    }
                }
            });
        },
        error: function(xhr, status, error) {
            console.error('Error fetching data: ', error);
        }
    });
}

// Event listener for the "Calculate" button to fetch data and update the chart
document.getElementById('showChartButton').addEventListener('click', function() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    // Fetch data based on selected date range
    if (!startDate || !endDate) {
        fetchDataAndUpdateChart('', '');  // Fetch all data if no dates are selected
    } else {
        fetchDataAndUpdateChart(startDate, endDate);  // Fetch data for the selected date range
    }
});
