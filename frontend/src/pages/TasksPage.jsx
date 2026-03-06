import { useEffect, useState } from 'react';
import axios from 'axios';
import { useTelegram } from '../hooks/useTelegram';
import { 
    Loader2, ExternalLink, 
    ShieldCheck, Sparkles, AlertCircle, Snowflake, BadgeCheck, Zap
} from 'lucide-react';

const TasksPage = ({ onTaskCompleted }) => {
    const [tasks, setTasks] = useState([]);
    const [loadingStates, setLoadingStates] = useState({});
    const [toast, setToast] = useState(null);
    const [errorModal, setErrorModal] = useState(null);
    const { tg, user, triggerVibration } = useTelegram();
    const [exitingTaskId, setExitingTaskId] = useState(null);

    useEffect(() => {
        if (user?.id) {
            axios.get(`/api/tasks/available?user_id=${user.id}`)
                .then(res => setTasks(res.data))
                .catch(err => console.error("Ошибка загрузки:", err));
        }
    }, [user?.id]);

    const showSuccessToast = (reward) => {
        setToast(`Успешно! +${reward} ⭐️`);
        triggerVibration('heavy');
        setTimeout(() => setToast(null), 3000);
    };

    const handleOpenChannel = (task) => {
        triggerVibration('heavy');
        let rawUrl = task.channel_url || task.channel_id || task.order?.channel_id;
        if (!rawUrl) return;
        const cleanName = rawUrl.replace(/https?:\/\/t\.me\//i, '').replace('@', '').split('/')[0].trim();
        const link = `https://t.me/${cleanName}`;
        const protocolLink = `tg://resolve?domain=${cleanName}`;
        try {
            if (tg && tg.openTelegramLink) {
                tg.openTelegramLink(link);
            } else {
                window.location.href = protocolLink;
            }
        } catch (e) {
            window.open(link, '_blank');
        }
    };

    const handleVerify = async (task) => {
        setLoadingStates(prev => ({ ...prev, [task.id]: 'loading' }));
        try {
            await axios.post(`/api/tasks/complete?user_id=${user.id}&task_id=${task.id}`);
            triggerVibration('heavy');
            setExitingTaskId(task.id);
            setTimeout(() => {
                showSuccessToast(task.reward || "0.25");
                if (onTaskCompleted) onTaskCompleted();
                setTasks(prev => prev.filter(t => t.id !== task.id));
                setExitingTaskId(null);
            }, 400);
        } catch (error) {
            triggerVibration('heavy');
            const errorMsg = error.response?.data?.detail || "Ошибка проверки. Подпишитесь на канал!";
            setErrorModal(errorMsg);
        } finally {
            setLoadingStates(prev => ({ ...prev, [task.id]: null }));
        }
    };

    return (
        <div className="page-container fade-in" style={{ 
            paddingBottom: '120px', 
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
        }}>
            {/* ТОСТЫ И МОДАЛКИ */}
            {toast && (
                <div style={{ position: 'fixed', top: '20px', left: 0, right: 0, zIndex: 1000, display: 'flex', justifyContent: 'center', pointerEvents: 'none' }}>
                    <div className="fade-in" style={{ background: 'rgba(52, 199, 89, 0.95)', padding: '12px 24px', borderRadius: '50px', display: 'flex', alignItems: 'center', gap: '10px', color: '#fff', fontWeight: 900, backdropFilter: 'blur(10px)', pointerEvents: 'auto' }}>
                        <Sparkles size={20} />
                        <span>{toast}</span>
                    </div>
                </div>
            )}

            {errorModal && (
                <div className="modal-overlay fade-in" style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.85)', zIndex: 9999, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
                    <div className="modal-content scale-in" style={{ background: '#111', width: '100%', maxWidth: '350px', borderRadius: '28px', padding: '24px', border: '1px solid rgba(255, 59, 48, 0.3)', textAlign: 'center' }}>
                        <div style={{ background: 'rgba(255, 59, 48, 0.1)', width: '64px', height: '64px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px', color: '#ff3b30' }}>
                            <AlertCircle size={32} />
                        </div>
                        <h3 style={{ margin: '0 0 10px 0', fontSize: '20px', color: '#fff', fontWeight: 800 }}>Внимание</h3>
                        <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: '14px', margin: '0 0 24px 0' }}>{errorModal}</p>
                        <button onClick={() => { triggerVibration('heavy'); setErrorModal(null); }} style={{ background: '#ff3b30', color: '#fff', width: '100%', padding: '14px', borderRadius: '16px', fontWeight: 'bold', border: 'none' }}>Понятно</button>
                    </div>
                </div>
            )}

            {/* ШАПКА */}
            <div style={{ width: '100%', maxWidth: '500px', padding: '40px 20px 20px', textAlign: 'center' }}>
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
                    <Zap size={30} fill="#34c759" />
                </div>
                
                <h1 style={{ margin: 0, fontSize: '32px', fontWeight: '900', color: '#FFFFFF', textTransform: 'uppercase', letterSpacing: '1px' }}>
                    EARN CENTER
                </h1>
                
                <p style={{ margin: '8px 0 0', color: 'rgba(255, 255, 255, 0.5)', fontSize: '15px', fontWeight: '500' }}>
                    Выполняй задания и забирай звезды
                </p>
            </div>

            {/* СПИСОК ЗАДАНИЙ */}
            <div className="task-container" style={{ width: '100%', maxWidth: '500px', padding: '0 16px' }}>
                {tasks.length > 0 ? tasks.map(task => (
                    <div 
                        key={task.id} 
                        className={`task-card-premium fade-in ${exitingTaskId === task.id ? 'task-card-exit' : ''}`} 
                        style={{ 
                            background: '#111', 
                            borderRadius: '28px', 
                            padding: '24px', 
                            marginBottom: '16px', 
                            border: '1px solid rgba(255, 255, 255, 0.05)',
                            boxShadow: '0 12px 40px rgba(0,0,0,0.6)'
                        }}
                    >
                        {/* КАРТОЧКА ЗАДАНИЯ */}
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <div style={{ background: 'rgba(255,255,255,0.05)', padding: '10px', borderRadius: '14px' }}><span>📱</span></div>
                                <div style={{ display: 'flex', flexDirection: 'column' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                        <div style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)', padding: '4px 10px', borderRadius: '10px', fontSize: '12px', fontWeight: '800', color: '#fff' }}>ПОДПИСКА</div>
                                        <BadgeCheck size={18} color="#34c759" />
                                    </div>
                                    <span style={{ fontSize: '11px', color: 'rgba(255,255,255,0.3)', fontWeight: 600 }}>Telegram Task</span>
                                </div>
                            </div>
                            <div style={{ background: 'rgba(52, 199, 89, 0.12)', color: '#34c759', padding: '8px 14px', borderRadius: '14px', fontWeight: 900 }}>+0.25 ⭐️</div>
                        </div>

                        <div style={{ background: 'rgba(125, 211, 252, 0.05)', padding: '16px', borderRadius: '20px', fontSize: '13px', color: 'rgba(255,255,255,0.7)', marginBottom: '20px', border: '1px solid rgba(125, 211, 252, 0.1)' }}>
                            <div style={{display: 'flex', alignItems: 'center', gap: '6px', color: '#7dd3fc', fontWeight: '800', marginBottom: '4px', fontSize: '11px'}}><Snowflake size={14}/> СИСТЕМА ЗАМОРОЗКИ</div>
                            Не отписывайтесь 72 часа или холд будет обнулен!
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                            <button onClick={() => handleOpenChannel(task)} style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', color: '#fff', padding: '16px', borderRadius: '18px', fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}><ExternalLink size={16}/> Открыть</button>
                            <button onClick={() => handleVerify(task)} disabled={loadingStates[task.id] === 'loading'} style={{ background: '#ffffff', color: '#000000', padding: '16px', borderRadius: '18px', fontWeight: 900, border: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                                {loadingStates[task.id] === 'loading' ? <Loader2 className="loader-spin" size={18}/> : <><ShieldCheck size={18}/> Проверить</>}
                            </button>
                        </div>
                    </div>
                )) : (
                    <div style={{textAlign: 'center', marginTop: '60px', color: 'rgba(255,255,255,0.15)'}}><div style={{ fontSize: '64px' }}>🏝</div><p style={{fontWeight: 600}}>Заданий пока нет</p></div>
                )}
            </div>
        </div>
    );
};

export default TasksPage;