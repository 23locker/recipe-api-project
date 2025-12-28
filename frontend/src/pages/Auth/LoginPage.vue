<template>
    <div class="min-h-screen relative flex items-center justify-center bg-[#0f172a] overflow-hidden">
        <!-- Анимированный фон -->
        <div class="absolute inset-0 z-0">
            <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-emerald-500/20 blur-[120px] rounded-full animate-pulse"></div>
            <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-600/20 blur-[120px] rounded-full animate-pulse" style="animation-delay: 2s"></div>
        </div>

        <div class="w-full max-w-md relative z-10 px-4">
            <!-- Glass Card -->
            <div class="bg-white/5 backdrop-blur-2xl rounded-[2.5rem] border border-white/10 p-10 shadow-2xl overflow-hidden group">
                <!-- Декоративные элементы -->
                <div class="absolute top-0 right-0 w-32 h-32 bg-white/5 -rotate-45 translate-x-16 -translate-y-16 group-hover:bg-white/10 transition-colors"></div>
                
                <div class="text-center mb-10">
                    <div class="w-16 h-16 bg-gradient-to-tr from-emerald-500 to-green-600 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-6 shadow-lg shadow-emerald-500/20">
                        🍳
                    </div>
                    <h1 class="text-4xl font-black text-white tracking-tight mb-2">Recipe<span class="text-emerald-500">App</span></h1>
                    <p class="text-slate-400 font-medium">Ваш личный шеф-повар в кармане</p>
                </div>

                <div v-if="authStore.error" class="mb-8 p-4 bg-red-500/10 border border-red-500/20 rounded-2xl text-red-400 text-sm flex items-center gap-3">
                    <span class="text-lg">⚠️</span> {{ authStore.error }}
                </div>

                <form @submit.prevent="handleLogin" class="space-y-6">
                    <div class="space-y-2">
                        <label class="block text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] ml-2">Имя пользователя</label>
                        <div class="relative">
                            <input v-model="formData.username" type="text" placeholder="chef_master" required class="w-full px-6 py-4 bg-white/5 border border-white/10 focus:border-emerald-500/50 focus:bg-white/10 rounded-2xl text-white placeholder-slate-600 outline-none transition-all font-bold" />
                        </div>
                    </div>

                    <div class="space-y-2">
                        <label class="block text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] ml-2">Пароль</label>
                        <div class="relative">
                            <input v-model="formData.password" type="password" placeholder="••••••••" required class="w-full px-6 py-4 bg-white/5 border border-white/10 focus:border-emerald-500/50 focus:bg-white/10 rounded-2xl text-white placeholder-slate-600 outline-none transition-all font-mono" />
                        </div>
                    </div>

                    <button type="submit" :disabled="authStore.isLoading" class="w-full py-4 bg-gradient-to-r from-emerald-600 to-green-500 hover:from-emerald-500 hover:to-green-400 text-white font-black rounded-2xl transition-all active:scale-[0.98] shadow-xl shadow-emerald-600/20 disabled:opacity-50 flex items-center justify-center gap-3 text-lg">
                        <svg v-if="authStore.isLoading" class="animate-spin h-5 w-5" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                        {{ authStore.isLoading ? "Входим..." : "Начать готовить" }}
                    </button>
                </form>

                <div class="mt-10 pt-8 border-t border-white/5 text-center">
                    <p class="text-slate-500 font-medium">
                        Новичок в RecipeApp?
                        <RouterLink to="/register" class="text-emerald-500 font-bold hover:text-emerald-400 ml-1 transition-colors underline underline-offset-4">Присоединиться</RouterLink>
                    </p>
                </div>

                <!-- Тестовые данные (чуть менее броско) -->
                <div class="mt-8 p-6 bg-emerald-500/5 rounded-3xl border border-emerald-500/10 opacity-60 hover:opacity-100 transition-opacity">
                    <div class="text-[9px] font-black text-emerald-500 uppercase tracking-widest mb-2">Демонстрационный доступ</div>
                    <div class="flex justify-between items-center text-xs text-slate-400">
                        <span>L: <code class="text-emerald-400/80">testuser</code></span>
                        <span>P: <code class="text-emerald-400/80">password</code></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/authStore";

const router = useRouter();
const authStore = useAuthStore();

const formData = reactive({
    username: "",
    password: "",
});

const handleLogin = async () => {
    authStore.clearError();

    if (!formData.username.trim() || !formData.password.trim()) {
        return;
    }

    try {
        await authStore.login(formData.username, formData.password);

        router.push("/recipes");
    } catch (error) {
        console.error("Login error:", error);
    }
};
</script>

<style scoped></style>
