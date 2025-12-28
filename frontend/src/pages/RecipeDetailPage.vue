<template>
  <div class="container mx-auto px-4 py-8 max-w-5xl">
    <div v-if="store.isLoading && !store.currentRecipe" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
    </div>

    <div v-else-if="recipe" class="animate-fade-in">
      <!-- Header -->
      <div class="mb-8">
        <router-link to="/recipes" class="text-green-600 hover:text-green-700 font-medium flex items-center gap-1 mb-4 transition-transform hover:-translate-x-1 inline-flex">
          ← Назад в список
        </router-link>
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h1 class="text-4xl font-black text-gray-900 mb-2">{{ recipe.name }}</h1>
            <p class="text-xl text-gray-500 max-w-2xl">{{ recipe.description }}</p>
          </div>
          <div class="flex gap-3">
             <span class="bg-orange-50 text-orange-700 px-4 py-2 rounded-2xl font-bold text-sm border border-orange-100 italic">
               {{ recipe.difficulty }}
             </span>
             <span class="bg-blue-50 text-blue-700 px-4 py-2 rounded-2xl font-bold text-sm border border-blue-100">
               {{ recipe.cook_time_minutes }} минут
             </span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Ingredients List -->
        <div class="lg:col-span-1">
          <div class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col h-full ring-1 ring-gray-50">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-gray-800">Ингредиенты</h2>
              <span class="text-sm font-medium text-gray-400 bg-gray-50 px-3 py-1 rounded-full">
                {{ recipe.portions }} порц.
              </span>
            </div>
            
            <ul class="space-y-4 flex-grow">
              <li 
                v-for="ing in recipe.ingredients" 
                :key="ing.ingredient_id"
                class="group p-4 rounded-2xl transition-all border border-transparent hover:bg-gray-50 hover:border-gray-100"
                :class="{'opacity-50 line-through grayscale': unavailableIds.has(ing.ingredient_id)}"
              >
                <div class="flex justify-between items-start mb-2">
                  <div class="flex items-center gap-3">
                    <button 
                      @click="toggleUnavailable(ing.ingredient_id)"
                      class="w-6 h-6 rounded-lg border-2 flex items-center justify-center transition-all"
                      :class="unavailableIds.has(ing.ingredient_id) ? 'bg-red-500 border-red-500 text-white' : 'border-gray-200 hover:border-green-500'"
                    >
                      <span v-if="unavailableIds.has(ing.ingredient_id)" class="text-[10px]">✕</span>
                    </button>
                    <span class="font-bold text-gray-800">{{ getIngredientName(ing.ingredient_id) }}</span>
                  </div>
                  <span class="text-sm font-medium text-gray-500 bg-gray-100 px-2 py-0.5 rounded-lg">
                    {{ ing.quantity }} {{ ing.unit }}
                  </span>
                </div>

                <!-- Store Prices -->
                <div v-if="!unavailableIds.has(ing.ingredient_id)" class="ml-9">
                  <div v-if="getLowestPrice(ing.ingredient_id)" class="text-xs text-emerald-600 font-bold flex items-center gap-1">
                    <span class="text-base">🛒</span> От {{ getLowestPrice(ing.ingredient_id).price }} ₽ в Пятёрочке
                  </div>
                  <div v-else class="text-[10px] text-gray-400 italic">Цены не найдены</div>
                </div>
              </li>
            </ul>

            <div v-if="unavailableIds.size > 0" class="mt-8 pt-6 border-t border-gray-100">
               <button 
                @click="applySubstitutes"
                :disabled="store.isLoading"
                class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-6 rounded-2xl transition-all shadow-lg shadow-indigo-100 active:scale-95"
               >
                 {{ store.isLoading ? 'Ищем альтернативы...' : 'Найти замены' }}
               </button>
               <p class="text-[10px] text-center text-gray-400 mt-3 px-4">
                 Мы подберем аналоги для выбранных ингредиентов и пересчитаем КБЖУ
               </p>
            </div>
          </div>
        </div>

        <!-- Instructions & Nutrition -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Nutrition -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
             <div class="bg-emerald-50 p-4 rounded-3xl border border-emerald-100 text-center">
               <div class="text-sm font-bold text-emerald-600 uppercase tracking-tighter mb-1">Калории</div>
               <div class="text-3xl font-black text-emerald-900">{{ Math.round(recipe.total_calories) }}</div>
             </div>
             <div class="bg-blue-50 p-4 rounded-3xl border border-blue-100 text-center">
               <div class="text-sm font-bold text-blue-600 uppercase tracking-tighter mb-1">Белки</div>
               <div class="text-3xl font-black text-blue-900">{{ Math.round(recipe.total_protein) }}г</div>
             </div>
             <div class="bg-purple-50 p-4 rounded-3xl border border-purple-100 text-center">
               <div class="text-sm font-bold text-purple-600 uppercase tracking-tighter mb-1">Жиры</div>
               <div class="text-3xl font-black text-purple-900">{{ Math.round(recipe.total_fat) }}г</div>
             </div>
             <div class="bg-orange-50 p-4 rounded-3xl border border-orange-100 text-center">
               <div class="text-sm font-bold text-orange-600 uppercase tracking-tighter mb-1">Углеводы</div>
               <div class="text-3xl font-black text-orange-900">{{ Math.round(recipe.total_carbs) }}г</div>
             </div>
          </div>

          <!-- Instructions -->
          <div class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 ring-1 ring-gray-50">
            <h2 class="text-2xl font-bold text-gray-800 mb-8 flex items-center gap-3">
              👨‍🍳 Приготовление
            </h2>
            <div class="space-y-10">
              <div 
                v-for="(step, index) in sortedInstructions" 
                :key="index"
                class="flex gap-6 group"
              >
                <div class="flex-shrink-0">
                  <div class="w-10 h-10 rounded-2xl bg-gray-50 text-gray-400 font-bold flex items-center justify-center transition-colors group-hover:bg-green-600 group-hover:text-white">
                    {{ step.step }}
                  </div>
                </div>
                <div class="pt-1">
                  <p class="text-gray-700 leading-relaxed text-lg">{{ step.description }}</p>
                  <div v-if="step.time_minutes" class="mt-2 text-sm font-bold text-indigo-500 inline-flex items-center gap-1 bg-indigo-50 px-2 py-0.5 rounded-lg">
                    ⏱ {{ step.time_minutes }} мин
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useRecipesStore } from '@/stores/recipesStore';
import recipeService from '@/services/recipeService';

const route = useRoute();
const store = useRecipesStore();
const recipe = computed(() => store.currentRecipe);
const unavailableIds = ref(new Set());

const sortedInstructions = computed(() => {
  if (!recipe.value?.instructions) return [];
  return [...recipe.value.instructions].sort((a, b) => a.step - b.step);
});

const getIngredientName = (id) => {
  const ing = store.ingredients.find(i => i.id === id);
  return ing ? ing.name : `Ингредиент #${id}`;
};

const toggleUnavailable = (id) => {
  if (unavailableIds.value.has(id)) {
    unavailableIds.value.delete(id);
  } else {
    unavailableIds.value.add(id);
  }
};

const getLowestPrice = (id) => {
  const prices = store.storePrices[id];
  if (!prices || prices.length === 0) return null;
  return [...prices].sort((a, b) => a.price - b.price)[0];
};

const applySubstitutes = async () => {
  const list = Array.from(unavailableIds.value).map(id => ({ ingredient_id: id }));
  try {
    store.isLoading = true;
    const modified = await recipeService.getRecipeWithSubstitutes(recipe.value.id, list);
    if (modified) {
      store.currentRecipe = modified;
      // Fetch prices for new ingredients
      for (const ing of modified.ingredients) {
         if (!store.storePrices[ing.ingredient_id]) {
            store.fetchIngredientPrices(ing.ingredient_id);
         }
      }
      unavailableIds.value.clear();
    }
  } catch (err) {
    alert("Не удалось найти замены для этих ингредиентов");
  } finally {
    store.isLoading = false;
  }
};

onMounted(async () => {
  await store.fetchIngredients();
  await store.fetchRecipe(route.params.id);
  
  if (recipe.value) {
    recipe.value.ingredients.forEach(ing => {
      store.fetchIngredientPrices(ing.ingredient_id);
    });
  }
});
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
