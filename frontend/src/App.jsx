import { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useTelegram } from './hooks/useTelegram';
import { ShieldAlert, MessageSquare } from 'lucide-react'; // <--- ВОТ ЭТОТ ИМПОРТ БЫЛ НУЖЕН
import TasksPage from './pages/TasksPage';
import ProfilePage from './pages/ProfilePage';
import CreateOrderPage from './pages/CreateOrderPage';
import './App.css';

function App() {
  const { tg, user, triggerVibration } = useTelegram();
  const [activeTab, setActiveTab] = useState('tasks');
  const [dbUser, setDbUser] = useState(null);

  const fetchUser = useCallback(() => {
    
      const tgId = window.Telegram.WebApp.initDataUnsafe?.user?.id || user?.id;
      const tgUsername = window.Telegram.WebApp.initDataUnsafe?.user?.username || user?.username || 'user';

      if (tgId) {
          axios.post('/api/auth', {
              tg_id: tgId,
              username: tgUsername
          })
          .then(res => setDbUser(res.data))
          .catch(e => console.error("Ошибка авторизации", e));
      }
    }, [tg, user?.id, user?.username]);

    useEffect(() => {
      tg.ready();
      tg.expand();
      fetchUser();
    }, []);

  const navChange = (tab) => {
    triggerVibration('heavy');
    setActiveTab(tab);
  };

  if (dbUser?.is_banned) {
    return (
        <div className="fade-in" style={{
            background: '#050505', minHeight: '100vh', display: 'flex',
            flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
            padding: '20px', textAlign: 'center'
        }}>
            <div style={{ 
                background: 'rgba(255, 59, 48, 0.1)', padding: '24px', 
                borderRadius: '50%', marginBottom: '24px',
                border: '1px solid rgba(255, 59, 48, 0.2)'
            }}>
                <ShieldAlert size={64} color="#ff3b30" />
            </div>
            
            <h1 style={{ color: '#fff', fontSize: '28px', fontWeight: 900, marginBottom: '12px', textTransform: 'uppercase' }}>
                Доступ закрыт
            </h1>
            
            <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '15px', lineHeight: '1.5', marginBottom: '32px', maxWidth: '300px' }}>
                Ваш аккаунт был заблокирован за нарушение правил сервиса. Вы больше не можете выполнять задания или создавать заказы.
            </p>
            
            <a
                href="https://t.me/managgee"
                style={{
                    background: '#ffffff', color: '#000000', padding: '16px 32px',
                    borderRadius: '16px', fontWeight: 900, textDecoration: 'none',
                    fontSize: '16px', display: 'flex', alignItems: 'center', gap: '8px'
                }}
            >
                <MessageSquare size={20} /> Поддержка
            </a>
        </div>
    );
  }

  return (
    <div className="App">
      {activeTab === 'tasks' && <TasksPage onTaskCompleted={fetchUser} />}
      {activeTab === 'create' && <CreateOrderPage dbUser={dbUser} onOrderCreated={() => { fetchUser(); navChange('profile'); }} />}
      {activeTab === 'profile' && <ProfilePage dbUser={dbUser} />}

      {/* Нижний Док (Навигация) */}
      <nav className="bottom-dock">
        <button className={`nav-item ${activeTab === 'tasks' ? 'active' : ''}`} onClick={() => navChange('tasks')}>
          ⚡️ <span>Задания</span>
        </button>
        <button className={`nav-item ${activeTab === 'create' ? 'active' : ''}`} onClick={() => navChange('create')}>
          ➕ <span>Создать</span>
        </button>
        <button className={`nav-item ${activeTab === 'profile' ? 'active' : ''}`} onClick={() => navChange('profile')}>
          👤 <span>Профиль</span>
        </button>
      </nav>
    </div>
  );
}

export default App;