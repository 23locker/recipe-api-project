import api from "./api";

export const authService = {
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
  async login(username, password) {
    try {
      const { data } = await api.post("/auth/login", {
        username,
        password,
      });
      return data;
    } catch (error) {
      throw error;
    }
  },
  logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
  },
  getCurrentUser() {
    const userStr = localStorage.getItem("user");
    return userStr ? JSON.parse(userStr) : null;
  },
  isAuthenticated() {
    return !!localStorage.getItem("access_token");
  },
};
