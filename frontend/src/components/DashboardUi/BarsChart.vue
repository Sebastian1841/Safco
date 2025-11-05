<template>
  <div class="w-full p-4 bg-white rounded-lg shadow space-y-4">
    <canvas ref="chartCanvas"></canvas>

    <div class="flex gap-2">
      <button v-if="chartInstance" @click="chartInstance.resetZoom()"
        class="px-3 py-1 bg-blue-600 text-white rounded text-xs shadow hover:bg-blue-700">
        Reiniciar Zoom
      </button>

      <button @click="toggleZoom" class="px-3 py-1 rounded text-xs shadow" :class="zoomEnabled
        ? 'bg-red-600 text-white hover:bg-red-700'
        : 'bg-gray-300 text-gray-900 hover:bg-gray-400'">
        {{ zoomEnabled ? 'Desactivar Zoom' : 'Activar Zoom' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, defineProps } from 'vue';
import axios from 'axios';
import zoomPlugin from 'chartjs-plugin-zoom';

import {
  Chart,
  BarController,
  BarElement,
  TimeScale,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
} from 'chart.js';

import 'chartjs-adapter-date-fns';
import es from 'date-fns/locale/es'; // ✅ FIX IMPORTACIÓN

Chart.register(
  BarController,
  BarElement,
  TimeScale,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
  zoomPlugin
);

const props = defineProps({
  fechaInicio: String,
  fechaFin: String,
  selectedDevices: Array,
  selectedRange: String
});

const BACKEND_URL = "http://localhost:5000";

const chartCanvas = ref(null);
let chartInstance = null;
const rawDatos = ref([]);
const zoomEnabled = ref(false);

const generateMockData = () => {
  const data = [];
  const devices = ['A101', 'B202', 'C303'];
  const now = new Date();
  for (let i = 0; i < 50; i++) {
    const date = new Date(now.getTime() - (i * 3600000 * 2));
    data.push({
      fecha: date.toISOString(),
      dispositivo_id: devices[i % devices.length],
      litros: (Math.random() * 5 + 1).toFixed(2),
      ibutton: i % 10 === 0 ? `iBtn-${i}` : null,
      dato1_nombre: i % 5 === 0 ? 'Sensor Temp' : null,
      dato2_nombre: i % 7 === 0 ? 'Sensor Pres' : null,
    });
  }
  return data;
};

async function fetchDatos() {
  try {
    const r = await axios.get(`${BACKEND_URL}/datos`);
    rawDatos.value = Array.isArray(r.data) ? r.data : [];
  } catch (error) {
    console.error("Error fetching data, using mock data:", error.message);
    rawDatos.value = generateMockData();
  }
}

function initChart() {

  // ✅ EVITA el error de "el is null"
  if (!chartCanvas.value) return;

  if (chartInstance) {
    try {
      chartInstance.destroy();
    } catch (e) {
      // ya estaba destruido, continuar
    }
    chartInstance = null;
  }


  let data = [...rawDatos.value];

  if (props.selectedDevices?.length) {
    data = data.filter(d => props.selectedDevices.includes(d.dispositivo_id));
  }

  const now = new Date();

  if (props.selectedRange === "last_hour") {
    data = data.filter(d => new Date(d.fecha) >= new Date(now.getTime() - 1 * 60 * 60 * 1000));
  }
  else if (props.selectedRange === "last_12_hours") {
    data = data.filter(d => new Date(d.fecha) >= new Date(now.getTime() - 12 * 60 * 60 * 1000));
  }
  else if (props.selectedRange === "last_week") {
    data = data.filter(d => new Date(d.fecha) >= new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000));
  }
  else if (props.selectedRange === "last_month") {
    data = data.filter(d => new Date(d.fecha) >= new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000));
  }
  else if (props.fechaInicio && props.fechaFin) {
    const ini = new Date(`${props.fechaInicio}T00:00:00`);
    const fin = new Date(`${props.fechaFin}T23:59:59`);
    data = data.filter(d => new Date(d.fecha) >= ini && new Date(d.fecha) <= fin);
  }
  else {
    data = data.filter(d => new Date(d.fecha) >= new Date(now.getTime() - 24 * 60 * 60 * 1000));
  }

  data.sort((a, b) => new Date(a.fecha) - new Date(b.fecha));

  if (!data.length) {
    const ctx = chartCanvas.value.getContext("2d");
    chartInstance = new Chart(ctx, {
      type: "bar",
      data: { datasets: [] },
      options: {
        plugins: { legend: { display: false }, tooltip: { enabled: false } },
        scales: { x: { display: false }, y: { display: false } }
      }
    });
    return;
  }

  const devicesToShow = props.selectedDevices.length ?
    props.selectedDevices :
    [...new Set(data.map(d => d.dispositivo_id))];

  const first = new Date(data[0].fecha);
  const last = new Date(data[data.length - 1].fecha);
  const diffHours = (last - first) / 3600000;
  const timeUnit = diffHours < 48 ? "hour" : "day";

  const datasets = devicesToShow.map((dev, i) => ({
    label: `Dispositivo ${dev}`,
    backgroundColor: ['#1E3A8A', '#065F46', '#B91C1C', '#92400E', '#312E81'][i % 5],
    borderRadius: 3,
    maxBarThickness: 6,
    barPercentage: 0.6,
    categoryPercentage: 0.8,
    data: data.filter(d => d.dispositivo_id === dev).map(d => ({
      x: new Date(d.fecha),
      y: Number(d.litros) || 0,
      ibutton: d.ibutton,
      dato1: d.dato1_nombre,
      dato2: d.dato2_nombre
    }))
  }));

  const ctx = chartCanvas.value.getContext("2d");

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: { datasets },
    options: {
      responsive: true,
      aspectRatio: 2.2,
      parsing: false,
      plugins: {
        legend: { display: true, position: "bottom" },
        tooltip: {
          backgroundColor: "#111827e6",
          displayColors: false,
          callbacks: {
            title: ([p]) => new Date(p.raw.x).toLocaleString("es-CL", {
              year: 'numeric',
              month: 'numeric',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit',
            }),
            label: ({ raw }) => {
              const l = [`Litros: ${raw.y} L`];
              if (raw.ibutton) l.push(`iButton: ${raw.ibutton}`);
              if (raw.dato1) l.push(`Dato 1: ${raw.dato1}`);
              if (raw.dato2) l.push(`Dato 2: ${raw.dato2}`);
              return l;
            }
          }
        },
        zoom: {
          zoom: { enabled: zoomEnabled.value, wheel: { enabled: zoomEnabled.value }, mode: "x" },
          pan: { enabled: zoomEnabled.value, mode: "x" }
        }
      },
      scales: {
        x: {
          type: "time",
          adapters: { date: { locale: es } },
          time: {
            unit: timeUnit,
            displayFormats: { hour: "HH:mm", day: "dd/MM" }
          },
          min: first.getTime() - (timeUnit === 'hour' ? 3600000 : 86400000),
          max: last.getTime() + (timeUnit === 'hour' ? 3600000 : 86400000),
          ticks: { autoSkip: true, maxTicksLimit: 10 }
        },
        y: {
          beginAtZero: true,
          title: { text: "Litros", display: true }
        }
      }
    }
  });
}

function toggleZoom() {
  zoomEnabled.value = !zoomEnabled.value;
  if (chartInstance) {
    chartInstance.options.plugins.zoom.zoom.enabled = zoomEnabled.value;
    chartInstance.options.plugins.zoom.zoom.wheel.enabled = zoomEnabled.value;
    chartInstance.options.plugins.zoom.pan.enabled = zoomEnabled.value;
    chartInstance.update('none'); // ✅ evita render extra
  }
}

onMounted(async () => {
  await fetchDatos();
  await nextTick();     // ✅ asegura que el canvas existe
  initChart();
});

// ✅ Watch corregido para evitar ejecutar si canvas no existe
watch(
  () => [props.fechaInicio, props.fechaFin, props.selectedDevices, props.selectedRange],
  async () => {
    await nextTick();
    if (chartCanvas.value) initChart();
  },
  { deep: true }
);
</script>
