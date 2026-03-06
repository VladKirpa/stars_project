import { useEffect, useState } from 'react';
import axios from 'axios';
import { useTelegram } from '../hooks/useTelegram';
import { Lock, ArrowDownToLine, PlusCircle, Megaphone, CheckCircle2, ShieldAlert, AlertTriangle, Calendar, Link2, Users, Gift, Copy } from 'lucide-react'; 
import WithdrawModal from '../components/WithdrawModal';
import WithdrawHistory from '../components/WithdrawHistory';
import HoldInfoModal from '../components/HoldInfoModal';
import AdBalanceInfoModal from '../components/AdBalanceInfoModal';
import ReferralInfoModal from '../components/ReferralInfoModal';
import TopUpModal from '../components/TopupModal';

const ProfilePage = ({ dbUser }) => {
    const { tg, user, triggerVibration } = useTelegram();
    const [myOrders, setMyOrders] = useState([]);
    const [isWithdrawModalOpen, setIsWithdrawModalOpen] = useState(false);
    const [isHoldModalOpen, setIsHoldModalOpen] = useState(false);
    const [isAdInfoModalOpen, setIsAdInfoModalOpen] = useState(false);
    const [isRefInfoModalOpen, setIsRefInfoModalOpen] = useState(false);
    const [localBalance, setLocalBalance] = useState(0);
    const [isTopUpModalOpen, setIsTopUpModalOpen] = useState(false);

    useEffect(() => {
        if (dbUser?.balance !== undefined) {
            setLocalBalance(parseFloat(dbUser.balance));
        }
    }, [dbUser?.balance]);

    useEffect(() => {
        if (user?.id) {
            axios.get(`/api/get-my-order/${user.id}`)
                .then(res => setMyOrders(res.data))
                .catch(err => console.log("Ошибка загрузки заказов", err));
        }
    }, [user?.id]);

    const handleWithdrawSuccess = (withdrawnAmount) => {
        setLocalBalance(prev => prev - withdrawnAmount);
        window.dispatchEvent(new Event('withdrawalCreated'));
    };

    const handleAction = (type) => {
        triggerVibration('heavy');
        if (type === 'hold_info') setIsHoldModalOpen(true);
        if (type === 'ad_info') setIsAdInfoModalOpen(true);
        if (type === 'ref_info') setIsRefInfoModalOpen(true);
        if (type === 'topup') setIsTopUpModalOpen(true);
    };

    return (
        <div className="fade-in" style={{ paddingBottom: '100px' }}>
            
            {/* Хедер профиля */}
            <div className="profile-header">
                <div className="user-badge">
                    <div className="avatar-placeholder">{user?.first_name?.charAt(0) || 'U'}</div>
                    <div>
                        <div style={{fontWeight: 600, fontSize: '16px'}}>{user?.first_name || 'User'}</div>
                        <div style={{color: 'var(--text-muted)', fontSize: '12px'}}>ID: {user?.id}</div>
                    </div>
                </div>
                <div style={{display: 'flex', flexDirection: 'column', gap: '6px', alignItems: 'flex-end'}}>
                    <div className="stats-pill">
                        <CheckCircle2 size={14} color="#34c759"/>
                        <span>Заданий: {dbUser?.completed_tasks_count || 0}</span>
                    </div>
                    <div className="stats-pill danger">
                        <ShieldAlert size={14} />
                        <span>Страйки: {dbUser?.strikes || 0} / 5</span>
                    </div>
                </div>
            </div>

            {/* Балансы вывода */}
            <div className="balances-grid">
                <div className="b-box primary">
                    <div>
                        <span className="b-label">Доступно</span>
                        <div className="b-val">{localBalance.toFixed(2)} <span>⭐️</span></div>
                    </div>
                    <button className="b-btn" onClick={() => { triggerVibration('heavy'); setIsWithdrawModalOpen(true); }}>
                        <ArrowDownToLine size={16}/> Вывести
                    </button>
                </div>
                <div className="b-box">
                    <div>
                        <span className="b-label"><Lock size={14}/> В холде</span>
                        <div className="b-val" style={{color: '#7dd3fc'}}>{dbUser?.frozen_balance || '0'} <span>❄️</span></div>
                    </div>
                    <button className="b-btn outline" onClick={() => handleAction('hold_info')} style={{opacity: 0.7}}>Инфо</button>
                </div>
            </div>

            <div className="info-banner">
                <div style={{fontSize: '13px'}}><b>Холдинг:</b> Звезды замораживаются на 3 дня.</div>
            </div>
            <div className="info-banner danger" style={{marginBottom: '24px'}}>
                <AlertTriangle size={18} style={{flexShrink: 0}} />
                <div style={{fontSize: '13px'}}><b>Бан:</b> 5 страйков = вечный бан.</div>
            </div>

            {/* рекламный баланс*/}
            <div className="b-box" style={{marginBottom: '24px'}}>
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px'}}>
                    <div>
                        <span className="b-label" style={{marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '8px'}}>
                            <Megaphone size={14}/> Рекламный баланс
                        </span>
                        <div className="b-val" style={{marginBottom: 0}}>
                            {dbUser?.stars_balance || '0'} <span style={{color: '#34c759'}}>💵</span>
                        </div>
                    </div>
                    
                    {/* Кнопка инфо */}
                    <button 
                        onClick={() => handleAction('ad_info')}
                        style={{
                            background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.1)', 
                            borderRadius: '50%', width: '24px', height: '24px', display: 'flex', 
                            alignItems: 'center', justifyContent: 'center', color: '#ffffff', 
                            fontSize: '14px', fontWeight: 'bold', cursor: 'pointer', fontStyle: 'italic',
                            fontFamily: 'serif'
                        }}
                    >
                        i
                    </button>
                </div>
                <button className="b-btn outline" onClick={() => handleAction('topup')}>
                    <PlusCircle size={16}/> Пополнить
                </button>
            </div>

            {/* Рефералка */}
            <div className="task-card-premium fade-in" style={{ marginBottom: '32px', background: 'linear-gradient(145deg, rgba(226, 183, 20, 0.1) 0%, rgba(0,0,0,0.4) 100%)', border: '1px solid rgba(226, 183, 20, 0.2)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div style={{ background: 'rgba(226, 183, 20, 0.2)', padding: '10px', borderRadius: '12px', color: 'var(--accent-gold)' }}><Gift size={24} /></div>
                        <div><h3 style={{ margin: 0, fontSize: '18px', color: '#fff' }}>Рефералы</h3><div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>3 ⭐️ за друга</div></div>
                    </div>
                    <button onClick={() => handleAction('ref_info')} style={{ background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '50%', width: '24px', height: '24px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#ffffff', fontSize: '14px', fontWeight: 'bold', cursor: 'pointer', fontStyle: 'italic', fontFamily: 'serif' }}>i</button>
                </div>

                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                    <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontSize: '13px', color: 'var(--text-muted)' }}>https://t.me/StarvsTakeBot?start={user?.id}</div>
                    <button className="action-btn-main" onClick={() => { triggerVibration('heavy'); navigator.clipboard.writeText(`https://t.me/StarvsTakeBot?start=${user?.id}`); tg.showAlert ? tg.showAlert("Скопировано!") : alert("Скопировано!"); }} style={{ padding: '6px 12px', borderRadius: '8px', flexShrink: 0, display: 'flex', gap: '4px', alignItems: 'center', fontSize: '12px' }}><Copy size={12}/> Копировать</button>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
                    <div style={{ textAlign: 'center', flex: 1, borderRight: '1px solid rgba(255,255,255,0.1)' }}><div style={{ color: 'var(--text-muted)', fontSize: '11px', marginBottom: '4px' }}>Друзей</div><div style={{ fontWeight: 'bold' }}>{dbUser?.referrals_count || 0} 👤</div></div>
                    <div style={{ textAlign: 'center', flex: 1 }}><div style={{ color: 'var(--text-muted)', fontSize: '11px', marginBottom: '4px' }}>Бонус</div><div style={{ fontWeight: 'bold', color: 'var(--accent-gold)' }}>{dbUser?.referral_earned || 0} ⭐️</div></div>
                </div>
            </div>

            <WithdrawHistory />

            {/* Список активных заказов */}
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', paddingLeft: '4px'}}>
                <h3 style={{margin: 0, fontSize: '18px'}}>Мои заказы</h3>
                <span className="stats-pill" style={{border: 'none', background: 'none'}}>Всего: {myOrders.length}</span>
            </div>
            
            {myOrders.length > 0 ? myOrders.map(order => {
                const progressPercent = Math.min((order.current_subs / order.subs_quantity) * 100, 100);
                const createdDate = order.created_at ? new Date(order.created_at).toLocaleDateString('ru-RU', { day: '2-digit', month: 'short' }) : 'Недавно';
                return (
                    <div key={order.id} className="task-card-premium fade-in" style={{ marginBottom: '12px', padding: '16px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                            <div><div style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '4px' }}>{createdDate} • ID: #{order.id}</div><div style={{ fontSize: '14px', fontWeight: 'bold', display: 'flex', gap: '6px', alignItems: 'center' }}><Link2 size={14} color="var(--accent-gold)" />{order.channel_id.replace('https://t.me/', '').replace('@', '')}</div></div>
                            <div style={{ fontSize: '10px', fontWeight: '800', textTransform: 'uppercase', background: order.status === 'pending' ? 'rgba(226, 183, 20, 0.1)' : 'rgba(52, 199, 89, 0.1)', color: order.status === 'pending' ? 'var(--accent-gold)' : '#34c759', padding: '4px 8px', borderRadius: '6px' }}>{order.status === 'pending' ? 'В работе' : 'Готово'}</div>
                        </div>
                        <div style={{ marginBottom: '12px' }}><div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', marginBottom: '6px' }}><span style={{ color: 'var(--text-muted)' }}>Прогресс: {order.current_subs} / {order.subs_quantity}</span></div><div style={{ background: 'rgba(255,255,255,0.06)', height: '6px', borderRadius: '3px', overflow: 'hidden' }}><div style={{ background: order.status === 'pending' ? 'var(--accent-gold)' : '#34c759', height: '100%', width: `${progressPercent}%`, transition: 'width 0.5s ease' }} /></div></div>
                    </div>
                );
            }) : (
                <div style={{textAlign: 'center', color: 'var(--text-muted)', padding: '24px', background: 'rgba(255,255,255,0.02)', borderRadius: '20px', border: '1px dashed rgba(255,255,255,0.1)'}}>
                    <Megaphone size={28} style={{opacity: 0.2, marginBottom: '8px'}}/><div style={{fontSize: '13px'}}>У вас пока нет активных заказов.</div>
                </div>
            )}

            <WithdrawModal isOpen={isWithdrawModalOpen} onClose={() => setIsWithdrawModalOpen(false)} userBalance={localBalance} onSuccess={handleWithdrawSuccess} />
            <HoldInfoModal isOpen={isHoldModalOpen} onClose={() => setIsHoldModalOpen(false)} />
            <AdBalanceInfoModal isOpen={isAdInfoModalOpen} onClose={() => setIsAdInfoModalOpen(false)} />
            <ReferralInfoModal isOpen={isRefInfoModalOpen} onClose={() => setIsRefInfoModalOpen(false)} />
            <TopUpModal isOpen={isTopUpModalOpen} onClose={() => setIsTopUpModalOpen(false)} />
        </div>
    );
};

export default ProfilePage;