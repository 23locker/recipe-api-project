<template>
    <nav class="bg-white shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Логотип/название -->
                <RouterLink to="/recipes" class="flex items-center">
                    <h1 class="text-2xl font-bold text-blue-600">
                        🍳 Recipe App
                    </h1>
                </RouterLink>

                <!-- Навигация + пользователь -->
                <div class="flex items-center gap-6">
                    <!-- Username -->
                    <span class="text-gray-700">
                        {{ authStore.user?.username }}
                    </span>

                    <!-- Logout button -->
                    <button
                        @click="handleLogout"
                        class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                    >
                        Выход
                    </button>
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
