const weekDays = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'];
const moneyCollectionsData = [100000, 150000, 200000, 180000, 250000, 300000, 220000];

const ctx = document.getElementById('weeklyCollections').getContext('2d');

const moneyCollectionsChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: weekDays,
    datasets: [{
      label: 'Collections',
      borderColor: 'rgb(75, 192, 192)',
      borderWidth: 2,
      fill: false,
      data: moneyCollectionsData,
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});


const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const moneyCollectionsData = [1000000, 1200000, 800000, 1500000, 2000000, 1800000, 2200000, 2500000, 2800000, 3000000, 2600000, 2300000];

const ctx = document.getElementById('monthlyCollections').getContext('2d');

const moneyCollectionsChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: months,
    datasets: [{
      label: 'Money Collections',
      borderColor: 'rgb(75, 192, 192)',
      borderWidth: 2,
      fill: false,
      data: moneyCollectionsData,
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});


const years = ['2018', '2019', '2020', '2021', '2022', '2023']; // Add more years as needed
const moneyCollectionsData = [5000000, 6000000, 8000000, 10000000, 12000000, 15000000]; // Corresponding data for each year

const ctx = document.getElementById('yearlyCollections').getContext('2d');

const moneyCollectionsChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: years,
    datasets: [{
      label: 'Money Collections',
      borderColor: 'rgb(75, 192, 192)',
      borderWidth: 2,
      fill: false,
      data: moneyCollectionsData,
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});