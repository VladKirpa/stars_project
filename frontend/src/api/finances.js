import axios from 'axios';

const getUserId = () => {
    
    return String(window.Telegram?.WebApp?.initDataUnsafe?.user?.id);
};

export const createWithdrawRequest = async (amount) => {
    const userId = getUserId();
    
    const response = await axios.post('/api/finances/withdraw', 
        { amount: parseInt(amount, 10) },
        { headers: { 'x-user-id': userId } }
    );
    return response.data;
};

export const getWithdrawHistory = async () => {
    const userId = getUserId();
    const response = await axios.get('/api/finances/withdraw/history', 
        { headers: { 'x-user-id': userId } }
    );
    return response.data;
};