import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import _isEqual from 'lodash/isEqual';

const PieChart = ({ data }) => {
  const chartRef = useRef(null);
  const prevDataRef = useRef(null);

  useEffect(() => {
    if (chartRef && chartRef.current && data) {
      const chartWidth = window.innerWidth * 0.5; // Set width as 50% of the screen width
      const chartHeight = window.innerHeight * 0.5; // Set height as 50% of the screen height

    
      const myPieChart = new Chart(chartRef.current, {
        type: 'pie',
        data: {
          labels: data.labels,
          datasets: [{
            label: 'Disk Usage',
            data: data.values,
            backgroundColor: [
              'rgba(255, 99, 132, 0.5)',
              'rgba(54, 162, 235, 0.5)',
              'rgba(255, 206, 86, 0.5)',
              'rgba(75, 192, 192, 0.5)',
              'rgba(153, 102, 255, 0.5)',
              'rgba(255, 159, 64, 0.5)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          animation: {
            // Disable all animations
            duration: 0
        },
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Disk Usage'
            }
          },
          layout: {
            padding: {
              left: 10,
              right: 10,
              top: 10,
              bottom: 10
            }
          },
          aspectRatio: chartWidth / chartHeight
        }
      });


      return () => {
        myPieChart.destroy(); // Clean up chart instance when component unmounts
      };
    }
  }, [data]);

  return (
    <div>
      <canvas ref={chartRef} />
    </div>
  );
};

export default PieChart;
