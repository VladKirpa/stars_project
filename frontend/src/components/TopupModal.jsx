import React from 'react';
import { X, Wallet, CheckCircle2, AlertCircle, MessageSquare } from 'lucide-react';

const TopUpModal = ({ isOpen, onClose }) => {
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
                {/* крестик */}
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
                        <Wallet size={32} />
                    </div>
                    <h2 style={{ margin: 0, fontSize: '24px' }}>Пополнение баланса</h2>
                    <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '8px' }}>
                        Рекламный кабинет
                    </p>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    
                    {/* Блок 1: Инфа про админа */}
                    <div style={{ background: 'rgba(255, 59, 48, 0.1)', border: '1px solid rgba(255, 59, 48, 0.2)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: '#ff3b30' }}><AlertCircle size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b style={{ display: 'block', marginBottom: '4px' }}>Временный режим:</b>
                            На данный момент автоматические платежи в разработке. Пополнение происходит вручную через администратора.
                        </div>
                    </div>

                    {/* Блок 2: Способы оплаты */}
                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '16px', display: 'flex', gap: '12px' }}>
                        <div style={{ color: '#34c759' }}><CheckCircle2 size={20} /></div>
                        <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                            <b style={{ display: 'block', marginBottom: '4px' }}>Любые способы:</b>
                            Доступна оплата Криптовалютой (USDT/TON), Telegram Звездами или переводом на карту.
                        </div>
                    </div>
                </div>

                {/* Кнопка на саппорта */}
                <a 
                    href="https://t.me/managgee" 
                    target="_blank" 
                    rel="noreferrer"
                    onClick={onClose}
                    style={{ 
                        marginTop: '32px', width: '100%', padding: '16px', 
                        borderRadius: '16px', fontSize: '16px', fontWeight: 'bold',
                        display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px',
                        textDecoration: 'none', background: '#ffffff', color: '#000000'
                    }}
                >
                    <MessageSquare size={20} /> Написать администратору
                </a>
            </div>
        </div>
    );
};

export default TopUpModal;