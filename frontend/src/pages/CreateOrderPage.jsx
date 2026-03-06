import { useState } from 'react';
import axios from 'axios';
import { useTelegram } from '../hooks/useTelegram';
import { Rocket, Megaphone, Link2, Users, AlignLeft, Sparkles, Loader2, AlertCircle, ShieldAlert } from 'lucide-react';

const PRICE_PER_SUB = 1.0; 

const CreateOrderPage = ({ dbUser, onOrderCreated }) => {
    const { tg, triggerVibration } = useTelegram();
    
    const [channelLink, setChannelLink] = useState('');
    const [subsCount, setSubsCount] = useState(100); 
    const [description, setDescription] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const validateTelegramLink = (link) => {
        return link.trim().length > 2 && !link.includes(' ');
    };

    const normalizeLink = (link) => {
        let clean = link.trim();
        clean = clean.replace(/^(https?:\/\/)?(t\.me\/)?/i, '');
        if (clean.startsWith('@')) clean = clean.substring(1);
        if (clean.endsWith('/')) clean = clean.slice(0, -1);
        return `https://t.me/${clean}`;
    };

    const totalPrice = subsCount * PRICE_PER_SUB;
    const currentBalance = parseFloat(dbUser?.stars_balance || 0);
    const canAfford = currentBalance >= totalPrice;
    const isValid = subsCount >= 100 && channelLink.length > 4;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!validateTelegramLink(channelLink)) {
            triggerVibration('error');
            setError('Некорректная ссылка! Используйте @username или t.me/link');
            return;
        }

        if (!canAfford) {
            triggerVibration('error');
            setError('Недостаточно звезд на балансе!');
            return;
        }

        if (!isValid) return;

        triggerVibration('heavy');
        setIsLoading(true);

        const finalLink = normalizeLink(channelLink);

        try {
            await axios.post('/api/create-order', {
                subs_quantity: Number(subsCount),
                channel_id: finalLink, 
                creator_id: dbUser.id, 
                action_type: 'SUBSCRIBE_CHANNEL', 
                description: description || 'Подписка на Telegram канал'
            });

            triggerVibration('heavy');
            if (tg.showAlert) {
                tg.showAlert('Заказ успешно создан и запущен в работу!');
            } else {
                alert('Заказ успешно создан!');
            }
            
            setChannelLink('');
            if (onOrderCreated) onOrderCreated();

        } catch (err) {
            triggerVibration('error');
            const errMsg = err.response?.data?.detail || "Ошибка при создании заказа";
            setError(errMsg);
            console.error("Order error", err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="fade-in" style={{ padding: '20px', paddingBottom: '100px' }}>
            
            <div style={{ width: '100%', padding: '20px 0 40px', textAlign: 'center' }}>
                <div style={{ 
                    background: 'rgba(52, 199, 89, 0.1)', 
                    width: '60px', 
                    height: '60px', 
                    borderRadius: '50%', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center', 
                    margin: '0 auto 20px', 
                    color: '#34c759',
                    border: '1px solid rgba(52, 199, 89, 0.2)'
                }}>
                    <Rocket size={30} fill="#34c759" />
                </div>
                
                <h1 style={{ 
                    margin: 0, 
                    fontSize: '32px', 
                    fontWeight: '900', 
                    color: '#FFFFFF', 
                    textTransform: 'uppercase',
                    letterSpacing: '1px'
                }}>
                    BOOST CENTER
                </h1>
                
                <p style={{ 
                    margin: '8px 0 0', 
                    color: 'rgba(255, 255, 255, 0.5)', 
                    fontSize: '15px',
                    fontWeight: '500'
                }}>
                    Запустите свою рекламу
                </p>
            </div>

            <div className="b-box primary" style={{ marginBottom: '24px', padding: '16px' }}>
                <span className="b-label" style={{ color: 'rgba(255,255,255,0.8)' }}>Мой рекламный баланс</span>
                <div className="b-val" style={{ fontSize: '28px', margin: 0 }}>
                    {currentBalance.toFixed(2)} <span>⭐️</span>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="task-card-premium" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                
                <div className="input-group">
                    <label style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '6px', display: 'flex', gap: '6px', alignItems: 'center' }}>
                        <Link2 size={14}/> Ссылка на канал : 
                    </label>
                    <input 
                        type="text" 
                        placeholder="https://t.me/" 
                        value={channelLink}
                        onChange={(e) => setChannelLink(e.target.value)}
                        className="styled-input"
                        required
                    />
                </div>

                <div className="input-group">
                    <label style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '6px', display: 'flex', gap: '6px', alignItems: 'center' }}>
                        <Users size={14}/> Сколько нужно подписчиков? (Мин. 100)
                    </label>
                    <input 
                        type="number" 
                        min="100"
                        step="1"
                        value={subsCount}
                        onChange={(e) => setSubsCount(e.target.value)}
                        className="styled-input"
                        required
                    />
                </div>

                <div className="input-group">
                    <label style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '6px', display: 'flex', gap: '6px', alignItems: 'center' }}>
                        <AlignLeft size={14}/> Краткое описание (Опционально)
                    </label>
                    <input 
                        type="text" 
                        placeholder="Твое описание" 
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        className="styled-input"
                    />
                </div>

                <div style={{ background: 'rgba(0,0,0,0.2)', padding: '12px', borderRadius: '12px', marginTop: '8px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '14px' }}>
                        <span style={{ color: 'var(--text-muted)' }}>Цена за подписчика:</span>
                        <span>{PRICE_PER_SUB} ⭐️</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold', fontSize: '16px', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '8px' }}>
                        <span>Итого к оплате:</span>
                        <span style={{ color: canAfford ? 'var(--accent-gold)' : '#ff453a' }}>
                            {totalPrice} ⭐️
                        </span>
                    </div>
                </div>

                {error && (
                    <div style={{ color: '#ff453a', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '6px', marginTop: '4px' }}>
                        <AlertCircle size={14} /> {error}
                    </div>
                )}

                <div className="task-card-premium fade-in" style={{ 
                    marginTop: '24px', 
                    background: 'linear-gradient(145deg, rgba(52, 199, 89, 0.05) 0%, rgba(0,0,0,0.4) 100%)', 
                    border: '1px solid rgba(52, 199, 89, 0.2)' 
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                        <div style={{ background: 'rgba(52, 199, 89, 0.2)', padding: '10px', borderRadius: '12px', color: '#34c759' }}>
                            <ShieldAlert size={24} />
                        </div>
                        <div>
                            <h3 style={{ margin: 0, fontSize: '18px', color: '#fff' }}>Важные правила</h3>
                            <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Обязательно к прочтению</div>
                        </div>
                    </div>

                    <ul style={{ margin: 0, paddingLeft: '20px', color: 'rgba(255,255,255,0.8)', fontSize: '14px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        <li>
                            <b>Добавьте бота в администраторы:</b> Бот <span style={{color: 'var(--accent-gold)'}}>@StarvsTakeBot</span> должен быть админом вашего канала, иначе мы не сможем отслеживать подписки и заказ не запустится.
                        </li>
                        <li>
                            <b>Формат ссылки:</b> Принимаются только публичные ссылки формата <code style={{background: 'rgba(255,255,255,0.1)', padding: '2px 6px', borderRadius: '4px'}}>https://t.me/username</code>.
                        </li>
                        <li>
                            <b>Не меняйте ссылку:</b> Во время активной рекламной кампании менять юзернейм канала строго запрещено — заказ будет аннулирован без возврата средств.
                        </li>
                    </ul>
                </div>

                <button 
                    type="submit" 
                    className="action-btn-main" 
                    disabled={!isValid || !canAfford || isLoading}
                    style={{ marginTop: '8px', opacity: (!isValid || !canAfford) ? 0.5 : 1 }}
                >
                    {isLoading ? <Loader2 className="loader-spin" size={20}/> : (
                        <>
                            <Megaphone size={19} /> 
                            {canAfford ? 'Запустить продвижение' : 'Недостаточно звезд'}
                        </>
                    )}
                </button>
            </form>

            <style>{`
                .styled-input {
                    width: 100%; padding: 12px 16px; border-radius: 12px;
                    border: 1px solid var(--border-color); background: var(--bg-secondary);
                    color: white; font-size: 15px; outline: none; transition: border 0.2s;
                }
                .styled-input:focus { border-color: var(--accent-gold); }
            `}</style>
        </div>
    );
};

export default CreateOrderPage;