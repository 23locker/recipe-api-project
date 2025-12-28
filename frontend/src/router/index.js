import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/authStore";

const LoginPage = () => import("@/pages/Auth/LoginPage.vue");
const RegisterPage = () => import("@/pages/Auth/RegisterPage.vue");
const RecipesPage = () => import("@/pages/RecipesPage.vue");
const RecipeDetailPage = () => import("@/pages/RecipeDetailPage.vue");
const AdminPage = () => import("@/pages/AdminPage.vue");
const IngredientsManagementPage = () => import("@/pages/IngredientsManagementPage.vue");
const CategoriesManagementPage = () => import("@/pages/CategoriesManagementPage.vue");
const RecipesManagementPage = () => import("@/pages/RecipesManagementPage.vue");
const RecipeEditPage = () => import("@/pages/RecipeEditPage.vue");
const StoreProductsPage = () => import("@/pages/StoreProductsPage.vue");
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
    name: "Recipes",
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
    path: "/admin",
    name: "Admin",
    component: AdminPage,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    path: "/admin/ingredients",
    name: "IngredientsManagement",
    component: IngredientsManagementPage,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    path: "/admin/categories",
    name: "CategoriesManagement",
    component: CategoriesManagementPage,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    path: "/admin/recipes",
    name: "RecipesManagement",
    component: RecipesManagementPage,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    path: "/admin/recipes/new",
    name: "RecipeCreate",
    component: RecipeEditPage,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    path: "/admin/recipes/edit/:id",
    name: "RecipeEdit",
    component: RecipeEditPage,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    path: "/admin/store-products",
    name: "StoreProducts",
    component: StoreProductsPage,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
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

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next("/recipes");
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
