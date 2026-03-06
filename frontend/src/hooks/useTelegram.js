const tg = window.Telegram.WebApp;

export function useTelegram() {
    const onClose = () => {
        tg.close();
    };

    const triggerVibration = (type = 'heavy') => {
        if (tg.HapticFeedback) {
            tg.HapticFeedback.impactOccurred(type);
        }
    };

    const rawUser = tg.initDataUnsafe?.user;
    const user = rawUser || { 
        id: 1891646344,
        username: 'admin_test', 
        first_name: 'Admin' 
    };

    return {
        onClose,
        triggerVibration,
        tg,
        user,
        queryId: tg.initDataUnsafe?.query_id,
    };
}