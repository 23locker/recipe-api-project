<template>
  <div class="container mx-auto px-4 py-8 max-w-6xl">
    <div class="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <router-link to="/admin" class="text-green-600 hover:text-green-700 font-medium flex items-center gap-1 mb-4 transition-transform hover:-translate-x-1 inline-flex">
          ← В админку
        </router-link>
        <h1 class="text-4xl font-black text-gray-900">Товары в магазинах</h1>
        <p class="text-gray-500 mt-2">База данных товаров, собранная парсерами (Пятёрочка и др.)</p>
      </div>
      
      <div class="bg-orange-50 px-6 py-3 rounded-2xl border border-orange-100 flex items-center gap-3">
        <div class="text-3xl">🛒</div>
        <div>
           <div class="text-[10px] text-orange-500 font-black uppercase tracking-wider mb-0.5">Всего товаров</div>
           <div class="text-xl font-black text-orange-900">{{ products.length }}+</div>
        </div>
      </div>
    </div>

    <!-- Search placeholder (API might not support search yet, but UI is ready) -->
    <div class="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 mb-8 flex items-center gap-4">
       <span class="text-gray-400">ℹ️</span>
       <p class="text-gray-500 text-sm">Здесь отображаются последние <b>{{ limit }}</b> товаров. Для поиска конкретного товара используйте базу ингредиентов.</p>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead class="bg-gray-50 border-b border-gray-100">
            <tr>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Фото</th>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Название</th>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Цена</th>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Магазин</th>
              <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest text-right">Ссылки</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-if="isLoading" class="animate-pulse">
               <td colspan="5" class="px-6 py-8 text-center text-gray-400">Загрузка данных...</td>
            </tr>
            <tr v-else-if="products.length === 0">
               <td colspan="5" class="px-6 py-8 text-center text-gray-400">Товары не найдены. Запустите парсер.</td>
            </tr>
            <tr v-for="product in products" :key="product.id || product.url" class="hover:bg-gray-50/50 transition-colors">
              <td class="px-6 py-4">
                 <div class="w-12 h-12 bg-gray-100 rounded-lg overflow-hidden border border-gray-200 flex items-center justify-center">
                    <img v-if="product.image_url" :src="product.image_url" alt="" class="w-full h-full object-cover" />
                    <span v-else class="text-xl">📦</span>
                 </div>
              </td>
              <td class="px-6 py-4">
                <div class="font-bold text-gray-900 line-clamp-2 max-w-md">{{ product.name }}</div>
                <div class="text-[10px] text-gray-400 mt-1" v-if="product.ingredient_id">Linked to Ingredient #{{ product.ingredient_id }}</div>
              </td>
              <td class="px-6 py-4">
                <span class="font-mono text-lg font-bold text-green-600">{{ product.price }} ₽</span>
              </td>
              <td class="px-6 py-4">
                 <span class="text-xs font-bold text-red-600 bg-red-50 px-2 py-1 rounded">5ka</span>
              </td>
              <td class="px-6 py-4 text-right">
                <a 
                  v-if="product.url" 
                  :href="product.url" 
                  target="_blank"
                  class="text-indigo-600 hover:text-indigo-800 font-bold text-sm bg-indigo-50 hover:bg-indigo-100 px-3 py-1.5 rounded-lg transition-colors inline-block"
                >
                  На сайт ↗
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Load More -->
      <div class="p-4 border-t border-gray-100 bg-gray-50 flex justify-center">
         <button 
           @click="loadMore" 
           :disabled="isLoading"
           class="text-gray-500 font-bold hover:text-gray-800 transition-colors text-sm"
         >
           {{ isLoading ? 'Загрузка...' : 'Загрузить ещё 50' }}
         </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import recipeService from '@/services/recipeService';

const products = ref([]);
const isLoading = ref(false);
const limit = ref(50);

const fetchProducts = async () => {
  isLoading.value = true;
  try {
    const data = await recipeService.getAllStoreProducts(limit.value);
    // data might be array or object from FastAPI, assuming array based on service
    products.value = Array.isArray(data) ? data : (data.data || []);
  } catch (err) {
    console.error("Failed to load products", err);
  } finally {
    isLoading.value = false;
  }
};

const loadMore = () => {
  limit.value += 50;
  fetchProducts();
};

onMounted(() => {
  fetchProducts();
});
</script>
