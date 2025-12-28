import api from "./api";

const adminService = {
    /**
     * Запустить синхронизацию цен магазинов (через RabbitMQ)
     */
    async triggerStoreSync() {
        try {
            const { data } = await api.post("/admin/parse-stores");
            return data;
        } catch (error) {
            console.error("Error triggering store sync:", error);
            throw error;
        }
    },

    /**
     * Получить статистику (для админов)
     */
    async getStats() {
        try {
            const { data } = await api.get("/admin/stats");
            return data;
        } catch (error) {
            console.error("Error fetching stats:", error);
            throw error;
        }
    },
};

export default adminService;
