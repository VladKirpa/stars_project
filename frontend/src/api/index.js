import axios from 'axios';

const API_URL = '/api';

export const fetchUserProfile = async (tgId) => {
    try {
        const response = await axios.get(`${API_URL}/user/${tgId}`);
        return response.data;
    } catch (error) {
        console.error("Ошибка при получении профиля:", error);
        throw error;
    }
};