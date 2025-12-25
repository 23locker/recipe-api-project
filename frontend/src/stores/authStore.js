// frontend/src/stores/authStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { authService } from "@/services/authService";

export const useAuthStore = defineStore("auth", () => {
  // === STATE ===
  const user = ref(null);
  const token = ref(localStorage.getItem("access_token") || null);
  const isLoading = ref(false);
  const error = ref(null);

  // === COMPUTED ===
  const isAuthenticated = computed(() => !!token.value);
  const isAdmin = computed(() => user.value?.role === "admin");

  // === ACTIONS ===
  const register = async (username, email, password) => {
    isLoading.value = true;
    error.value = null;

    try {
      const userData = await authService.register(username, email, password);
      user.value = userData;
      return userData;
    } catch (err) {
      error.value = err.response?.data?.detail || "Ошибка регистрации";
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const login = async (username, password) => {
    isLoading.value = true;
    error.value = null;

    try {
      const { access_token, user: userData } = await authService.login(
        username,
        password,
      );

      token.value = access_token;
      user.value = userData;

      localStorage.setItem("access_token", access_token);
      localStorage.setItem("user", JSON.stringify(userData));

      return userData;
    } catch (err) {
      error.value = err.response?.data?.detail || "Ошибка входа";
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const logout = () => {
    authService.logout();
    user.value = null;
    token.value = null;
    error.value = null;
  };

  const initializeAuth = () => {
    const savedUser = localStorage.getItem("user");
    const savedToken = localStorage.getItem("access_token");

    if (savedToken && savedUser) {
      try {
        token.value = savedToken;
        user.value = JSON.parse(savedUser);
      } catch (err) {
        console.error("Error initializing auth:", err);
        localStorage.removeItem("user");
        localStorage.removeItem("access_token");
      }
    }
  };

  const clearError = () => {
    error.value = null;
  };

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    isAdmin,
    register,
    login,
    logout,
    initializeAuth,
    clearError,
  };
});
