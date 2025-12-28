// frontend/src/stores/recipesStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import recipeService from "@/services/recipeService";

export const useRecipesStore = defineStore("recipes", () => {
  // === STATE ===
  const recipes = ref([]);
  const currentRecipe = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  const pagination = ref({
    cursor: null,
    hasMore: false,
  });

  const categories = ref([]);
  const ingredients = ref([]);
  const storePrices = ref({}); // { ingredientId: [prices] }

  const filters = ref({
    categoryId: null,
    minCalories: null,
    maxCalories: null,
    maxTime: null,
    excludeIngredients: [],
  });

  // === COMPUTED ===
  const hasMoreRecipes = computed(() => pagination.value.hasMore);
  const isEmpty = computed(() => recipes.value.length === 0);

  // === ACTIONS ===
  const fetchRecipes = async (additionalParams = {}, append = false) => {
    isLoading.value = true;
    error.value = null;

    try {
      const queryParams = {
        ...filters.value,
        ...additionalParams,
        size: 9,
      };

      const response = await recipeService.getRecipes(queryParams);

      if (append) {
        recipes.value.push(...response.data);
      } else {
        recipes.value = response.data;
      }

      pagination.value.cursor = response.next_cursor;
      pagination.value.hasMore = response.has_more;
    } catch (err) {
      error.value = "Ошибка загрузки рецептов";
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  };

  const loadMore = async () => {
    if (!pagination.value.cursor || !pagination.value.hasMore) return;

    await fetchRecipes({ cursor: pagination.value.cursor }, true);
  };

  const fetchRecipe = async (recipeId) => {
    isLoading.value = true;
    error.value = null;

    try {
      currentRecipe.value = await recipeService.getRecipe(recipeId);
    } catch (err) {
      error.value = "Ошибка загрузки рецепта";
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  };

  const fetchCategories = async () => {
    try {
      categories.value = await recipeService.getCategories();
    } catch (err) {
      console.error("Error fetching categories:", err);
    }
  };

  const fetchIngredients = async () => {
    try {
      const response = await recipeService.getIngredients({ size: 100 });
      ingredients.value = response.data;
    } catch (err) {
      console.error("Error fetching ingredients:", err);
    }
  };

  const fetchIngredientPrices = async (ingredientId) => {
    try {
      const prices = await recipeService.getIngredientPrices(ingredientId);
      storePrices.value[ingredientId] = prices;
    } catch (err) {
      console.error(`Error fetching prices for ingredient ${ingredientId}:`, err);
    }
  };

  const createIngredient = async (data) => {
    try {
      const newIng = await recipeService.createIngredient(data);
      ingredients.value.push(newIng);
      return newIng;
    } catch (err) {
      console.error("Error creating ingredient:", err);
      throw err;
    }
  };

  const updateIngredient = async (id, data) => {
    try {
      const updated = await recipeService.updateIngredient(id, data);
      const idx = ingredients.value.findIndex(i => i.id === id);
      if (idx !== -1) {
        ingredients.value[idx] = updated;
      }
      return updated;
    } catch (err) {
      console.error("Error updating ingredient:", err);
      throw err;
    }
  };

  const deleteIngredient = async (id) => {
    try {
      await recipeService.deleteIngredient(id);
      ingredients.value = ingredients.value.filter(i => i.id !== id);
    } catch (err) {
      console.error("Error deleting ingredient:", err);
      throw err;
    }
  };

  const createRecipe = async (data) => {
    try {
      const newRec = await recipeService.createRecipe(data);
      recipes.value.unshift(newRec);
      return newRec;
    } catch (err) {
      console.error("Error creating recipe:", err);
      throw err;
    }
  };

  const updateRecipe = async (id, data) => {
    try {
      const updated = await recipeService.updateRecipe(id, data);
      const idx = recipes.value.findIndex(r => r.id === id);
      if (idx !== -1) {
        recipes.value[idx] = updated;
      }
      if (currentRecipe.value?.id === id) {
        currentRecipe.value = updated;
      }
      return updated;
    } catch (err) {
      console.error("Error updating recipe:", err);
      throw err;
    }
  };

  const deleteRecipe = async (id) => {
    try {
      await recipeService.deleteRecipe(id);
      recipes.value = recipes.value.filter(r => r.id !== id);
    } catch (err) {
      console.error("Error deleting recipe:", err);
      throw err;
    }
  };

  const createCategory = async (data) => {
    try {
      const newCat = await recipeService.createCategory(data);
      categories.value.push(newCat);
      return newCat;
    } catch (err) {
      console.error("Error creating category:", err);
      throw err;
    }
  };

  const updateCategory = async (id, data) => {
    try {
      const updated = await recipeService.updateCategory(id, data);
      const idx = categories.value.findIndex(c => c.id === id);
      if (idx !== -1) {
        categories.value[idx] = updated;
      }
      return updated;
    } catch (err) {
      console.error("Error updating category:", err);
      throw err;
    }
  };

  const deleteCategory = async (id) => {
    try {
      await recipeService.deleteCategory(id);
      categories.value = categories.value.filter(c => c.id !== id);
    } catch (err) {
      console.error("Error deleting category:", err);
      throw err;
    }
  };

  const setFilter = (key, value) => {
    filters.value[key] = value;
  };

  const toggleExcludeIngredient = (ingredientId) => {
    const idx = filters.value.excludeIngredients.indexOf(ingredientId);
    if (idx > -1) {
      filters.value.excludeIngredients.splice(idx, 1);
    } else {
      filters.value.excludeIngredients.push(ingredientId);
    }
  };

  const clearFilters = () => {
    filters.value = {
      categoryId: null,
      minCalories: null,
      maxCalories: null,
      maxTime: null,
      excludeIngredients: [],
    };
  };

  const clearError = () => {
    error.value = null;
  };

  return {
    recipes,
    currentRecipe,
    isLoading,
    error,
    pagination,
    categories,
    ingredients,
    storePrices,
    filters,
    hasMoreRecipes,
    isEmpty,
    fetchRecipes,
    loadMore,
    fetchRecipe,
    fetchCategories,
    fetchIngredients,
    fetchIngredientPrices,
    createIngredient,
    updateIngredient,
    deleteIngredient,
    createRecipe,
    updateRecipe,
    deleteRecipe,
    createCategory,
    updateCategory,
    deleteCategory,
    setFilter,
    toggleExcludeIngredient,
    clearFilters,
    clearError,
  };
});
