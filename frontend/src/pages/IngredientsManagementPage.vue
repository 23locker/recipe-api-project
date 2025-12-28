<template>
  <div class="container mx-auto px-4 py-8 max-w-6xl">
    <div class="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <router-link to="/admin" class="text-green-600 hover:text-green-700 font-medium flex items-center gap-1 mb-4 transition-transform hover:-translate-x-1 inline-flex">
          ← В админку
        </router-link>
        <h1 class="text-4xl font-black text-gray-900">Управление ингредиентами</h1>
        <p class="text-gray-500 mt-2">Добавление, изменение и удаление ингредиентов системы</p>
      </div>
      <button 
        @click="openModal()" 
        class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-2xl shadow-lg shadow-green-100 transition-all active:scale-95 flex items-center gap-2"
      >
        <span>➕</span> Добавить ингредиент
      </button>
    </div>

    <!-- Search and Stats -->
    <div class="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 mb-8 flex flex-col md:flex-row gap-6 items-center">
      <div class="relative flex-grow w-full">
        <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Поиск по названию..." 
          class="w-full pl-12 pr-4 py-3 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500 rounded-2xl transition-all"
        />
      </div>
      <div class="flex gap-4 w-full md:w-auto">
        <div class="bg-blue-50 px-6 py-3 rounded-2xl border border-blue-100 flex-grow md:flex-grow-0 text-center">
          <div class="text-[10px] text-blue-500 font-black uppercase tracking-wider mb-0.5">Всего</div>
          <div class="text-xl font-black text-blue-900">{{ filteredIngredients.length }}</div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead class="bg-gray-50 border-b border-gray-100">
            <tr>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Название</th>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Ккал/100г</th>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Б/Ж/У</th>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest text-right">Действия</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="ing in filteredIngredients" :key="ing.id" class="hover:bg-gray-50/50 transition-colors group">
              <td class="px-6 py-5">
                <div class="font-bold text-gray-900">{{ ing.name }}</div>
                <div class="text-[10px] text-gray-400 mt-0.5">ID: {{ ing.id }}</div>
              </td>
              <td class="px-6 py-5">
                <span class="font-mono text-gray-600 bg-gray-100 px-2 py-1 rounded-lg text-sm">{{ ing.calories_per_100g }}</span>
              </td>
              <td class="px-6 py-5">
                <div class="flex items-center gap-2 font-mono text-sm">
                  <span class="text-blue-600 font-bold" title="Белки">{{ ing.protein_per_100g }}</span>
                  <span class="text-gray-300">/</span>
                  <span class="text-purple-600 font-bold" title="Жиры">{{ ing.fat_per_100g }}</span>
                  <span class="text-gray-300">/</span>
                  <span class="text-orange-600 font-bold" title="Углеводы">{{ ing.carbs_per_100g }}</span>
                </div>
              </td>
              <td class="px-6 py-5 text-right">
                <div class="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button 
                    @click="openModal(ing)"
                    class="p-2 bg-indigo-50 text-indigo-600 rounded-xl hover:bg-indigo-600 hover:text-white transition-all active:scale-90"
                    title="Редактировать"
                  >
                    ✏️
                  </button>
                  <button 
                    @click="confirmDelete(ing)"
                    class="p-2 bg-red-50 text-red-600 rounded-xl hover:bg-red-600 hover:text-white transition-all active:scale-90"
                    title="Удалить"
                  >
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="filteredIngredients.length === 0" class="py-20 text-center">
        <div class="text-6xl mb-4">🍃</div>
        <p class="text-gray-400">Ингредиенты не найдены</p>
      </div>
    </div>

    <!-- Edit/Add Modal -->
    <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="closeModal"></div>
      <div class="bg-white rounded-[2rem] w-full max-w-xl relative shadow-2xl animate-modal-in overflow-hidden">
        <div class="p-8">
          <h2 class="text-3xl font-black text-gray-900 mb-8">
            {{ isEditing ? 'Изменить ингредиент' : 'Новый ингредиент' }}
          </h2>
          
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <div>
              <label class="block text-sm font-black text-gray-400 uppercase tracking-widest mb-2">Название</label>
              <input 
                v-model="formData.name" 
                type="text" 
                required
                class="w-full px-5 py-4 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500 rounded-2xl transition-all font-bold"
              />
            </div>

            <div>
              <label class="block text-sm font-black text-gray-400 uppercase tracking-widest mb-2">Ккал/100г</label>
              <input v-model.number="formData.calories_per_100g" type="number" step="0.1" required class="w-full px-5 py-4 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500 rounded-2xl transition-all font-mono font-bold" />
            </div>

            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="block text-xs font-black text-blue-500 uppercase tracking-widest mb-2">Белки</label>
                <input v-model.number="formData.protein_per_100g" type="number" step="0.1" required class="w-full px-4 py-4 bg-blue-50/50 border-transparent focus:bg-white focus:ring-2 focus:ring-blue-500 rounded-2xl transition-all font-mono font-bold" />
              </div>
              <div>
                <label class="block text-xs font-black text-purple-500 uppercase tracking-widest mb-2">Жиры</label>
                <input v-model.number="formData.fat_per_100g" type="number" step="0.1" required class="w-full px-4 py-4 bg-purple-50/50 border-transparent focus:bg-white focus:ring-2 focus:ring-purple-500 rounded-2xl transition-all font-mono font-bold" />
              </div>
              <div>
                <label class="block text-xs font-black text-orange-500 uppercase tracking-widest mb-2">Углеводы</label>
                <input v-model.number="formData.carbs_per_100g" type="number" step="0.1" required class="w-full px-4 py-4 bg-orange-50/50 border-transparent focus:bg-white focus:ring-2 focus:ring-orange-500 rounded-2xl transition-all font-mono font-bold" />
              </div>
            </div>

            <div class="flex gap-4 pt-4">
              <button 
                type="submit" 
                :disabled="isSubmitting"
                class="flex-grow bg-green-600 hover:bg-green-700 text-white font-black py-5 px-8 rounded-2xl transition-all shadow-xl shadow-green-100 active:scale-95 disabled:opacity-50"
              >
                {{ isSubmitting ? 'Сохранение...' : (isEditing ? 'Сохранить изменения' : 'Создать ингредиент') }}
              </button>
              <button 
                type="button" 
                @click="closeModal" 
                class="px-8 bg-gray-100 hover:bg-gray-200 text-gray-500 font-bold rounded-2xl transition-all"
              >
                Отмена
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRecipesStore } from '@/stores/recipesStore';

const store = useRecipesStore();
const searchQuery = ref('');
const showModal = ref(false);
const isEditing = ref(false);
const isSubmitting = ref(false);
const editingId = ref(null);

const formData = ref({
  name: '',
  calories_per_100g: 0,
  protein_per_100g: 0,
  fat_per_100g: 0,
  carbs_per_100g: 0
});

const filteredIngredients = computed(() => {
  if (!searchQuery.value) return store.ingredients;
  const q = searchQuery.value.toLowerCase();
  return store.ingredients.filter(i => i.name.toLowerCase().includes(q));
});

const getCategoryName = (id) => {
  // Categories are for recipes, not ingredients
  return 'N/A';
};

const openModal = (ing = null) => {
  if (ing) {
    isEditing.value = true;
    editingId.value = ing.id;
    formData.value = { ...ing };
  } else {
    isEditing.value = false;
    editingId.value = null;
    formData.value = {
      name: '',
      calories_per_100g: 0,
      protein_per_100g: 0,
      fat_per_100g: 0,
      carbs_per_100g: 0
    };
  }
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const handleSubmit = async () => {
  isSubmitting.value = true;
  try {
    if (isEditing.value) {
      await store.updateIngredient(editingId.value, formData.value);
    } else {
      await store.createIngredient(formData.value);
    }
    closeModal();
  } catch (err) {
    alert(err.response?.data?.detail || 'Ошибка при сохранении');
  } finally {
    isSubmitting.value = false;
  }
};

const confirmDelete = async (ing) => {
  if (confirm(`Вы уверены, что хотите удалить ингредиент "${ing.name}"?`)) {
    try {
      await store.deleteIngredient(ing.id);
    } catch (err) {
      alert(err.response?.data?.detail || 'Ошибка при удалении');
    }
  }
};

onMounted(() => {
  store.fetchIngredients();
});
</script>

<style scoped>
@keyframes modal-in {
  from { opacity: 0; transform: scale(0.95) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-modal-in {
  animation: modal-in 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
</style>
