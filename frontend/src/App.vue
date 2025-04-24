<template>
  <div id="app">
    <h1>Weather Summary</h1>
    
    <label for="zip-code">Zip code</label>
    <input v-model="zipCode" type="text" id="zip-code" />

    <label for="country-code">Country code</label>
    <input v-model="countryCode" type="text" id="country-code" />
    
    <button @click="getSummary">Get Weather Data</button>

    <!-- Display the message below the button -->
    <div v-if="message" class="alert">{{ message }}</div>

    <HistoryData />
    <HbCheck />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HbCheck from './components/HearbeatCheck.vue'
import HistoryData from './components/HistoryData.vue'

const summary = ref(null)

// Refs for zip and country code inputs
const zipCode = ref('')
const countryCode = ref('')

// Ref for the alert message
const message = ref('')

const getSummary = async () => {
  // Construct the query string with zip and country code
  const url = `http://localhost/api/summary?zip_code=${zipCode.value}&country_code=${countryCode.value}`;
  
  try {
    const res = await fetch(url);
    summary.value = await res.json();
    
    // Show the message and remove it after 2 seconds
    message.value = "The table will update automatically!";
    setTimeout(() => {
      message.value = '';
    }, 2000);

  } catch (error) {
    console.error('Error fetching data:', error);
    message.value = "Error fetching data!";
    setTimeout(() => {
      message.value = '';
    }, 2000);
  }
}
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}

button {
  margin: 10px;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
}

div {
  margin-top: 20px;
}

.alert {
  margin-top: 10px;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border-radius: 5px;
}
</style>
