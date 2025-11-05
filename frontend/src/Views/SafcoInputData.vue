<template>
  <div class="p-4 sm:p-6 bg-gray-50 min-h-screen font-sans">

    <div v-if="editingItem" class="fixed inset-0 bg-gray-600 bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-2xl w-full max-w-lg p-6">
        <h2 class="text-xl font-bold mb-4 text-blue-700">
          Editar: {{ editingItem.type === 'litros' ? 'Control de Consumo' : `Dato ${editingItem.type.slice(-1)}` }}
        </h2>
        <form @submit.prevent="saveEdit">
          <div v-if="editingItem.type === 'dato1' || editingItem.type === 'dato2'">
            <label for="edit-nombre" class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
            <input type="text" id="edit-nombre" v-model="editingItem.item.nombre" required
              class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <div v-if="editingItem.type === 'litros'">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
              <div>
                <label for="edit-date" class="block text-sm font-medium text-gray-700 mb-1">Fecha de
                  Control</label>
                <input type="date" id="edit-date" v-model="editingItem.item.fecha" required
                  class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
              <div>
                <label for="edit-device" class="block text-sm font-medium text-gray-700 mb-1">Dispositivo</label>
                <select id="edit-device" v-model="editingItem.item.dispositivo" required
                  class="w-full border border-gray-300 rounded-md p-2 text-sm bg-white focus:ring-blue-500 focus:border-blue-500">
                  <option v-for="device in dispositivos" :key="device.id" :value="device.id">
                    {{ getOptionLabel(device) }}
                  </option>
                </select>
              </div>
            </div>

            <div class="flex gap-4 mb-4">
              <div class="flex-1">
                <label for="edit-litros-inicio" class="block text-sm font-medium text-gray-700 mb-1">Litros
                  Iniciales</label>
                <input type="number" id="edit-litros-inicio" v-model.number="editingItem.item.litros_inicio" required
                  step="0.01" min="0"
                  class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
              <div class="flex-1">
                <label for="edit-litros-final" class="block text-sm font-medium text-gray-700 mb-1">Litros
                  Finales</label>
                <input type="number" id="edit-litros-final" v-model.number="editingItem.item.litros_final" required
                  step="0.01" :min="0"
                  class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>
            </div>
            <div class="text-xs font-semibold p-2 rounded-md bg-red-100 text-red-800">
              Recuerde: El valor final debe ser menor o igual al valor inicial.
            </div>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <button type="button" @click="cancelEdit"
              class="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition duration-150 text-sm">
              Cancelar
            </button>
            <button type="submit"
              class="px-4 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition duration-150 shadow-md text-sm">
              Guardar Cambios
            </button>
          </div>
        </form>
      </div>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <div class="bg-white p-4 sm:p-6 rounded-lg shadow-xl border border-gray-200">
        <h2 class="text-xl font-semibold text-blue-700 mb-4 flex items-center gap-2">
          Añadir Referencia: Dato 1
        </h2>
        <form @submit.prevent="addDato1" class="flex flex-col sm:flex-row gap-4 mb-4">
          <input type="text" v-model="newDato1Item" required
            class="flex-1 border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500"
            placeholder="Ej: Cliente D, Turno Mañana..." />
          <button type="submit"
            class="sm:w-auto px-4 py-2 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 transition duration-150 shadow-md text-sm">
            Agregar
          </button>
        </form>
        <h3 class="text-sm font-bold text-gray-700 mt-6 mb-2 border-t pt-4">
          Datos Agregados: ({{ dato1Data.length }})
        </h3>
        <div class="max-h-40 overflow-y-auto border border-gray-100 rounded-md p-2 bg-gray-50">
          <ul v-if="dato1Data.length" class="space-y-1">
            <li v-for="item in dato1Data" :key="item.id"
              class="flex justify-between items-center bg-white p-2 rounded-md shadow-sm text-sm border border-gray-100">
              <span class="text-gray-800 font-medium">{{ item.nombre }}</span>
              <div class="flex items-center gap-2">
                <span class="text-xs text-gray-500 font-mono hidden sm:inline">ID: {{ item.id }}</span>
                <button @click="startEdit('dato1', item)"
                  class="p-1 text-blue-600 hover:text-blue-800 transition duration-150 rounded-full hover:bg-blue-50"
                  title="Editar Dato 1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                </button>
                <button @click="deleteDato1(item.id)"
                  class="p-1 text-red-600 hover:text-red-800 transition duration-150 rounded-full hover:bg-red-50"
                  title="Eliminar Dato 1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-500 italic p-2 text-center">
            Aún no se han agregado referencias.
          </p>
        </div>
      </div>

      <div class="bg-white p-4 sm:p-6 rounded-lg shadow-xl border border-gray-200">
        <h2 class="text-xl font-semibold text-blue-700 mb-4 flex items-center gap-2">
          Añadir Referencia: Dato 2
        </h2>
        <form @submit.prevent="addDato2" class="flex flex-col sm:flex-row gap-4 mb-4">
          <input type="text" v-model="newDato2Item" required
            class="flex-1 border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500"
            placeholder="Ej: Proyecto Alfa, Turno Noche..." />
          <button type="submit"
            class="sm:w-auto px-4 py-2 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 transition duration-150 shadow-md text-sm">
            Agregar
          </button>
        </form>
        <h3 class="text-sm font-bold text-gray-700 mt-6 mb-2 border-t pt-4">
          Datos Agregados: ({{ dato2Data.length }})
        </h3>
        <div class="max-h-40 overflow-y-auto border border-gray-100 rounded-md p-2 bg-gray-50">
          <ul v-if="dato2Data.length" class="space-y-1">
            <li v-for="item in dato2Data" :key="item.id"
              class="flex justify-between items-center bg-white p-2 rounded-md shadow-sm text-sm border border-gray-100">
              <span class="text-gray-800 font-medium">{{ item.nombre }}</span>
              <div class="flex items-center gap-2">
                <span class="text-xs text-gray-500 font-mono hidden sm:inline">ID: {{ item.id }}</span>
                <button @click="startEdit('dato2', item)"
                  class="p-1 text-blue-600 hover:text-blue-800 transition duration-150 rounded-full hover:bg-blue-50"
                  title="Editar Dato 2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                </button>
                <button @click="deleteDato2(item.id)"
                  class="p-1 text-red-600 hover:text-red-800 transition duration-150 rounded-full hover:bg-red-50"
                  title="Eliminar Dato 2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-500 italic p-2 text-center">
            Aún no se han agregado referencias.
          </p>
        </div>
      </div>
    </div>

    <div class="bg-white p-4 sm:p-6 rounded-lg shadow-xl border border-gray-200">
      <h2 class="text-xl font-semibold text-blue-700 mb-4 flex items-center gap-2">
        Registro Manual de Consumo por Litros
      </h2>

      <form @submit.prevent="addLitrosControl" class="flex flex-col gap-4 mb-4">

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label for="control-date" class="block text-xs font-medium text-gray-700 mb-1">Fecha de
              Control</label>
            <input type="date" id="control-date" v-model="newLitrosControl.fecha" required
              class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <div>
            <label for="control-device"
              class="block text-xs font-medium text-gray-700 mb-1">Dispositivo/Vehículo</label>
            <select id="control-device" v-model="newLitrosControl.dispositivo" required
              class="w-full border border-gray-300 rounded-md p-2 text-sm bg-white focus:ring-blue-500 focus:border-blue-500">
              <option value="" disabled>
                <span v-if="loadingDevices">Cargando Dispositivos...</span>
                <span v-else-if="dispositivos.length === 0">No se encontraron dispositivos</span>
                <span v-else>Seleccione un Dispositivo</span>
              </option>
              <option v-for="device in dispositivos" :key="device.id" :value="device.id" :disabled="loadingDevices">
                {{ getOptionLabel(device) }}
              </option>
            </select>
          </div>
        </div>

        <div class="flex gap-4">
          <div class="flex-1">
            <label for="litros-inicio" class="block text-xs font-medium text-gray-700 mb-1">Litros Iniciales
            </label>
            <input type="number" id="litros-inicio" v-model.number="newLitrosControl.litros_inicio" required step="0.01"
              min="0"
              class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="0.00" />
          </div>
          <div class="flex-1">
            <label for="litros-final" class="block text-xs font-medium text-gray-700 mb-1">Litros Finales
            </label>
            <input type="number" id="litros-final" v-model.number="newLitrosControl.litros_final" required step="0.01"
              :min="0"
              class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="0.00" />
          </div>
        </div>

        <div class="text-sm font-semibold p-2 rounded-md bg-red-100 text-red-800">
          ATENCIÓN: Para registrar el consumo, el valor final debe ser menor o igual al valor inicial.
        </div>

        <button type="submit" :disabled="loadingDevices || dispositivos.length === 0"
          class="sm:w-full px-4 py-2 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 transition duration-150 shadow-md text-sm disabled:bg-gray-400">
          Registrar Consumo Manual
        </button>
      </form>

      <h3 class="text-sm font-bold text-gray-700 mt-6 mb-2 border-t pt-4">
        Controles de Consumo Registrados ({{ litrosControlData.length }})
      </h3>
      <div class="max-h-60 overflow-y-auto border border-gray-100 rounded-md p-2 bg-gray-50">
        <ul v-if="litrosControlData.length" class="space-y-1">
          <li v-for="item in litrosControlData" :key="item.id"
            class="flex flex-wrap justify-between items-center bg-white p-2 rounded-md shadow-sm text-sm border border-gray-100">

            <div class="flex flex-col sm:flex-row sm:items-center justify-between w-full">
              <span class="text-gray-800 font-bold">
                <span class="text-red-600">CONSUMO</span>: {{ getOptionLabelById(item.dispositivo) }}
              </span>

              <div class="flex items-center gap-2 mt-1 sm:mt-0">
                <span class="text-xs text-gray-500 font-semibold">{{ item.fecha }}</span>
                <button @click="startEdit('litros', item)"
                  class="p-1 text-blue-600 hover:text-blue-800 transition duration-150 rounded-full hover:bg-blue-50"
                  title="Editar Control">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                </button>
                <button @click="deleteLitrosControl(item.id)"
                  class="p-1 text-red-600 hover:text-red-800 transition duration-150 rounded-full hover:bg-red-50"
                  title="Eliminar Control">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="flex justify-between items-center w-full mt-1">
              <span class="text-xs text-gray-500">
                Inicio: **{{ item.litros_inicio }} L** | Fin: **{{ item.litros_final }} L**
              </span>
              <span class="bg-red-100 text-red-700 px-2 py-0.5 rounded-full font-bold text-xs whitespace-nowrap">
                Consumo: {{ Math.abs(item.diferencia_manual).toFixed(2) }} L
              </span>
            </div>
          </li>
        </ul>
        <p v-else class="text-sm text-gray-500 italic p-2 text-center">
          Aún no se han registrado controles manuales de litros.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const BACKEND_URL = process.env.VUE_APP_BACKEND_URL || 'http://localhost:5000';

export default {
  name: "SafcoInputData",
  setup() {
    // -------------------- Utilidades de Fecha --------------------
    const today = new Date().toISOString().slice(0, 10); // Formato YYYY-MM-DD

    // -------------------- Estados Comunes de Edición --------------------
    // { type: 'dato1' | 'dato2' | 'litros', item: { ... }, originalItem: { ... } }
    const editingItem = ref(null);

    const startEdit = (type, item) => {
      // Clonar el objeto para no modificar el dato original directamente en la UI
      editingItem.value = {
        type: type,
        item: { ...item },
        originalItem: item // Referencia al objeto original en la lista
      };

      if (type === 'litros') {
        // Asegurar que los campos numéricos se manejen como números
        editingItem.value.item.litros_inicio = parseFloat(item.litros_inicio);
        editingItem.value.item.litros_final = parseFloat(item.litros_final);
      }
    };

    const cancelEdit = () => {
      editingItem.value = null;
    };

    const saveEdit = async () => {
      if (!editingItem.value) return;

      const { type, item, originalItem } = editingItem.value;
      let url = '';
      let payload = {};

      try {
        switch (type) {
          case 'dato1': { // <-- Corregido con llaves
            url = `${BACKEND_URL}/dato1/${item.id}`;
            payload = { nombre: item.nombre.trim() };
            break;
          }
          case 'dato2': { // <-- Corregido con llaves
            url = `${BACKEND_URL}/dato2/${item.id}`;
            payload = { nombre: item.nombre.trim() };
            break;
          }
          case 'litros': { // <-- Corregido con llaves
            url = `${BACKEND_URL}/litros_control/${item.id}`;

            if (item.litros_final > item.litros_inicio) {
              console.error("Error: Los litros finales NO pueden ser mayores a los iniciales.");
              return;
            }

            // Declaración léxica dentro de un bloque seguro
            const diferencia_manual = item.litros_final - item.litros_inicio;

            payload = {
              fecha: item.fecha,
              dispositivo: item.dispositivo,
              litros_inicio: item.litros_inicio,
              litros_final: item.litros_final,
              diferencia_manual: diferencia_manual,
            };
            break;
          }
          default:
            return;
        }

        const res = await axios.put(url, payload);

        // Actualizar el objeto original en la lista con los datos devueltos por el servidor
        Object.assign(originalItem, res.data);
        console.log(`✅ Edición de ${type} con ID ${item.id} guardada.`);

        editingItem.value = null; // Cerrar el formulario de edición

      } catch (err) {
        console.error(`❌ Error al guardar edición de ${type}:`, err);
        console.error(`Error al guardar la edición de ${type}.`);
      }
    };


    // -------------------- Dispositivos API --------------------
    const dispositivos = ref([]);
    const loadingDevices = ref(true);

    const fetchDispositivosConDatos = async () => {
      loadingDevices.value = true;
      try {
        const res = await axios.get(`${BACKEND_URL}/dispositivos`);
        dispositivos.value = res.data;
      } catch (err) {
        console.error("❌ Error al cargar dispositivos:", err);
        dispositivos.value = [];
      } finally {
        loadingDevices.value = false;
      }
    };

    // Funciones utilitarias para labels
    const getOptionLabel = (device) => device.nombre;
    const getOptionLabelById = (id) => {
      const device = dispositivos.value.find(d => d.id === id);
      return device ? device.nombre : `Dispositivo ${id}`;
    };

    // -------------------- Dato 1 --------------------
    const newDato1Item = ref('');
    const dato1Data = ref([]);

    const fetchDato1 = async () => {
      try {
        const res = await axios.get(`${BACKEND_URL}/dato1`);
        dato1Data.value = res.data;
      } catch (err) {
        console.error("❌ Error al cargar Dato 1:", err);
      }
    };

    const addDato1 = async () => {
      if (newDato1Item.value.trim() !== '') {
        try {
          const res = await axios.post(`${BACKEND_URL}/dato1`, {
            nombre: newDato1Item.value.trim()
          });
          dato1Data.value.push(res.data);
          newDato1Item.value = '';
        } catch (err) {
          console.error("❌ Error al agregar Dato 1:", err);
          console.error("Error al agregar Dato 1.");
        }
      }
    };

    const deleteDato1 = async (id) => {
      if (confirm('¿Estás seguro de que quieres eliminar esta referencia de Dato 1?')) {
        try {
          await axios.delete(`${BACKEND_URL}/dato1/${id}`);
          dato1Data.value = dato1Data.value.filter(item => item.id !== id);
          console.log(`✅ Referencia Dato 1 con ID ${id} eliminada.`);
        } catch (err) {
          console.error(`❌ Error al eliminar Dato 1 con ID ${id}:`, err);
          console.error("Error al eliminar la referencia de Dato 1.");
        }
      }
    };


    // -------------------- Dato 2 --------------------
    const newDato2Item = ref('');
    const dato2Data = ref([]);

    const fetchDato2 = async () => {
      try {
        const res = await axios.get(`${BACKEND_URL}/dato2`);
        dato2Data.value = res.data;
      } catch (err) {
        console.error("❌ Error al cargar Dato 2:", err);
      }
    };

    const addDato2 = async () => {
      if (newDato2Item.value.trim() !== '') {
        try {
          const res = await axios.post(`${BACKEND_URL}/dato2`, {
            nombre: newDato2Item.value.trim()
          });
          dato2Data.value.push(res.data);
          newDato2Item.value = '';
        } catch (err) {
          console.error("❌ Error al agregar Dato 2:", err);
          console.error("Error al agregar Dato 2.");
        }
      }
    };

    const deleteDato2 = async (id) => {
      if (confirm('¿Estás seguro de que quieres eliminar esta referencia de Dato 2?')) {
        try {
          await axios.delete(`${BACKEND_URL}/dato2/${id}`);
          dato2Data.value = dato2Data.value.filter(item => item.id !== id);
          console.log(`✅ Referencia Dato 2 con ID ${id} eliminada.`);
        } catch (err) {
          console.error(`❌ Error al eliminar Dato 2 con ID ${id}:`, err);
          console.error("Error al eliminar la referencia de Dato 2.");
        }
      }
    };

    // -------------------- Consumo por Litros --------------------

    const newLitrosControl = ref({
      fecha: today,
      dispositivo: '',
      litros_inicio: null,
      litros_final: null
    });

    const litrosControlData = ref([]);

    const fetchLitrosControl = async () => {
      try {
        const res = await axios.get(`${BACKEND_URL}/litros_control`);
        // Ordenar por fecha descendente
        litrosControlData.value = res.data.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
      } catch (err) {
        console.error("❌ Error al cargar Controles de Litros:", err);
      }
    };

    const addLitrosControl = async () => {
      const { litros_inicio, litros_final } = newLitrosControl.value;
      if (litros_final > litros_inicio) {
        console.error("Error: Los litros finales NO pueden ser mayores a los iniciales.");
        return;
      }

      const diferencia_manual = litros_final - litros_inicio;

      try {
        const res = await axios.post(`${BACKEND_URL}/litros_control`, {
          ...newLitrosControl.value,
          diferencia_manual: diferencia_manual,
        });

        litrosControlData.value.unshift(res.data);

        // Reinicialización
        newLitrosControl.value = { fecha: today, dispositivo: '', litros_inicio: null, litros_final: null };

      } catch (err) {
        console.error("❌ Error al registrar Consumo Manual:", err);
        console.error("Error al registrar el consumo manual.");
      }
    };

    const deleteLitrosControl = async (id) => {
      if (confirm('¿Estás seguro de que quieres eliminar este control de consumo?')) {
        try {
          await axios.delete(`${BACKEND_URL}/litros_control/${id}`);
          litrosControlData.value = litrosControlData.value.filter(item => item.id !== id);
          console.log(`✅ Control de Litros con ID ${id} eliminado.`);
        } catch (err) {
          console.error(`❌ Error al eliminar Control de Litros con ID ${id}:`, err);
          console.error("Error al eliminar el control de consumo.");
        }
      }
    };

    // Llamar a todas las funciones de carga de datos en el montaje
    onMounted(() => {
      fetchDispositivosConDatos();
      fetchDato1();
      fetchDato2();
      fetchLitrosControl();
    });

    return {
      dispositivos, loadingDevices, getOptionLabel, getOptionLabelById, today,
      // Edición
      editingItem, startEdit, cancelEdit, saveEdit,
      // Dato 1
      newDato1Item, dato1Data, addDato1, deleteDato1,
      // Dato 2
      newDato2Item, dato2Data, addDato2, deleteDato2,
      // Consumo por Litros
      newLitrosControl, litrosControlData, addLitrosControl, deleteLitrosControl
    };
  }
};
</script>

<style scoped>
/* Estilos opcionales */
</style>
