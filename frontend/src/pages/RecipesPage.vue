<template>
  <div class="container mx-auto px-4 py-10">
    <!-- Hero Section -->
    <div class="relative bg-[#1e293b] rounded-[3rem] p-12 mb-12 overflow-hidden shadow-2xl shadow-indigo-100 border border-white/5 group">
      <!-- Glow background -->
      <div class="absolute top-0 right-0 w-[50%] h-[100%] bg-emerald-500/10 blur-[100px] rounded-full group-hover:bg-emerald-500/20 transition-all duration-500"></div>
      
      <div class="relative z-10 max-w-2xl">
        <div class="flex items-center gap-3 mb-6">
          <span class="px-4 py-1.5 bg-emerald-500/20 text-emerald-400 text-[10px] font-black uppercase tracking-[2px] rounded-full border border-emerald-500/20">Лучшие рецепты мира</span>
        </div>
        <h1 class="text-5xl md:text-6xl font-black text-white leading-tight mb-6">Готовьте как <span class="text-emerald-500 underline decoration-emerald-500/30 underline-offset-8">настоящий шеф</span></h1>
        <p class="text-slate-400 text-lg mb-10 leading-relaxed font-medium">Откройте для себя тысячи рецептов, оптимизированных по калориям и ценам. Вдохновение для вашего стола начинается здесь.</p>
        
        <div class="flex flex-wrap gap-4">
          <button @click="scrollToFilter" class="px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-white font-black rounded-2xl transition-all shadow-xl shadow-emerald-500/20 active:scale-95 flex items-center gap-2">
            🔍 Найти рецепт
          </button>
          
          <router-link 
            v-if="authStore.isAdmin" 
            to="/admin/recipes/new" 
            class="px-8 py-4 bg-white/10 hover:bg-white/20 text-white font-black rounded-2xl transition-all backdrop-blur-md border border-white/10 active:scale-95 flex items-center gap-2"
          >
            ➕ Создать рецепт
          </router-link>
        </div>
      </div>

      <!-- Floating Icon -->
      <div class="absolute right-12 bottom-12 text-[120px] opacity-20 rotate-12 -z-0 select-none pointer-events-none group-hover:rotate-0 transition-transform duration-700">
        🔪
      </div>
    </div>

    <!-- Filters -->
    <div id="filters" class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8 transition-all hover:shadow-md">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Категория</label>
          <select 
            v-model="store.filters.categoryId" 
            @change="store.fetchRecipes()"
            class="w-full border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
          >
            <option :value="null">Все категории</option>
            <option v-for="cat in store.categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Макс. калории</label>
          <input 
            v-model.number="store.filters.maxCalories" 
            @input="debounceFetch"
            type="number" 
            placeholder="Напр. 500"
            class="w-full border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Макс. время (мин)</label>
          <input 
            v-model.number="store.filters.maxTime" 
            @input="debounceFetch"
            type="number" 
            placeholder="Напр. 30"
            class="w-full border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
          />
        </div>
        <div class="flex items-end">
          <button 
            @click="clearFilters" 
            class="w-full bg-gray-50 hover:bg-orange-50 text-orange-600 font-semibold py-2 px-4 rounded-xl border border-orange-100 transition-all active:scale-95"
          >
            Сбросить фильтры
          </button>
        </div>
      </div>
    </div>

    <!-- Recipe Grid -->
    <div v-if="store.isLoading && store.recipes.length === 0" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
    </div>

    <div v-else-if="store.recipes.length === 0" class="text-center py-20 bg-gray-50 rounded-3xl border-2 border-dashed border-gray-200">
      <div class="text-6xl mb-4">🔍</div>
      <p class="text-xl text-gray-500">Рецепты не найдены. Попробуйте изменить фильтры.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <router-link 
        v-for="recipe in store.recipes" 
        :key="recipe.id" 
        :to="`/recipes/${recipe.id}`"
        class="group bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-1 block"
      >
        <div class="h-48 bg-gradient-to-br from-green-50 to-emerald-50 relative">
          <div class="absolute inset-0 flex items-center justify-center text-6xl group-hover:scale-110 transition-transform duration-300">
            🥘
          </div>
          <div class="absolute top-4 right-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-xs font-bold text-emerald-700 shadow-sm">
            {{ recipe.cook_time_minutes }} мин
          </div>
        </div>
        <div class="p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-2 truncate group-hover:text-green-600 transition-colors">{{ recipe.name }}</h2>
          <p class="text-gray-600 text-sm line-clamp-2 mb-4">{{ recipe.description }}</p>
          <div class="flex justify-between items-center pt-4 border-t border-gray-50">
            <div class="flex items-center gap-1">
              <span class="text-green-600 font-bold">{{ recipe.total_calories }}</span>
              <span class="text-gray-400 text-xs uppercase tracking-wider">ккал</span>
            </div>
            <div class="text-xs font-medium text-gray-400 bg-gray-50 px-2 py-1 rounded">
              {{ recipe.portions }} порции
            </div>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Load More -->
    <div v-if="store.hasMoreRecipes" class="flex justify-center mt-12 mb-8">
      <button 
        @click="store.loadMore" 
        :disabled="store.isLoading"
        class="bg-white hover:bg-gray-50 text-gray-800 font-bold py-3 px-10 rounded-2xl shadow-sm border border-gray-200 transition-all disabled:opacity-50 active:scale-95"
      >
        <span v-if="store.isLoading" class="flex items-center gap-2">
           <svg class="animate-spin h-5 w-5 text-gray-500" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
           Загрузка...
        </span>
        <span v-else>Показать еще</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRecipesStore } from '@/stores/recipesStore';
import { useAuthStore } from '@/stores/authStore';

const store = useRecipesStore();
const authStore = useAuthStore();
let debounceTimer = null;

const debounceFetch = () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    store.fetchRecipes();
  }, 500);
};

const clearFilters = () => {
  store.clearFilters();
  store.fetchRecipes();
};

const scrollToFilter = () => {
  const el = document.getElementById('filters');
  if (el) el.scrollIntoView({ behavior: 'smooth' });
};

onMounted(() => {
  store.fetchCategories();
  store.fetchRecipes();
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
