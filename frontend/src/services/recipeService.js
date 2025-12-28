// frontend/src/services/recipeService.js
import api from "./api";

/**
 * Recipes сервис — всё что связано с рецептами и ингредиентами
 */

const recipeService = {
  /**
   * Получить список рецептов с фильтрами и пагинацией
   *
   * @param {Object} params - параметры запроса
   * @param {string} params.cursor - курсор для пагинации (опционально)
   * @param {number} params.size - количество рецептов на странице (опционально)
   * @param {number} params.categoryId - ID категории (опционально)
   * @param {number} params.minCalories - минимальные калории (опционально)
   * @param {number} params.maxCalories - максимальные калории (опционально)
   * @param {number} params.maxTime - максимальное время готовки (опционально)
   * @param {Array} params.excludeIngredients - ID ингредиентов для исключения (опционально)
   *
   * @returns {Promise} объект с полями:
   * {
   *   "data": [рецепты],
   *   "next_cursor": "курсор для следующей страницы",
   *   "has_more": true/false
   * }
   */
  async getRecipes(params = {}) {
    try {
      // Преобразуем массив в строку если нужно
      const queryParams = {
        cursor: params.cursor,
        size: params.size,
        category_id: params.categoryId,
        min_calories: params.minCalories,
        max_calories: params.maxCalories,
        max_time: params.maxTime,
        exclude_ingredients: Array.isArray(params.excludeIngredients)
          ? params.excludeIngredients.join(",")
          : params.excludeIngredients
      };

      // Remove undefined/null/empty keys to keep URL clean
      Object.keys(queryParams).forEach(key =>
        (queryParams[key] === undefined || queryParams[key] === null || queryParams[key] === "") && delete queryParams[key]
      );

      const { data } = await api.get("/recipes", { params: queryParams });
      return data;
    } catch (error) {
      console.error("Error fetching recipes:", error);
      throw error;
    }
  },

  /**
   * Получить один рецепт по ID
   *
   * @param {string} recipeId - ID рецепта (ObjectId из MongoDB)
   * @returns {Promise} - данные рецепта
   */
  async getRecipe(recipeId) {
    try {
      const { data } = await api.get(`/recipes/${recipeId}`);
      return data;
    } catch (error) {
      console.error("Error fetching recipe:", error);
      throw error;
    }
  },

  /**
   * Получить рецепт с заменами для недоступных ингредиентов
   *
   * Например: у тебя нет масла, приложение найдёт替альную маргарин
   *
   * @param {string} recipeId - ID рецепта
   * @param {Array} unavailableIngredients - массив объектов {ingredient_id: 1}
   * @returns {Promise} - рецепт с заменённых ингредиентов
   */
  async getRecipeWithSubstitutes(recipeId, unavailableIngredients) {
    try {
      const { data } = await api.post(`/recipes/${recipeId}/with-substitutes`, {
        unavailable_ingredients: unavailableIngredients,
      });
      return data;
    } catch (error) {
      console.error("Error fetching recipe with substitutes:", error);
      throw error;
    }
  },

  /**
   * Получить список ингредиентов
   *
   * @param {Object} params - параметры (cursor, size, search)
   * @returns {Promise} объект с полями:
   * {
   *   "data": [ингредиенты],
   *   "next_cursor": "...",
   *   "has_more": true/false
   * }
   */
  async getIngredients(params = {}) {
    try {
      const { data } = await api.get("/ingredients", { params });
      return data;
    } catch (error) {
      console.error("Error fetching ingredients:", error);
      throw error;
    }
  },

  /**
   * Получить один ингредиент по ID
   *
   * @param {number} ingredientId
   * @returns {Promise} - данные ингредиента
   */
  async getIngredient(ingredientId) {
    try {
      const { data } = await api.get(`/ingredients/${ingredientId}`);
      return data;
    } catch (error) {
      console.error("Error fetching ingredient:", error);
      throw error;
    }
  },

  /**
   * Получить категории рецептов
   *
   * @returns {Promise} - массив категорий
   */
  async getCategories() {
    try {
      const { data } = await api.get("/category");
      return data.items;
    } catch (error) {
      console.error("Error fetching categories:", error);
      throw error;
    }
  },

  /**
   * Получить замены для ингредиента
   *
   * @param {number} ingredientId
   * @returns {Promise} - массив возможных замен
   */
  async getSubstitutes(ingredientId) {
    try {
      const { data } = await api.get(
        `/ingredients/${ingredientId}/substitutes`,
      );
      return data;
    } catch (error) {
      console.error("Error fetching substitutes:", error);
      throw error;
    }
  },
  /**
   * Получить цены на конкретный ингредиент во всех магазинах
   *
   * @param {number} ingredientId
   * @returns {Promise} - массив товаров с ценами
   */
  async getIngredientPrices(ingredientId) {
    try {
      const { data } = await api.get(`/store/products/${ingredientId}`);
      return data;
    } catch (error) {
      console.error("Error fetching ingredient prices:", error);
      throw error;
    }
  },

  /**
   * Получить список всех доступных в магазинах продуктов
   *
   * @param {number} limit
   * @returns {Promise} - список товаров
   */
  async getAllStoreProducts(limit = 50) {
    try {
      const { data } = await api.get("/store/products", { params: { limit } });
      return data;
    } catch (error) {
      console.error("Error fetching all store products:", error);
      throw error;
    }
  },
  /**
   * Создать новый ингредиент
   *
   * @param {Object} data
   * @returns {Promise}
   */
  async createIngredient(data) {
    try {
      const { data: created } = await api.post("/ingredients", data);
      return created;
    } catch (error) {
      console.error("Error creating ingredient:", error);
      throw error;
    }
  },

  /**
   * Обновить существующий ингредиент
   *
   * @param {number} id
   * @param {Object} data
   * @returns {Promise}
   */
  async updateIngredient(id, data) {
    try {
      const { data: updated } = await api.put(`/ingredients/${id}`, data);
      return updated;
    } catch (error) {
      console.error("Error updating ingredient:", error);
      throw error;
    }
  },

  /**
   * Удалить ингредиент
   *
   * @param {number} id
   * @returns {Promise}
   */
  async deleteIngredient(id) {
    try {
      await api.delete(`/ingredients/${id}`);
      return true;
    } catch (error) {
      console.error("Error deleting ingredient:", error);
      throw error;
    }
  },

  /**
   * Создать новый рецепт
   */
  async createRecipe(data) {
    try {
      const { data: created } = await api.post("/recipes", data);
      return created;
    } catch (error) {
      console.error("Error creating recipe:", error);
      throw error;
    }
  },

  /**
   * Обновить рецепт
   */
  async updateRecipe(id, data) {
    try {
      const { data: updated } = await api.put(`/recipes/${id}`, data);
      return updated;
    } catch (error) {
      console.error("Error updating recipe:", error);
      throw error;
    }
  },

  /**
   * Удалить рецепт
   */
  async deleteRecipe(id) {
    try {
      await api.delete(`/recipes/${id}`);
      return true;
    } catch (error) {
      console.error("Error deleting recipe:", error);
      throw error;
    }
  },

  /**
   * Создать категорию
   */
  async createCategory(data) {
    try {
      const { data: created } = await api.post("/category", data);
      return created;
    } catch (error) {
      console.error("Error creating category:", error);
      throw error;
    }
  },

  /**
   * Обновить категорию
   */
  async updateCategory(id, data) {
    try {
      const { data: updated } = await api.put(`/category/${id}`, data);
      return updated;
    } catch (error) {
      console.error("Error updating category:", error);
      throw error;
    }
  },

  /**
   * Удалить категорию
   */
  async deleteCategory(id) {
    try {
      await api.delete(`/category/${id}`);
      return true;
    } catch (error) {
      console.error("Error deleting category:", error);
      throw error;
    }
  },

  /**
   * Получить все замены ингредиентов
   */
  async getAllSubstitutes() {
    try {
      const { data } = await api.get("/ingredients/substitutes/all");
      return data;
    } catch (error) {
      console.error("Error fetching all substitutes:", error);
      throw error;
    }
  },

  /**
   * Создать замену ингредиента
   * @param {Object} substituteData - {original_ingredient_id, substitute_ingredient_id, coefficient}
   */
  async createSubstitute(substituteData) {
    try {
      const { data } = await api.post("/ingredients/substitutes", substituteData);
      return data;
    } catch (error) {
      console.error("Error creating substitute:", error);
      throw error;
    }
  },

  /**
   * Удалить замену ингредиента
   * @param {number} substituteId
   */
  async deleteSubstitute(substituteId) {
    try {
      await api.delete(`/ingredients/substitutes/${substituteId}`);
      return true;
    } catch (error) {
      console.error("Error deleting substitute:", error);
      throw error;
    }
  },
};

export default recipeService;
