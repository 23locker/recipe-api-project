<template>
    <div class="container mx-auto px-4 py-8 max-w-4xl">
        <div class="mb-8">
            <router-link
                to="/recipes"
                class="text-green-600 hover:text-green-700 font-medium flex items-center gap-1 mb-4 transition-transform hover:-translate-x-1 inline-flex"
            >
                ← Назад к рецептам
            </router-link>
            <h1 class="text-4xl font-black text-gray-900">Админ-панель</h1>
            <p class="text-gray-500 mt-2">
                Управление фоновыми задачами и синхронизацией данных
            </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Store Sync Card -->
            <div
                class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col h-full ring-1 ring-gray-100/50"
            >
                <div class="mb-6">
                    <div
                        class="w-14 h-14 bg-orange-50 rounded-2xl flex items-center justify-center text-3xl mb-4"
                    >
                        🛒
                    </div>
                    <h2 class="text-2xl font-bold text-gray-800 mb-2">
                        Синхронизация цен
                    </h2>
                    <p class="text-gray-600 text-sm">
                        Задача будет отправлена в RabbitMQ и обработана в
                        фоновом режиме.
                    </p>
                </div>

                <div class="mt-auto space-y-3">
                    <router-link
                        to="/admin/store-products"
                        class="w-full bg-orange-100 hover:bg-orange-200 text-orange-700 font-bold py-3 px-6 rounded-2xl transition-all block text-center"
                    >
                        👁️ Посмотреть товары
                    </router-link>
                    <button
                        @click="triggerSync"
                        :disabled="isLoading"
                        class="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 px-6 rounded-2xl transition-all shadow-lg shadow-orange-100 active:scale-95 disabled:opacity-50"
                    >
                        {{
                            isLoading ? "Запускаем..." : "Запустить обновление"
                        }}
                    </button>
                </div>

                <div
                    v-if="message"
                    class="mt-4 p-4 rounded-xl text-sm"
                    :class="
                        isError
                            ? 'bg-red-50 text-red-600 border border-red-100'
                            : 'bg-emerald-50 text-emerald-600 border border-emerald-100'
                    "
                >
                    {{ message }}
                </div>
            </div>

            <!-- Ingredient Management Card -->
            <div
                class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col h-full ring-1 ring-gray-100/50"
            >
                <div class="mb-6">
                    <div
                        class="w-14 h-14 bg-green-50 rounded-2xl flex items-center justify-center text-3xl mb-4"
                    >
                        🥦
                    </div>
                    <h2 class="text-2xl font-bold text-gray-800 mb-2">
                        Ингредиенты
                    </h2>
                    <p class="text-gray-600 text-sm">
                        Управление глобальной базой ингредиентов, настройка КБЖУ
                        и категорий.
                    </p>
                </div>
                <div class="mt-auto">
                    <router-link
                        to="/admin/ingredients"
                        class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-6 rounded-2xl transition-all shadow-lg shadow-green-100 active:scale-95 block text-center"
                    >
                        Управление списком
                    </router-link>
                </div>
            </div>

            <!-- Recipes Management Card -->
            <div
                class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col h-full ring-1 ring-gray-100/50"
            >
                <div class="mb-6">
                    <div
                        class="w-14 h-14 bg-indigo-50 rounded-2xl flex items-center justify-center text-3xl mb-4"
                    >
                        📖
                    </div>
                    <h2 class="text-2xl font-bold text-gray-800 mb-2">
                        Рецепты
                    </h2>
                    <p class="text-gray-600 text-sm">
                        Редактирование существующих рецептов и добавление новых
                        кулинарных шедевров.
                    </p>
                </div>
                <div class="mt-auto">
                    <router-link
                        to="/admin/recipes"
                        class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-6 rounded-2xl transition-all shadow-lg shadow-indigo-100 active:scale-95 block text-center"
                    >
                        Управление рецептами
                    </router-link>
                </div>
            </div>

            <!-- Categories Management Card -->
            <div
                class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col h-full ring-1 ring-gray-100/50"
            >
                <div class="mb-6">
                    <div
                        class="w-14 h-14 bg-purple-50 rounded-2xl flex items-center justify-center text-3xl mb-4"
                    >
                        📂
                    </div>
                    <h2 class="text-2xl font-bold text-gray-800 mb-2">
                        Категории
                    </h2>
                    <p class="text-gray-600 text-sm">
                        Управление иерархией категорий для удобного поиска
                        рецептов.
                    </p>
                </div>
                <div class="mt-auto">
                    <router-link
                        to="/admin/categories"
                        class="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 px-6 rounded-2xl transition-all shadow-lg shadow-purple-100 active:scale-95 block text-center"
                    >
                        Управление категориями
                    </router-link>
                </div>
            </div>

            <!-- Stats Card (Placeholder) -->
            <div
                class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col h-full ring-1 ring-gray-100/50 opacity-60"
            >
                <div class="mb-6">
                    <div
                        class="w-14 h-14 bg-indigo-50 rounded-2xl flex items-center justify-center text-3xl mb-4"
                    >
                        📊
                    </div>
                    <h2 class="text-2xl font-bold text-gray-800 mb-2">
                        Статистика
                    </h2>
                    <p class="text-gray-600 text-sm">
                        Просмотр активности пользователей и самых популярных
                        рецептов.
                    </p>
                </div>

                <div class="mt-auto">
                    <button
                        disabled
                        class="w-full bg-indigo-100 text-indigo-400 font-bold py-4 px-6 rounded-2xl cursor-not-allowed"
                    >
                        В разработке
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import adminService from "@/services/adminService";

const isLoading = ref(false);
const message = ref("");
const isError = ref(false);

const triggerSync = async () => {
    isLoading.value = true;
    message.value = "";
    isError.value = false;

    try {
        const response = await adminService.triggerStoreSync();
        message.value =
            response.message || "Задача успешно добавлена в очередь!";
    } catch (err) {
        isError.value = true;
        message.value =
            "Ошибка при запуске задачи. Проверьте соединение с сервером.";
    } finally {
        isLoading.value = false;
    }
};
</script>
