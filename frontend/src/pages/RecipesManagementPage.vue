<template>
  <div class="container mx-auto px-4 py-8 max-w-6xl">
    <div class="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <router-link to="/admin" class="text-green-600 hover:text-green-700 font-medium flex items-center gap-1 mb-4 transition-transform hover:-translate-x-1 inline-flex">
          ← В админку
        </router-link>
        <h1 class="text-4xl font-black text-gray-900">Управление рецептами</h1>
        <p class="text-gray-500 mt-2">Создание и редактирование рецептов системы</p>
      </div>
      <router-link 
        to="/admin/recipes/new" 
        class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-2xl shadow-lg shadow-green-100 transition-all active:scale-95 flex items-center gap-2"
      >
        <span>➕</span> Создать рецепт
      </router-link>
    </div>

    <!-- Search -->
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
    </div>

    <!-- Grid -->
    <div v-if="filteredRecipes.length === 0" class="py-20 text-center bg-gray-50 rounded-3xl border-2 border-dashed border-gray-200">
      <div class="text-6xl mb-4">🍳</div>
      <p class="text-gray-400">Рецепты не найдены</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="recipe in filteredRecipes" 
        :key="recipe.id" 
        class="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden flex flex-col group hover:shadow-xl transition-all duration-300"
      >
        <div class="h-32 bg-gradient-to-br from-green-50 to-emerald-50 flex items-center justify-center text-4xl group-hover:scale-110 transition-transform">
          🥘
        </div>
        <div class="p-6 flex-grow">
          <div class="flex justify-between items-start mb-2">
            <h3 class="font-bold text-gray-900 text-lg line-clamp-1">{{ recipe.name }}</h3>
          </div>
          <div class="flex gap-2 mb-4">
            <span class="text-[10px] font-black uppercase tracking-widest text-gray-400 bg-gray-50 px-2 py-1 rounded">
              {{ getCategoryName(recipe.category_id) }}
            </span>
            <span class="text-[10px] font-black uppercase tracking-widest text-indigo-500 bg-indigo-50 px-2 py-1 rounded">
              {{ recipe.cook_time_minutes }} мин
            </span>
          </div>
          <div class="flex justify-between items-center pt-4 border-t border-gray-50 mt-auto">
            <div class="flex gap-2">
              <router-link 
                :to="`/admin/recipes/edit/${recipe.id}`"
                class="p-2 bg-indigo-50 text-indigo-600 rounded-xl hover:bg-indigo-600 hover:text-white transition-all active:scale-90"
              >
                ✏️
              </router-link>
              <button 
                @click="confirmDelete(recipe)"
                class="p-2 bg-red-50 text-red-600 rounded-xl hover:bg-red-600 hover:text-white transition-all active:scale-90"
              >
                🗑️
              </button>
            </div>
            <router-link :to="`/recipes/${recipe.id}`" class="text-xs font-bold text-green-600 hover:underline">
              Просмотр →
            </router-link>
          </div>
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

const filteredRecipes = computed(() => {
  if (!searchQuery.value) return store.recipes;
  const q = searchQuery.value.toLowerCase();
  return store.recipes.filter(r => r.name.toLowerCase().includes(q));
});

const getCategoryName = (id) => {
  const cat = store.categories.find(c => c.id === id);
  return cat ? cat.name : 'Без категории';
};

const confirmDelete = async (recipe) => {
  if (confirm(`Вы уверены, что хотите удалить рецепт "${recipe.name}"?`)) {
    try {
      await store.deleteRecipe(recipe.id);
    } catch (err) {
      alert('Ошибка при удалении');
    }
  }
};

onMounted(() => {
  store.fetchCategories();
  store.fetchRecipes({ size: 100 }); // Load many for management
});
</script>
