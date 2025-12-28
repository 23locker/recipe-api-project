<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <div class="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <router-link to="/admin" class="text-green-600 hover:text-green-700 font-medium flex items-center gap-1 mb-4 transition-transform hover:-translate-x-1 inline-flex">
          ← В админку
        </router-link>
        <h1 class="text-4xl font-black text-gray-900">Категории</h1>
        <p class="text-gray-500 mt-2">Управление категориями рецептов</p>
      </div>
      <button 
        @click="openModal()" 
        class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-2xl shadow-lg shadow-green-100 transition-all active:scale-95 flex items-center gap-2"
      >
        <span>➕</span> Добавить категорию
      </button>
    </div>

    <div class="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead class="bg-gray-50 border-b border-gray-100">
            <tr>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">ID</th>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Название</th>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest text-right">Действия</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="cat in store.categories" :key="cat.id" class="hover:bg-gray-50/50 transition-colors group">
              <td class="px-6 py-5 font-mono text-sm text-gray-400">{{ cat.id }}</td>
              <td class="px-6 py-5">
                <div class="font-bold text-gray-900 text-lg">{{ cat.name }}</div>
              </td>
              <td class="px-6 py-5 text-right">
                <div class="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button 
                    @click="openModal(cat)"
                    class="p-2 bg-indigo-50 text-indigo-600 rounded-xl hover:bg-indigo-600 hover:text-white transition-all active:scale-90"
                  >
                    ✏️
                  </button>
                  <button 
                    @click="confirmDelete(cat)"
                    class="p-2 bg-red-50 text-red-600 rounded-xl hover:bg-red-600 hover:text-white transition-all active:scale-90"
                  >
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Edit/Add Modal -->
    <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="closeModal"></div>
      <div class="bg-white rounded-[2rem] w-full max-w-md relative shadow-2xl animate-modal-in overflow-hidden">
        <div class="p-8">
          <h2 class="text-3xl font-black text-gray-900 mb-8">
            {{ isEditing ? 'Изменить категорию' : 'Новая категория' }}
          </h2>
          
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <div>
              <label class="block text-sm font-black text-gray-400 uppercase tracking-widest mb-2">Название</label>
              <input 
                v-model="formData.name" 
                type="text" 
                required
                placeholder="Напр. Десерты"
                class="w-full px-5 py-4 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500 rounded-2xl transition-all font-bold text-lg"
              />
            </div>

            <div class="flex gap-4 pt-4">
              <button 
                type="submit" 
                :disabled="isSubmitting"
                class="flex-grow bg-green-600 hover:bg-green-700 text-white font-black py-5 px-8 rounded-2xl transition-all shadow-xl shadow-green-100 active:scale-95 disabled:opacity-50"
              >
                {{ isSubmitting ? 'Сохранение...' : (isEditing ? 'Сохранить изменения' : 'Создать категорию') }}
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
import { ref, onMounted } from 'vue';
import { useRecipesStore } from '@/stores/recipesStore';

const store = useRecipesStore();
const showModal = ref(false);
const isEditing = ref(false);
const isSubmitting = ref(false);
const editingId = ref(null);

const formData = ref({
  name: ''
});

const openModal = (cat = null) => {
  if (cat) {
    isEditing.value = true;
    editingId.value = cat.id;
    formData.value = { ...cat };
  } else {
    isEditing.value = false;
    editingId.value = null;
    formData.value = { name: '' };
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
      await store.updateCategory(editingId.value, formData.value);
    } else {
      await store.createCategory(formData.value);
    }
    closeModal();
  } catch (err) {
    alert(err.response?.data?.detail || 'Ошибка при сохранении');
  } finally {
    isSubmitting.value = false;
  }
};

const confirmDelete = async (cat) => {
  if (confirm(`Вы уверены, что хотите удалить категорию "${cat.name}"?`)) {
    try {
      await store.deleteCategory(cat.id);
    } catch (err) {
      alert(err.response?.data?.detail || 'Ошибка при удалении');
    }
  }
};

onMounted(() => {
  store.fetchCategories();
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
