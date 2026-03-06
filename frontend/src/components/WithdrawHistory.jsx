import { useEffect, useState } from 'react';
import { getWithdrawHistory } from '../api/finances';
import { Clock, CheckCircle2, XCircle, ArrowDownToLine, Loader2, Info, ChevronDown, ChevronUp } from 'lucide-react';

const WithdrawHistory = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isExpanded, setIsExpanded] = useState(false);

    const loadHistory = async () => {
        try {
            const data = await getWithdrawHistory();
            if (Array.isArray(data)) {
                setHistory(data);
            }
        } catch (error) {
            console.error("Ошибка загрузки истории:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadHistory();
        window.addEventListener('withdrawalCreated', loadHistory);
        return () => window.removeEventListener('withdrawalCreated', loadHistory);
    }, []);

    const getStatusConfig = (status) => {
        switch (status) {
            case 'pending': return { icon: <Clock size={16}/>, color: '#ffcc00', text: 'В обработке', bg: 'rgba(255, 204, 0, 0.15)' };
            case 'approved': return { icon: <CheckCircle2 size={16}/>, color: '#34c759', text: 'Выплачено', bg: 'rgba(52, 199, 89, 0.15)' };
            case 'rejected': return { icon: <XCircle size={16}/>, color: '#ff3b30', text: 'Отклонено', bg: 'rgba(255, 59, 48, 0.15)' };
            default: return { icon: <Clock size={16}/>, color: '#aaa', text: status, bg: 'rgba(255,255,255,0.1)' };
        }
    };

    if (loading) return <div style={{textAlign: 'center', padding: '20px'}}><Loader2 className="loader-spin" size={24}/></div>;

    // какие элементы показывать
    const displayedHistory = isExpanded ? history : history.slice(0, 3);

    return (
        <div style={{marginBottom: '32px'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', paddingLeft: '4px'}}>
                <h3 style={{margin: 0, fontSize: '18px'}}>История выводов</h3>
                {history.length > 0 && (
                    <span style={{fontSize: '13px', color: 'var(--text-muted)'}}>Всего: {history.length}</span>
                )}
            </div>
            
            {history.length > 0 ? (
                <>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        {displayedHistory.map(item => {
                            const conf = getStatusConfig(item.status);
                            const date = new Date(item.created_at).toLocaleDateString('ru-RU', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });

                            return (
                                <div key={item.id} className="task-card-premium fade-in" style={{ padding: '14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <div>
                                        <div style={{ fontSize: '15px', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '6px' }}>
                                            <ArrowDownToLine size={14} color="var(--accent-gold)"/> {item.amount} ⭐️
                                        </div>
                                        <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                                            {date} • ID: #{item.id}
                                        </div>
                                    </div>
                                    <div style={{
                                        fontSize: '10px', fontWeight: '800', textTransform: 'uppercase',
                                        background: conf.bg, color: conf.color,
                                        padding: '5px 8px', borderRadius: '6px', display: 'flex', alignItems: 'center', gap: '4px'
                                    }}>
                                        {conf.icon} {conf.text}
                                    </div>
                                </div>
                            );
                        })}
                    </div>

                    {history.length > 3 && (
                        <button 
                            onClick={() => setIsExpanded(!isExpanded)}
                            style={{
                                width: '100%', marginTop: '12px', padding: '10px',
                                background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
                                borderRadius: '12px', color: 'var(--text-muted)', fontSize: '13px',
                                display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px',
                                cursor: 'pointer'
                            }}
                        >
                            {isExpanded ? (
                                <><ChevronUp size={16}/> Скрыть</>
                            ) : (
                                <><ChevronDown size={16}/> Показать все ({history.length})</>
                            )}
                        </button>
                    )}
                </>
            ) : (
                <div style={{textAlign: 'center', padding: '20px', background: 'rgba(255,255,255,0.03)', borderRadius: '16px', color: 'var(--text-muted)', fontSize: '13px'}}>
                    <Info size={20} style={{marginBottom: '6px', opacity: 0.4}} />
                    <div>У вас пока нет заявок на вывод</div>
                </div>
            )}
        </div>
    );
};

export default WithdrawHistory;