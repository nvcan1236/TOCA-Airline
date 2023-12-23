
  const ctx = document.getElementById('myChart');

data = {
  labels: [
    'Tuyến HN - SG',
    'Tuyến SG - DN',
    'Tuyến SG - DL',
      'Tuyến HN - DN'
  ],
  datasets: [{
    label: 'Doanh thu theo tuyến bay trong năm 2023',
    data: [300, 50, 100, 40],
    backgroundColor: [
      'rgb(255, 99, 132)',
      'rgb(54, 162, 235)',
      'rgb(255, 205, 86)',
        'rgb(69,190,112)'
    ],
    hoverOffset: 4
  }]
};

  new Chart(ctx, {
    type: 'pie',
    data: data,
    options: {
        plugins: {
            title: {
                display: true,
              position: 'bottom',
                font: {
                    size: 18,
                },
                text: 'Báo cáo thông kê doanh thu theo tuyến bay trong năm 2023'
            },
          legend: {
              position: 'right',
            align: 'start',
            title: {
                display: true,
                text: 'Chú thích'
            }
          }
        }
    }
  });