import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/authStore";

const LoginPage = () => import("@/pages/Auth/LoginPage.vue");
const RegisterPage = () => import("@/pages/Auth/RegisterPage.vue");
const RecipesPage = () => import("@/pages/RecipesPage.vue");
const RecipeDetailPage = () => import("@/pages/RecipeDetailPage.vue");
const NotFoundPage = () => import("@/pages/NotFoundPage.vue");

const routes = [
  {
    path: "/",
    redirect: "/recipes",
  },

  {
    path: "/login",
    name: "Login",
    component: LoginPage,
    meta: {
      requiresAuth: false,
    },
  },

  {
    path: "/register",
    name: "Register",
    component: RegisterPage,
    meta: {
      requiresAuth: false,
    },
  },

  {
    path: "/recipes",
    component: "Recipes",
    component: RecipesPage,
    meta: {
      requiresAuth: true,
    },
  },

  {
    path: "/recipes/:id",
    name: "RecipeDetail",
    component: RecipeDetailPage,
    meta: {
      requiresAuth: true,
    },
  },

  {
    path: "/:pathMatch(.*)*",
    component: NotFoundPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/login");
    return;
  }

  if (
    (to.path === "/login" || to.path === "/register") &&
    authStore.isAuthenticated
  ) {
    next("/recipes");
    return;
  }

  next();
});

export default router;
