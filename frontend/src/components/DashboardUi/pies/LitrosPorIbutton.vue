<template>
  <div class="w-full p-4 bg-white rounded-lg shadow space-y-2">
    <p class="text-xs font-semibold text-gray-600">Litros por iButton</p>

    <div class="w-full h-60 sm:h-72 md:h-80 lg:h-96 relative">
      <canvas ref="canvas" class="w-full h-full"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps, nextTick } from "vue";
import { Chart, BarController, BarElement, LinearScale, CategoryScale, Tooltip, Legend } from "chart.js";

Chart.register(BarController, BarElement, LinearScale, CategoryScale, Tooltip, Legend);

const props = defineProps({
  datos: { type: Array, default: () => [] }
});

const canvas = ref(null);
let chart = null;

function render() {
  if (!canvas.value) return;
  if (chart) { chart.destroy(); chart = null; }

  const totals = {};

  props.datos.forEach(d => {
    if (!d.ibutton) return;
    const litros = Number(d.litros) || 0;
    totals[d.ibutton] = (totals[d.ibutton] || 0) + litros;
  });

  const labels = Object.keys(totals);
  const values = Object.values(totals);

  const ctx = canvas.value.getContext("2d");
  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Litros",
        data: values,
        backgroundColor: "#2563EB"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: "y",
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ({ raw }) => ` ${raw.toFixed(2)} L`
          }
        }
      },
      scales: {
        x: { beginAtZero: true },
        y: { ticks: { autoSkip: false } }
      }
    }
  });
}

onMounted(() => nextTick(render));

watch(() => props.datos, () => nextTick(render), { deep: true });
</script>
