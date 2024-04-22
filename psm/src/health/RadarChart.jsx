import  { useEffect, useRef } from 'react';

const RadarChart = ({ data2 }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const chartWidth = window.innerWidth * 0.5; // Set width as 50% of the screen width
    const chartHeight = window.innerHeight * 0.5; // Set height as 50% of the screen height

    const data = {
      labels: data2.labels,
      datasets: [
        {
          label: 'Used',
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
          borderWidth: 1,
          pointBackgroundColor: 'rgba(255, 99, 132, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(255, 99, 132, 1)',
          data: data2.values1
        },
        {
          label: 'Free',
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
          borderWidth: 1,
          pointBackgroundColor: 'rgba(255, 99, 132, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(255, 99, 132, 1)',
          data: data2.values2
        }
      ]
    };

    const options = {
      scale: {
        ticks: { beginAtZero: true }
      },
      animation: {
        // Disable all animations
        duration: 0
    }
    };

    const ctx = canvasRef.current.getContext('2d');

    // Destroy existing chart instance if it exists
    if (window.myRadarChart) {
      window.myRadarChart.destroy();
    }

    // Create the radar chart
    window.myRadarChart = new window.Chart(ctx, {
      type: 'radar',
      data: data,
      options: options,
      responsive: true,
      maintainAspectRatio: false,
      aspectRatio: chartWidth / chartHeight
    });

    // Cleanup on component unmount
    return () => {
      if (window.myRadarChart) {
        window.myRadarChart.destroy();
      }
    };
  }, [data2]); // Run only once on component mount

  return <canvas ref={canvasRef} id="radarChart"></canvas>;
};

export default RadarChart;
