<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50">
        <div class="text-center">
            <h1 class="text-5xl font-bold mb-4">404</h1>
            <p class="text-xl text-gray-600 mb-8">Страница не найдена</p>
            <RouterLink
                to="/recipes"
                class="inline-block px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
                Вернуться на главную
            </RouterLink>
        </div>
    </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>
