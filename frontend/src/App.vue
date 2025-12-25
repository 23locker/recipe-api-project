<template>
    <div id="app" class="min-h-screen bg-gray-50">
        <!-- Navbar (будет создана позже) -->
        <Navbar v-if="authStore.isAuthenticated" />

        <!-- Main content (RouterView показывает текущую страницу) -->
        <main>
            <RouterView />
        </main>
    </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/authStore";
import Navbar from "@/components/layout/Navbar.vue";

/**
 * App.vue — корневой компонент приложения
 *
 * Здесь:
 * - Инициализируем авторизацию
 * - Показываем Navbar (если авторизован)
 * - RouterView показывает текущую страницу
 */

const authStore = useAuthStore();

/**
 * При загрузке приложения восстанавливаем пользователя из localStorage
 */
onMounted(() => {
    authStore.initializeAuth();
});
</script>

<style scoped>
/* Специфичные стили для App компонента */
</style>
