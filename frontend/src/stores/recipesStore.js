// frontend/src/stores/recipesStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { recipeService } from "@/services/recipeService";

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
      categories.value = [];
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
    filters,
    hasMoreRecipes,
    isEmpty,
    fetchRecipes,
    loadMore,
    fetchRecipe,
    fetchCategories,
    fetchIngredients,
    setFilter,
    toggleExcludeIngredient,
    clearFilters,
    clearError,
  };
});
