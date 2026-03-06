import React from 'react';
import { X, Megaphone, ShieldAlert, Coins, Repeat, Info } from 'lucide-react';

const AdBalanceInfoModal = ({ isOpen, onClose }) => {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay fade-in" style={{
            position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
            background: 'rgba(0,0,0,0.85)', zIndex: 9999,
            display: 'flex', alignItems: 'flex-end', justifyContent: 'center'
        }}>
            <div className="modal-content slide-up" style={{
                background: 'var(--bg-primary)', width: '100%', maxWidth: '500px',
                borderTopLeftRadius: '24px', borderTopRightRadius: '24px',
                padding: '24px', position: 'relative', borderTop: '1px solid var(--border-color)',
                maxHeight: '90vh', overflowY: 'auto'
            }}>
                {/* Кнопка закрытия */}
                <button onClick={onClose} style={{
                    position: 'absolute', top: '16px', right: '16px', 
                    background: 'rgba(255, 255, 255, 0.1)', border: '1px solid rgba(255, 255, 255, 0.2)', 
                    borderRadius: '50%', width: '36px', height: '36px', 
                    display: 'flex', alignItems: 'center', justifyContent: 'center', 
                    color: '#ffffff', fontSize: '18px', fontWeight: 'bold', cursor: 'pointer', zIndex: 10
                }}>
                    ✕
                </button>

                <div style={{ textAlign: 'center', marginBottom: '24px' }}>
                    <div style={{ 
                        background: 'rgba(52, 199, 89, 0.1)', width: '64px', height: '64px', 
                        borderRadius: '20px', display: 'flex', alignItems: 'center', 
                        justifyContent: 'center', margin: '0 auto 16px', color: '#34c759' 
                    }}>
                        <Megaphone size={32} />
                    </div>
                    <h2 style={{ margin: 0, fontSize: '24px' }}>Рекламный баланс</h2>
                    <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '8px' }}>
                        Особенности рекламного счета
                    </p>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    
                    {/* Блок 1: Назначение */}
                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: '#34c759' }}><Megaphone size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b>Только для рекламы:</b> Этот баланс предназначен исключительно для создания заданий и продвижения ваших ресурсов в системе.
                        </div>
                    </div>

                    {/* Блок 2: Ограничения */}
                    <div style={{ background: 'rgba(255, 59, 48, 0.1)', border: '1px solid rgba(255, 59, 48, 0.2)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: '#ff3b30' }}><ShieldAlert size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b>Без вывода:</b> Рекламный баланс невозможно вывести на карту/кошелек или обменять на «Доступные» звезды.
                        </div>
                    </div>

                    {/* Блок 3: Пополнение */}
                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: 'var(--accent-gold)' }}><Coins size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b>Как пополнить:</b> Пополнение происходит через администратора или с помощью криптовалют. Заработанные звезды перевести сюда нельзя.
                        </div>
                    </div>

                    {/* Блок 4: Разделение счетов */}
                    <div style={{ background: 'rgba(125, 211, 252, 0.1)', border: '1px solid rgba(125, 211, 252, 0.2)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: '#7dd3fc' }}><Repeat size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b>Разные балансы:</b> Доступный баланс (для вывода) и Рекламный баланс — это два независимых счета.
                        </div>
                    </div>
                </div>

                <button 
                    className="action-btn-main" 
                    onClick={onClose}
                    style={{ 
                        marginTop: '32px', width: '100%', padding: '16px', 
                        borderRadius: '16px', fontSize: '16px', fontWeight: 'bold',
                        display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px'
                    }}
                >
                    <Info size={20} /> Понятно
                </button>
            </div>
        </div>
    );
};

export default AdBalanceInfoModal;