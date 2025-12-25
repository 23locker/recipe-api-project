<template>
    <div
        class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4"
    >
        <div class="w-full max-w-md">
            <!-- Карточка логина -->
            <div class="bg-white rounded-lg shadow-xl p-8">
                <!-- Заголовок -->
                <div class="text-center mb-8">
                    <h1 class="text-4xl font-bold text-blue-600 mb-2">🍳</h1>
                    <h2 class="text-3xl font-bold text-gray-900">Recipe App</h2>
                    <p class="text-gray-600 mt-2">Добро пожаловать!</p>
                </div>

                <!-- Сообщение об ошибке -->
                <div
                    v-if="authStore.error"
                    class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
                >
                    {{ authStore.error }}
                </div>

                <!-- Форма логина -->
                <form @submit.prevent="handleLogin" class="space-y-5">
                    <!-- Username -->
                    <div>
                        <label
                            for="username"
                            class="block text-sm font-medium text-gray-700 mb-2"
                        >
                            Имя пользователя
                        </label>
                        <input
                            id="username"
                            v-model="formData.username"
                            type="text"
                            placeholder="Введите имя пользователя"
                            required
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                        />
                    </div>

                    <!-- Password -->
                    <div>
                        <label
                            for="password"
                            class="block text-sm font-medium text-gray-700 mb-2"
                        >
                            Пароль
                        </label>
                        <input
                            id="password"
                            v-model="formData.password"
                            type="password"
                            placeholder="Введите пароль"
                            required
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                        />
                    </div>

                    <!-- Submit Button -->
                    <button
                        type="submit"
                        :disabled="authStore.isLoading"
                        class="w-full py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                        <!-- Спиннер при загрузке -->
                        <svg
                            v-if="authStore.isLoading"
                            class="animate-spin h-5 w-5"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                        >
                            <circle
                                class="opacity-25"
                                cx="12"
                                cy="12"
                                r="10"
                                stroke="currentColor"
                                stroke-width="4"
                            />
                            <path
                                class="opacity-75"
                                fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                            />
                        </svg>
                        <span>{{
                            authStore.isLoading ? "Загрузка..." : "Вход"
                        }}</span>
                    </button>
                </form>

                <!-- Ссылка на регистрацию -->
                <div class="mt-6 text-center">
                    <p class="text-gray-600">
                        Нет аккаунта?
                        <RouterLink
                            to="/register"
                            class="text-blue-600 font-semibold hover:text-blue-700 transition-colors"
                        >
                            Зарегистрируйтесь
                        </RouterLink>
                    </p>
                </div>

                <!-- Demo credentials (для тестирования) -->
                <div
                    class="mt-6 p-4 bg-blue-50 rounded-lg text-sm text-gray-700"
                >
                    <p class="font-semibold mb-2">
                        📝 Тестовые учетные данные:
                    </p>
                    <p>
                        Username:
                        <code class="bg-white px-2 py-1 rounded">testuser</code>
                    </p>
                    <p>
                        Password:
                        <code class="bg-white px-2 py-1 rounded">password</code>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/authStore";

/**
 * LoginPage компонент
 *
 * Это страница логина с:
 * - Формой с username и password
 * - Валидацией
 * - Обработкой ошибок
 * - Спиннером при загрузке
 * - Ссылкой на регистрацию
 */

const router = useRouter();
const authStore = useAuthStore();

// Состояние формы
const formData = reactive({
    username: "",
    password: "",
});

/**
 * Обработчик отправки формы
 *
 * 1. Проверяем, что поля не пусты
 * 2. Вызываем authStore.login()
 * 3. Если успешно - перенаправляем на /recipes
 * 4. Если ошибка - показываем её
 */
const handleLogin = async () => {
    // Очищаем старую ошибку
    authStore.clearError();

    // Проверяем что поля не пусты
    if (!formData.username.trim() || !formData.password.trim()) {
        return;
    }

    try {
        // Отправляем запрос на логин
        await authStore.login(formData.username, formData.password);

        // Если успешно, перенаправляем на список рецептов
        router.push("/recipes");
    } catch (error) {
        // Ошибка уже сохранена в authStore.error
        // и показывается в шаблоне
        console.error("Login error:", error);
    }
};
</script>

<style scoped>
/* Стили для LoginPage */
</style>
