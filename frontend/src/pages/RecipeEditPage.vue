<template>
  <div class="container mx-auto px-4 py-8 max-w-5xl">
    <div class="mb-8">
      <button @click="$router.back()" class="text-green-600 hover:text-green-700 font-medium flex items-center gap-1 mb-4 transition-transform hover:-translate-x-1">
        ← Назад
      </button>
      <h1 class="text-4xl font-black text-gray-900">
        {{ isEditing ? 'Редактировать рецепт' : 'Новый рецепт' }}
      </h1>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-8">
      <!-- Main Info -->
      <div class="bg-white p-8 rounded-[2rem] shadow-sm border border-gray-100 ring-1 ring-gray-100/50">
        <h2 class="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
          <span class="w-8 h-8 bg-green-50 text-green-600 rounded-lg flex items-center justify-center text-sm">1</span> Основная информация
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="md:col-span-2">
            <label class="block text-sm font-black text-gray-400 uppercase tracking-widest mb-2">Название рецепта</label>
            <input v-model="formData.name" type="text" required class="w-full px-5 py-4 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500 rounded-2xl transition-all font-bold text-lg" />
          </div>
          
          <div class="md:col-span-2">
            <label class="block text-sm font-black text-gray-400 uppercase tracking-widest mb-2">Описание</label>
            <textarea v-model="formData.description" required rows="3" class="w-full px-5 py-4 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500 rounded-2xl transition-all"></textarea>
          </div>

          <div>
            <label class="block text-sm font-black text-gray-400 uppercase tracking-widest mb-2">Категория</label>
            <select v-model="formData.category_id" required class="w-full px-5 py-4 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500 rounded-2xl transition-all font-bold">
              <option v-for="cat in store.categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-black text-gray-400 uppercase tracking-widest mb-2">Сложность</label>
            <select v-model="formData.difficulty" class="w-full px-5 py-4 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500 rounded-2xl transition-all font-bold">
              <option value="Легко">Легко</option>
              <option value="Средне">Средне</option>
              <option value="Сложно">Сложно</option>
            </select>
          </div>

          <div>
             <label class="block text-sm font-black text-gray-400 uppercase tracking-widest mb-2">Время (мин)</label>
             <input v-model.number="formData.cook_time_minutes" type="number" required class="w-full px-5 py-4 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500 rounded-2xl transition-all font-bold" />
          </div>

          <div>
             <label class="block text-sm font-black text-gray-400 uppercase tracking-widest mb-2">Порции</label>
             <input v-model.number="formData.portions" type="number" required class="w-full px-5 py-4 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-green-500 rounded-2xl transition-all font-bold" />
          </div>
        </div>
      </div>

      <!-- Ingredients -->
      <div class="bg-white p-8 rounded-[2rem] shadow-sm border border-gray-100 ring-1 ring-gray-100/50">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">
            <span class="w-8 h-8 bg-blue-50 text-blue-600 rounded-lg flex items-center justify-center text-sm">2</span> Ингредиенты
          </h2>
          <button @click.prevent="addIngredient" class="text-sm font-bold text-blue-600 hover:text-blue-700">+ Добавить ещё</button>
        </div>

        <div class="space-y-4">
          <div v-for="(ing, index) in formData.ingredients" :key="index" class="flex flex-wrap md:flex-nowrap gap-4 p-4 bg-gray-50 rounded-2xl items-end relative">
            <div class="flex-grow w-full md:w-auto">
              <label class="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Ингредиент</label>
              <select v-model="ing.ingredient_id" required class="w-full px-4 py-2 bg-white border border-gray-100 rounded-xl focus:ring-2 focus:ring-blue-500 font-medium">
                <option v-for="i in store.ingredients" :key="i.id" :value="i.id">{{ i.name }}</option>
              </select>
            </div>
            <div class="w-32">
              <label class="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Кол-во</label>
              <input v-model.number="ing.quantity" type="number" step="0.1" required class="w-full px-4 py-2 bg-white border border-gray-100 rounded-xl focus:ring-2 focus:ring-blue-500 font-mono" />
            </div>
            <div class="w-32">
              <label class="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Ед. изм.</label>
              <input v-model="ing.unit" type="text" required placeholder="г, шт..." class="w-full px-4 py-2 bg-white border border-gray-100 rounded-xl focus:ring-2 focus:ring-blue-500" />
            </div>
            <button @click.prevent="removeIngredient(index)" v-if="formData.ingredients.length > 1" class="p-2 text-red-400 hover:text-red-600 transition-colors">🗑️</button>
          </div>
        </div>
      </div>

      <!-- Instructions -->
      <div class="bg-white p-8 rounded-[2rem] shadow-sm border border-gray-100 ring-1 ring-gray-100/50">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">
            <span class="w-8 h-8 bg-purple-50 text-purple-600 rounded-lg flex items-center justify-center text-sm">3</span> Шаги приготовления
          </h2>
          <button @click.prevent="addStep" class="text-sm font-bold text-purple-600 hover:text-purple-700">+ Добавить шаг</button>
        </div>

        <div class="space-y-6">
          <div v-for="(step, index) in formData.instructions" :key="index" class="flex gap-4">
            <div class="w-10 h-10 bg-gray-100 text-gray-400 font-bold rounded-xl flex items-center justify-center flex-shrink-0 mt-2">
              {{ index + 1 }}
            </div>
            <div class="flex-grow space-y-3">
              <textarea v-model="step.description" required rows="2" placeholder="Опишите процесс..." class="w-full px-5 py-4 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-purple-500 rounded-2xl transition-all"></textarea>
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-gray-400 uppercase tracking-widest">Время шага:</span>
                <input v-model.number="step.time_minutes" type="number" class="w-20 px-3 py-1 bg-gray-50 rounded-lg font-mono text-sm" />
                <span class="text-xs text-gray-400 font-bold">мин</span>
              </div>
            </div>
            <button @click.prevent="removeStep(index)" v-if="formData.instructions.length > 1" class="self-start mt-4 p-2 text-red-400 hover:text-red-600">✕</button>
          </div>
        </div>
      </div>

      <div class="flex gap-4">
        <button 
          type="submit" 
          :disabled="isSubmitting"
          class="flex-grow bg-green-600 hover:bg-green-700 text-white font-black py-5 px-8 rounded-[2rem] transition-all shadow-xl shadow-green-100 active:scale-95 disabled:opacity-50 text-xl"
        >
          {{ isSubmitting ? 'Сохранение...' : (isEditing ? 'Сохранить изменения' : 'Опубликовать рецепт') }}
        </button>
        <button 
          type="button" 
          @click="$router.back()" 
          class="px-12 bg-gray-100 hover:bg-gray-200 text-gray-500 font-bold rounded-[2rem] transition-all"
        >
          {{ isEditing ? 'Отмена' : 'Сбросить' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useRecipesStore } from '@/stores/recipesStore';

const route = useRoute();
const router = useRouter();
const store = useRecipesStore();
const isSubmitting = ref(false);
const isEditing = computed(() => !!route.params.id);

const formData = ref({
  name: '',
  description: '',
  category_id: null,
  cook_time_minutes: 30,
  portions: 2,
  difficulty: 'Легко',
  ingredients: [
    { ingredient_id: null, quantity: 0, unit: 'г' }
  ],
  instructions: [
    { step: 1, description: '', time_minutes: 5 }
  ]
});

const addIngredient = () => {
  formData.value.ingredients.push({ ingredient_id: null, quantity: 0, unit: 'г' });
};

const removeIngredient = (index) => {
  formData.value.ingredients.splice(index, 1);
};

const addStep = () => {
  const nextStep = formData.value.instructions.length + 1;
  formData.value.instructions.push({ step: nextStep, description: '', time_minutes: 5 });
};

const removeStep = (index) => {
  formData.value.instructions.splice(index, 1);
  // Re-index
  formData.value.instructions.forEach((s, i) => s.step = i + 1);
};

const handleSubmit = async () => {
  isSubmitting.value = true;
  try {
    // Validation
    if (formData.value.ingredients.length < 2) {
      alert('Рецепт должен содержать минимум 2 ингредиента');
      isSubmitting.value = false;
      return;
    }

    const payload = {
      ...formData.value,
      // Ensure specific fields are correct type for MongoDB/FastAPI
      cook_time_minutes: Number(formData.value.cook_time_minutes),
      portions: Number(formData.value.portions)
    };
    
    if (isEditing.value) {
      await store.updateRecipe(route.params.id, payload);
    } else {
      await store.createRecipe(payload);
    }
    router.push('/admin/recipes');
  } catch (err) {
    console.error(err);
    alert(err.response?.data?.detail || 'Ошибка при сохранении рецепта');
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(async () => {
  await store.fetchCategories();
  await store.fetchIngredients();
  
  if (isEditing.value) {
    await store.fetchRecipe(route.params.id);
    if (store.currentRecipe) {
      // Create a clean copy for the form
      const r = store.currentRecipe;
      formData.value = {
        name: r.name,
        description: r.description,
        category_id: r.category_id,
        cook_time_minutes: r.cook_time_minutes,
        portions: r.portions,
        difficulty: r.difficulty || 'Легко',
        ingredients: r.ingredients.map(i => ({
          ingredient_id: i.ingredient_id,
          quantity: i.quantity,
          unit: i.unit
        })),
        instructions: r.instructions.map(s => ({
          step: s.step,
          description: s.description,
          time_minutes: s.time_minutes
        }))
      };
    }
  } else {
    // Set default category
    if (store.categories.length > 0) {
      formData.value.category_id = store.categories[0].id;
    }
  }
});
</script>
