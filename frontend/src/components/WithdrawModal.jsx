import { useState } from 'react';
import { createWithdrawRequest } from '../api/finances';
import { useTelegram } from '../hooks/useTelegram';
import { Rocket, AlertCircle, Loader2 } from 'lucide-react';

const WithdrawModal = ({ isOpen, onClose, userBalance, onSuccess }) => {
    const { tg, triggerVibration } = useTelegram();
    const [amount, setAmount] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    if (!isOpen) return null;

    const parsedAmount = parseInt(amount);
    const isValid = Number.isInteger(parsedAmount) && parsedAmount >= 25 && parsedAmount <= parseFloat(userBalance || 0);

    const handleSubmit = async () => {
        if (!isValid || loading) return; // Защита от двойного клика
        
        setError('');
        setLoading(true);
        triggerVibration('heavy');

        try {
            await createWithdrawRequest(parsedAmount);
            triggerVibration('heavy');
            
            if (tg?.showAlert) {
                tg.showAlert('🚀 Заявка успешно создана! Ожидайте зачисления в течение дня.', () => {
                    onSuccess(parsedAmount);
                    setAmount('');
                    onClose();
                });
            } else {
                alert('🚀 Заявка успешно создана!');
                onSuccess(parsedAmount);
                setAmount('');
                onClose();
            }
        } catch (err) {
            console.error("Полная ошибка вывода:", err);
            triggerVibration('error');
            
            // Расширенный поиск причины ошибки
            const errMsg = err.response?.data?.detail 
                || err.response?.data?.message 
                || err.message 
                || "Скрытая ошибка (Смотри консоль браузера)";
                
            setError(`Детали: ${errMsg}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay fade-in" style={{
            position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
            background: 'rgba(0,0,0,0.8)', zIndex: 9999,
            display: 'flex', alignItems: 'flex-end', justifyContent: 'center'
        }}>
            <div className="modal-content slide-up" style={{
                background: 'var(--bg-primary)', width: '100%', maxWidth: '500px',
                borderTopLeftRadius: '24px', borderTopRightRadius: '24px',
                padding: '24px', position: 'relative', borderTop: '1px solid var(--border-color)'
            }}>
                {/* крестик текстовый символ */}
                <button onClick={onClose} style={{
                    position: 'absolute', top: '16px', right: '16px', 
                    background: 'rgba(255, 255, 255, 0.15)', border: '1px solid rgba(255, 255, 255, 0.3)', 
                    borderRadius: '50%', width: '34px', height: '34px', 
                    display: 'flex', alignItems: 'center', justifyContent: 'center', 
                    color: '#ffffff', fontSize: '18px', fontWeight: 'bold', cursor: 'pointer', zIndex: 10
                }}>
                    ✕
                </button>

                <h2 style={{margin: '0 0 16px 0', fontSize: '22px'}}>Вывод средств</h2>

                <div style={{
                    background: 'rgba(52, 199, 89, 0.1)', border: '1px solid rgba(52, 199, 89, 0.3)', 
                    borderRadius: '12px', padding: '12px', marginBottom: '12px'
                }}>
                    <p style={{color: '#34c759', fontSize: '13px', margin: 0, display: 'flex', gap: '8px', alignItems: 'center'}}>
                        <span style={{fontSize: '16px'}}>⏱</span> Ваша заявка будет рассмотрена и одобрена в течении рабочего дня.
                    </p>
                </div>

                <div style={{
                    background: 'rgba(255, 59, 48, 0.1)', border: '1px solid rgba(255, 59, 48, 0.3)', 
                    borderRadius: '12px', padding: '12px', marginBottom: '20px'
                }}>
                    <p style={{color: '#ff3b30', fontSize: '13px', margin: 0, display: 'flex', gap: '8px', alignItems: 'flex-start'}}>
                        <AlertCircle size={18} style={{flexShrink: 0, marginTop: '2px'}} /> 
                        <span><b>Обязательно:</b> Установите публичный @username в настройках Telegram, иначе мы не сможем перевести вам звезды!</span>
                    </p>
                </div>

                <div className="b-box primary" style={{ marginBottom: '20px', padding: '12px' }}>
                    <span className="b-label" style={{ color: 'rgba(255,255,255,0.8)' }}>Доступно для вывода</span>
                    <div className="b-val" style={{ fontSize: '24px', margin: 0 }}>
                        {parseFloat(userBalance || 0).toFixed(2)} <span>⭐️</span>
                    </div>
                </div>

                <div className="input-group">
                    <label style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>
                        Сумма (Минимум 25)
                    </label>
                    <input 
                        type="number" 
                        placeholder="25" 
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="styled-input"
                        style={{ width: '100%', padding: '16px', borderRadius: '16px', fontSize: '20px', textAlign: 'center' }}
                    />
                </div>

                {error && (
                    <div style={{ color: '#ff453a', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '6px', marginTop: '12px', justifyContent: 'center', textAlign: 'center' }}>
                        <AlertCircle size={16} style={{flexShrink: 0}} /> 
                        <span>{error}</span>
                    </div>
                )}

                <button 
                    className="action-btn-main" 
                    onClick={handleSubmit}
                    disabled={!isValid || loading}
                    style={{ 
                        marginTop: '24px', width: '100%', padding: '16px', borderRadius: '16px',
                        opacity: isValid ? 1 : 0.5, transition: 'all 0.3s'
                    }}
                >
                    {loading ? <Loader2 className="loader-spin" size={24}/> : (
                        <span style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', fontSize: '18px'}}>
                            <Rocket size={20} /> Вывести {parsedAmount || 0} ⭐️
                        </span>
                    )}
                </button>
            </div>
        </div>
    );
};

export default WithdrawModal;