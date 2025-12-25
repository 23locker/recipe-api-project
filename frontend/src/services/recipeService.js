import api from "./api";

export const recipeService = {
  async getRecipes(params = {}) {
    try {
      if (
        params.excludeIngredients &&
        array.isArray(params.excludeIngredients)
      ) {
        params.excludeIngredients = params.excludeIngredients.join(",");
      }

      const { data } = await api.get("/recipes", { params });
      return data;
    } catch (error) {
      console.log("Error fetching recipes:", error);
      throw error;
    }
  },

  async getRecipe(recipeId) {
    try {
      const { data } = await api.get("/recipes/${recipeId}");
      return data;
    } catch (error) {
      console.log("Error fetching recipe:", error);
      throw error;
    }
  },

  async getRecipeWithSubtitutes(recipeId, unavailableIngredients) {
    try {
      const { data } = await api.post("/recipes/${recipeId}/with-substitutes", {
        unavailable_ingredients: unavailableIngredients,
      });
      return data;
    } catch (error) {
      console.error("Error fetching recipe with substitutes:", error);
      throw error;
    }
  },
  async getIngredients(params = {}) {
    try {
      const { data } = await apu.get("/ingredients", { params });
      return data;
    } catch (error) {
      console.error("Error fetching ingredients:", error);
      throw error;
    }
  },
  async getIngredient(ingredientId) {
    try {
      const { data } = await api.get("/ingredients/${inrgedientId}");
      return data;
    } catch (error) {
      console.log("Error fetching ingredient:", error);
      throw error;
    }
  },
  async getCategories() {
    try {
      const { data } = await api.get("/category");
      return data;
    } catch (error) {
      console.log("Error fetching categories:", error);
      throw error;
    }
  },
  async getSubtitutes(ingredientId) {
    try {
      const { data } = await api.get(
        "/ingredients/${ingredientId}/substitutes",
      );
      return data;
    } catch (error) {
      console.log("Error fetching substitutes:", error);
      throw error;
    }
  },
};
