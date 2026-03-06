import React from 'react';
import { X, ShieldCheck, Clock, AlertTriangle, CheckCircle2 } from 'lucide-react';

const HoldInfoModal = ({ isOpen, onClose }) => {
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
                        background: 'rgba(125, 211, 252, 0.1)', width: '64px', height: '64px', 
                        borderRadius: '20px', display: 'flex', alignItems: 'center', 
                        justifyContent: 'center', margin: '0 auto 16px', color: '#7dd3fc' 
                    }}>
                        <Clock size={32} />
                    </div>
                    <h2 style={{ margin: 0, fontSize: '24px' }}>Система заморозки</h2>
                    <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '8px' }}>
                        Как работает холд баланса
                    </p>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    
                    {/* Блок 1: Зачем это нужно */}
                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: '#7dd3fc' }}><ShieldCheck size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b>Защита рекламодателей:</b> Холд нужен для того, чтобы убедиться, что вы реально подписались на канал, а не просто нажали кнопку.
                        </div>
                    </div>

                    {/* Блок 2: Срок заморозки */}
                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: 'var(--accent-gold)' }}><Clock size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b>Срок 3 дня:</b> После выполнения задания звезды попадают в «Холд» на <b>72 часа</b>. По истечении этого времени они автоматически перейдут в «Доступно».
                        </div>
                    </div>

                    {/* Блок 3: Правило отписки */}
                    <div style={{ background: 'rgba(255, 59, 48, 0.1)', border: '1px solid rgba(255, 59, 48, 0.2)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: '#ff3b30' }}><AlertTriangle size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b>Важно:</b> Если вы отпишетесь от канала, пока деньги в холде — <b>выплата будет аннулирована</b>, а на ваш аккаунт будет начислен страйк.
                        </div>
                    </div>

                    {/* Блок 4: Страйки */}
                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: '#34c759' }}><CheckCircle2 size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b>Система страйков:</b> Отписка от любого рекламного канала (даже после разморозки) дает 1 страйк. <b>5 страйков = вечный бан</b> без возможности вывода средств.
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
                    <CheckCircle2 size={20} /> Понятно
                </button>
            </div>
        </div>
    );
};

export default HoldInfoModal;


