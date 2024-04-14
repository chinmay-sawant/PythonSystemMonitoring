import  { useEffect } from 'react'
import Chart from 'chart.js/auto';
export const CPURAM = (props) => {
    /*
        function for line graph here
        */
        var myLineChart; // Declare a variable to store the chart instance

         // Function to create/update the line chart
         function createLineChart(cData,cLabels,rData) {
            var ctx = document.getElementById('myLineChart').getContext('2d');
            if (myLineChart) {
                myLineChart.destroy(); // Destroy the existing chart if it exists
            }
            myLineChart  = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: cLabels,
                    datasets: [{
                        label: 'CPU Usage',
                        data: cData,
                        borderColor: 'rgba(255, 99, 132, 1)', // Line color
                        backgroundColor: 'rgba(255, 192, 203, 0.2)', // Background color
                        fill: true,
                        pointRadius: 5, // Point radius
                        pointHoverRadius: 8, // Point radius on hover
                        pointHoverBorderColor: 'rgba(255, 99, 132, 1)', // Point border color on hover
                        pointHoverBorderWidth: 2 // Point border width on hover
                    },{
                        label: 'RAM Usage',
                        data: rData,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        fill: true,
                        pointRadius: 5, // Point radius
                        pointHoverRadius: 8, // Point radius on hover
                        pointHoverBorderColor: 'rgba(255, 99, 132, 1)', // Point border color on hover
                        pointHoverBorderWidth: 2 // Point border width on hover
                    }
                ]
                },
                options: {
                    tooltips: {
                        callbacks: {
                            label: function(tooltipItem, data) {
                                return 'Value: ' + tooltipItem.yLabel;
                            }
                        }
                    }
                }
            });
        }
        // Function to update chart data
        function updateChartData(newData,newLabels) {
            myLineChart.data.datasets[0].data = newData;
            myLineChart.data.labels = newLabels;
            myLineChart.update();
        }

       
    useEffect(() => {
      // Get today's date
      const today = new Date();

      // Get year, month, and day
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are zero-based
      const day = String(today.getDate()).padStart(2, '0');

      // Format the date
      const formattedDate = `${year}-${month}-${day}`;

      const eventSource = new EventSource('http://localhost:8000/stream');

      var cpuLineData = [];
      var ramLineData = [];
      var lineLabels = [];
      var firstTime = true;

      eventSource.onmessage = function(event) {
          const data = JSON.parse(event.data);
          props.updateEventData(data[formattedDate]);
           // console.log(data[formattedDate]["health"]);
          if (cpuLineData.length > 5) {
              cpuLineData.shift();
              ramLineData.shift();
              lineLabels.shift();
          }
          cpuLineData.push(data[formattedDate]["health"]["cpu"]["percent"]);
          ramLineData.push(data[formattedDate]["health"]["ram"]["percent"]);
          lineLabels.push(data[formattedDate]["timestamp"]);
          if (firstTime === true) {
              createLineChart(cpuLineData, lineLabels, ramLineData);
          } else {
              updateChartData(cpuLineData, lineLabels, ramLineData);
          }
          firstTime = false;
      };

      eventSource.onerror = function(error) {
          console.error('EventSource error:', error);
      };

      return () => {
          eventSource.close(); // Close the event source when component unmounts
      };
  }, []); // Empty dependency array ensures this effect runs only once on mount

  return (
    <>
    <div>
    <canvas id="myLineChart"></canvas>
    </div>
    
  </>
  )
}
