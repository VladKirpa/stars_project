import React from 'react';
import { X, Gift, Users, Zap, CheckCircle2, Info } from 'lucide-react';

const ReferralInfoModal = ({ isOpen, onClose }) => {
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
                        background: 'rgba(226, 183, 20, 0.1)', width: '64px', height: '64px', 
                        borderRadius: '20px', display: 'flex', alignItems: 'center', 
                        justifyContent: 'center', margin: '0 auto 16px', color: 'var(--accent-gold)' 
                    }}>
                        <Gift size={32} />
                    </div>
                    <h2 style={{ margin: 0, fontSize: '24px' }}>Реферальная система</h2>
                    <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '8px' }}>
                        Зарабатывайте вместе с друзьями
                    </p>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    
                    {/* Блок 1: Как пригласить */}
                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: 'var(--accent-gold)' }}><Users size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b>Приглашайте друзей:</b> Копируйте свою уникальную ссылку и отправляйте её друзьям. Каждый, кто перейдет по ней, станет вашим рефералом.
                        </div>
                    </div>

                    {/* Блок 2: Награда */}
                    <div style={{ background: 'rgba(52, 199, 89, 0.1)', border: '1px solid rgba(52, 199, 89, 0.2)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: '#34c759' }}><Zap size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b>Бонус 3 ⭐️:</b> Вы получаете фиксированную награду в размере 3-х звезд за каждого активного приглашенного пользователя.
                        </div>
                    </div>

                    {/* Блок 3: Условие активности */}
                    <div style={{ background: 'rgba(125, 211, 252, 0.1)', border: '1px solid rgba(125, 211, 252, 0.2)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: '#7dd3fc' }}><CheckCircle2 size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b>Условие начисления:</b> Звезды будут зачислены на ваш баланс автоматически только после того, как ваш друг выполнит <b>10 любых заданий</b>.
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

export default ReferralInfoModal;