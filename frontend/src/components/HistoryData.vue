<template>
    <div>
      <h1>Weather History</h1>
      <table border="1">
        <thead>
          <tr>
            <th>Zip Code</th>
            <th>Country Code</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Avg Sunshine [sec]</th>
            <th>Avg Rain [mm]</th>
            <th>Needs light</th>
            <th>Needs water</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in history" :key="entry.timestamp">
            <td>{{ entry.zip_code }}</td>
            <td>{{ entry.country_code }}</td>
            <td>{{ entry.lat }}</td>
            <td>{{ entry.lon }}</td>
            <td>{{ entry.start_date }}</td>
            <td>{{ entry.end_date }}</td>
            <td>{{ entry.avg_sunshine }}</td>
            <td>{{ entry.avg_rain }}</td>
            <td>{{ entry.needs_light }}</td>
            <td>{{ entry.needs_water }}</td>
            <td>{{ entry.timestamp }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        history: [] // Initially an empty array
      };
    },
    mounted() {
      // Fetch data when the component is mounted
      this.fetchHistoryData();
      this.fetchInterval = setInterval(this.fetchHistoryData, 3000);
    },
    beforeDestroy() {
      // Clear the interval when the component is destroyed
      clearInterval(this.fetchInterval);
    },
    methods: {
      async fetchHistoryData() {
        try {
          const response = await axios.get('http://localhost/api/history');
          this.history = response.data.history;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    padding: 8px;
    text-align: left;
  }
  
  th {
    background-color: #f2f2f2;
  }
  </style>
  