<template>
    <div
        class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4"
    >
        <div class="w-full max-w-md">
            <!-- Карточка регистрации -->
            <div class="bg-white rounded-lg shadow-xl p-8">
                <!-- Заголовок -->
                <div class="text-center mb-8">
                    <h1 class="text-4xl font-bold text-blue-600 mb-2">🍳</h1>
                    <h2 class="text-3xl font-bold text-gray-900">Recipe App</h2>
                    <p class="text-gray-600 mt-2">Создайте аккаунт</p>
                </div>

                <!-- Сообщение об ошибке -->
                <div
                    v-if="authStore.error"
                    class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
                >
                    {{ authStore.error }}
                </div>

                <!-- Сообщение об успехе -->
                <div
                    v-if="successMessage"
                    class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
                >
                    {{ successMessage }}
                </div>

                <!-- Форма регистрации -->
                <form @submit.prevent="handleRegister" class="space-y-5">
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
                            minlength="3"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                        />
                        <p class="text-xs text-gray-500 mt-1">
                            Минимум 3 символа
                        </p>
                    </div>

                    <!-- Email -->
                    <div>
                        <label
                            for="email"
                            class="block text-sm font-medium text-gray-700 mb-2"
                        >
                            Email
                        </label>
                        <input
                            id="email"
                            v-model="formData.email"
                            type="email"
                            placeholder="Введите email"
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
                            minlength="6"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                        />
                        <p class="text-xs text-gray-500 mt-1">
                            Минимум 6 символов
                        </p>
                    </div>

                    <!-- Confirm Password -->
                    <div>
                        <label
                            for="confirmPassword"
                            class="block text-sm font-medium text-gray-700 mb-2"
                        >
                            Подтвердите пароль
                        </label>
                        <input
                            id="confirmPassword"
                            v-model="formData.confirmPassword"
                            type="password"
                            placeholder="Подтвердите пароль"
                            required
                            minlength="6"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                        />
                        <!-- Проверка совпадения паролей -->
                        <p
                            v-if="
                                formData.confirmPassword &&
                                formData.password !== formData.confirmPassword
                            "
                            class="text-xs text-red-500 mt-1"
                        >
                            ❌ Пароли не совпадают
                        </p>
                        <p
                            v-else-if="
                                formData.confirmPassword &&
                                formData.password === formData.confirmPassword
                            "
                            class="text-xs text-green-500 mt-1"
                        >
                            ✅ Пароли совпадают
                        </p>
                    </div>

                    <!-- Submit Button -->
                    <button
                        type="submit"
                        :disabled="
                            authStore.isLoading ||
                            formData.password !== formData.confirmPassword
                        "
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
                            authStore.isLoading
                                ? "Загрузка..."
                                : "Зарегистрироваться"
                        }}</span>
                    </button>
                </form>

                <!-- Ссылка на логин -->
                <div class="mt-6 text-center">
                    <p class="text-gray-600">
                        Уже есть аккаунт?
                        <RouterLink
                            to="/login"
                            class="text-blue-600 font-semibold hover:text-blue-700 transition-colors"
                        >
                            Войдите
                        </RouterLink>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/authStore";

/**
 * RegisterPage компонент
 *
 * Это страница регистрации с:
 * - Формой с username, email, password
 * - Подтверждением пароля
 * - Проверкой совпадения паролей (в реальном времени)
 * - Обработкой ошибок
 * - Спиннером при загрузке
 */

const router = useRouter();
const authStore = useAuthStore();
const successMessage = ref("");

// Состояние формы
const formData = reactive({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
});

/**
 * Обработчик отправки формы
 */
const handleRegister = async () => {
    // Очищаем старые сообщения
    authStore.clearError();
    successMessage.value = "";

    // Проверяем что пароли совпадают
    if (formData.password !== formData.confirmPassword) {
        authStore.error = "Пароли не совпадают";
        return;
    }

    // Проверяем что поля не пусты
    if (
        !formData.username.trim() ||
        !formData.email.trim() ||
        !formData.password.trim()
    ) {
        return;
    }

    try {
        // Отправляем запрос на регистрацию
        await authStore.register(
            formData.username,
            formData.email,
            formData.password,
        );

        // Если успешно, показываем сообщение
        successMessage.value = "Регистрация успешна! Переходим на логин...";

        // Через 1.5 секунды перенаправляем на логин
        setTimeout(() => {
            router.push("/login");
        }, 1500);
    } catch (error) {
        // Ошибка уже сохранена в authStore.error
        console.error("Register error:", error);
    }
};
</script>

<style scoped>
/* Стили для RegisterPage */
</style>
