<template>
    <div style="padding: 20px; max-width: 500px; margin: 40px auto; background: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
      <h2 style="font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 20px;">Service Status Monitor</h2>
      <div
        v-for="service in services"
        :key="service.name"
        style="display: flex; justify-content: space-between; align-items: center; padding: 10px; border: 1px solid #ccc; border-radius: 6px; margin-bottom: 10px;"
      >
        <span style="font-weight: 500;">{{ service.label }}</span>
        <span :style="statusStyle(service.status)">
          {{ statusText(service.status) }}
        </span>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue'
  import axios from 'axios'
  
  const services = ref([
    {
      name: 'frontend_api',
      label: 'Frontend API',
      url: 'http://localhost:8080/api/heartbeat',
      status: 'unknown',
    },
    {
      name: 'analytics_processor',
      label: 'Analytics Processor',
      url: 'http://localhost:8080/analytics/heartbeat',
      status: 'unknown',
    },
    {
      name: 'weather_fetcher',
      label: 'Weather Fetcher',
      url: 'http://localhost:8080/weather/heartbeat',
      status: 'unknown',
    }
  ])
  
  const statusText = (status) => {
    if (status === 'ok') return '🟢 Online'
    if (status === 'error') return '🔴 Offline'
    return '🟡 Checking...'
  }
  
  const statusStyle = (status) => {
    if (status === 'ok') return { color: 'green', fontWeight: 'bold' }
    if (status === 'error') return { color: 'red', fontWeight: 'bold' }
    return { color: 'orange', fontWeight: 'bold' }
  }
  
  let intervalId = null
  
  const checkServices = async () => {
    for (const service of services.value) {
      try {
        const res = await axios.get(service.url)
        service.status = res.status === 200 ? 'ok' : 'error'
      } catch {
        service.status = 'error'
      }
    }
  }
  
  onMounted(() => {
    checkServices()
    intervalId = setInterval(checkServices, 5000)
  })
  
  onUnmounted(() => {
    clearInterval(intervalId)
  })
  </script>
  