<template>
    <nav class="bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-20">
                <!-- Логотип/название -->
                <RouterLink to="/recipes" class="flex items-center group">
                    <div class="w-10 h-10 bg-green-600 rounded-xl flex items-center justify-center text-xl shadow-lg shadow-green-100 mr-3 group-hover:rotate-12 transition-transform">
                        🍳
                    </div>
                    <h1 class="text-2xl font-black text-gray-900 tracking-tight">
                        Recipe<span class="text-green-600">App</span>
                    </h1>
                </RouterLink>

                <!-- Навигация -->
                <div class="hidden md:flex items-center gap-8">
                    <RouterLink 
                        to="/recipes" 
                        class="text-sm font-bold transition-all"
                        :class="router.currentRoute.value.path === '/recipes' ? 'text-green-600' : 'text-gray-500 hover:text-green-600'"
                    >
                        Рецепты
                    </RouterLink>
                    
                    <RouterLink 
                        v-if="authStore.isAdmin" 
                        to="/admin/ingredients" 
                        class="text-sm font-bold transition-all"
                         :class="router.currentRoute.value.path === '/admin/ingredients' ? 'text-green-600' : 'text-gray-500 hover:text-green-600'"
                    >
                        Ингредиенты
                    </RouterLink>

                    <RouterLink 
                        v-if="authStore.isAdmin" 
                        to="/admin/categories" 
                        class="text-sm font-bold transition-all"
                         :class="router.currentRoute.value.path === '/admin/categories' ? 'text-green-600' : 'text-gray-500 hover:text-green-600'"
                    >
                        Категории
                    </RouterLink>

                    <RouterLink 
                        v-if="authStore.isAdmin" 
                        to="/admin" 
                        class="text-sm font-bold transition-all"
                         :class="router.currentRoute.value.path === '/admin' ? 'text-green-600' : 'text-gray-500 hover:text-green-600'"
                    >
                        Админка
                    </RouterLink>

                    <RouterLink 
                        v-if="authStore.isAdmin" 
                        to="/admin/recipes/new" 
                        class="bg-green-600 hover:bg-green-700 text-white px-5 py-2.5 rounded-xl text-sm font-bold transition-all shadow-lg shadow-green-100 flex items-center gap-2 active:scale-95 ml-4"
                    >
                        <span>➕</span> Создать
                    </RouterLink>
                </div>

                <!-- Пользователь -->
                <div class="flex items-center gap-4">
                    <div class="h-6 w-px bg-gray-100 mx-2 hidden md:block"></div>

                    <!-- Username -->
                    <div class="flex items-center gap-3">
                        <div class="text-right hidden sm:block">
                            <div class="text-sm font-bold text-gray-900">{{ authStore.user?.username }}</div>
                            <div class="text-[10px] text-gray-400 uppercase font-black tracking-widest">{{ authStore.user?.role }}</div>
                        </div>
                        <button
                            @click="handleLogout"
                            class="p-2.5 bg-gray-50 text-gray-400 rounded-xl hover:bg-orange-50 hover:text-orange-600 transition-all active:scale-95"
                            title="Выход"
                        >
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/authStore";

/**
 * Navbar компонент
 *
 * Показывается только если пользователь авторизован
 * Содержит: навигацию, имя пользователя, кнопку выхода
 */

const router = useRouter();
const authStore = useAuthStore();

/**
 * Обработчик выхода
 */
const handleLogout = () => {
    authStore.logout();
    router.push("/login");
};
</script>

<style scoped>
/* Стили для navbar */
</style>
