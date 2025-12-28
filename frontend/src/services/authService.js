// frontend/src/services/authService.js
import api from "./api";

/**
 * Auth сервис — всё что связано с авторизацией
 */

const authService = {
  /**
   * Регистрация нового пользователя
   */
  async register(username, email, password) {
    try {
      const { data } = await api.post("/auth/register", {
        username,
        email,
        password,
      });
      return data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Вход пользователя
   */
  async login(username, password) {
    try {
      if (!username || !password) {
        throw new Error("Username and password are required");
      }

      console.log("Sending login request:", { username, password });

      const { data } = await api.post("/auth/login", {
        username,
        password,
      });

      console.log("Login response:", data);
      return data;
    } catch (error) {
      console.error("Login service error:", error);
      throw error;
    }
  },

  /**
   * Выход из аккаунта
   */
  logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
  },

  /**
   * Получить текущего пользователя из localStorage
   */
  getCurrentUser() {
    const userStr = localStorage.getItem("user");
    return userStr ? JSON.parse(userStr) : null;
  },

  /**
   * Проверить, есть ли валидный токен
   */
  isAuthenticated() {
    return !!localStorage.getItem("access_token");
  },
};

export default authService;
