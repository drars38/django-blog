"""
Пример серверной части для плагина прокторинга RDP
Обрабатывает предупреждения от веб-клиента
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import sqlite3
import datetime
from typing import Dict, List, Any
import logging

app = Flask(__name__)
CORS(app)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RDPAlertProcessor:
    """Обработчик предупреждений о RDP подключениях"""
    
    def __init__(self, db_path: str = "rdp_alerts.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                alert_type TEXT,
                message TEXT,
                confidence REAL,
                evidence TEXT,
                timestamp DATETIME,
                ip_address TEXT,
                user_agent TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                start_time DATETIME,
                end_time DATETIME,
                total_alerts INTEGER DEFAULT 0,
                max_confidence REAL DEFAULT 0,
                ip_address TEXT,
                user_agent TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("База данных инициализирована")
    
    def process_alert(self, alert_data: Dict[str, Any], ip_address: str, user_agent: str) -> Dict[str, Any]:
        """Обработка предупреждения от клиента"""
        
        # Генерация ID сессии на основе IP и User-Agent
        session_id = self.generate_session_id(ip_address, user_agent)
        
        # Сохранение предупреждения
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (session_id, alert_type, message, confidence, evidence, timestamp, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            alert_data.get('message', 'Unknown'),
            alert_data.get('message', 'Unknown'),
            alert_data.get('confidence', 0),
            json.dumps(alert_data.get('evidence', [])),
            datetime.datetime.now(),
            ip_address,
            user_agent
        ))
        
        # Обновление статистики сессии
        cursor.execute('''
            INSERT OR REPLACE INTO sessions (id, start_time, end_time, total_alerts, max_confidence, ip_address, user_agent)
            VALUES (?, 
                COALESCE((SELECT start_time FROM sessions WHERE id = ?), ?),
                ?, 
                COALESCE((SELECT total_alerts FROM sessions WHERE id = ?), 0) + 1,
                MAX(COALESCE((SELECT max_confidence FROM sessions WHERE id = ?), 0), ?),
                ?, ?
            )
        ''', (
            session_id, session_id, datetime.datetime.now(),
            datetime.datetime.now(), session_id, session_id, alert_data.get('confidence', 0),
            ip_address, user_agent
        ))
        
        conn.commit()
        conn.close()
        
        # Анализ серьезности предупреждения
        severity = self.analyze_severity(alert_data)
        
        logger.info(f"Обработано предупреждение: {alert_data.get('message', 'Unknown')} "
                   f"(уверенность: {alert_data.get('confidence', 0):.2f})")
        
        return {
            'status': 'processed',
            'session_id': session_id,
            'severity': severity,
            'recommendations': self.get_recommendations(alert_data)
        }
    
    def generate_session_id(self, ip_address: str, user_agent: str) -> str:
        """Генерация уникального ID сессии"""
        import hashlib
        data = f"{ip_address}_{user_agent}_{datetime.date.today()}"
        return hashlib.md5(data.encode()).hexdigest()[:16]
    
    def analyze_severity(self, alert_data: Dict[str, Any]) -> str:
        """Анализ серьезности предупреждения"""
        confidence = alert_data.get('confidence', 0)
        
        if confidence >= 0.8:
            return 'critical'
        elif confidence >= 0.6:
            return 'high'
        elif confidence >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    def get_recommendations(self, alert_data: Dict[str, Any]) -> List[str]:
        """Получение рекомендаций на основе предупреждения"""
        recommendations = []
        confidence = alert_data.get('confidence', 0)
        
        if confidence >= 0.7:
            recommendations.extend([
                "Рекомендуется немедленно проверить активность пользователя",
                "Рассмотреть возможность приостановки тестирования",
                "Уведомить администратора системы"
            ])
        elif confidence >= 0.5:
            recommendations.extend([
                "Продолжить мониторинг активности",
                "Обратить внимание на поведение пользователя"
            ])
        else:
            recommendations.append("Мониторинг продолжается в обычном режиме")
        
        return recommendations
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Получение статистики сессии"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM sessions WHERE id = ?
        ''', (session_id,))
        
        session = cursor.fetchone()
        
        if session:
            cursor.execute('''
                SELECT COUNT(*) FROM alerts WHERE session_id = ?
            ''', (session_id,))
            total_alerts = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT alert_type, COUNT(*) FROM alerts WHERE session_id = ?
                GROUP BY alert_type ORDER BY COUNT(*) DESC
            ''', (session_id,))
            alert_types = dict(cursor.fetchall())
        
        conn.close()
        
        if session:
            return {
                'session_id': session[0],
                'start_time': session[1],
                'end_time': session[2],
                'total_alerts': total_alerts,
                'max_confidence': session[4],
                'alert_types': alert_types
            }
        
        return None

# Инициализация обработчика
alert_processor = RDPAlertProcessor()

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/rdp-alert', methods=['POST'])
def handle_rdp_alert():
    """Обработка предупреждений о RDP от клиента"""
    try:
        alert_data = request.get_json()
        
        if not alert_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Получение информации о клиенте
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        # Обработка предупреждения
        result = alert_processor.process_alert(alert_data, ip_address, user_agent)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Ошибка обработки предупреждения: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/session/<session_id>')
def get_session_info(session_id: str):
    """Получение информации о сессии"""
    try:
        stats = alert_processor.get_session_stats(session_id)
        
        if stats:
            return jsonify(stats)
        else:
            return jsonify({'error': 'Session not found'}), 404
            
    except Exception as e:
        logger.error(f"Ошибка получения информации о сессии: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/dashboard')
def dashboard():
    """Дашборд с общей статистикой"""
    try:
        conn = sqlite3.connect(alert_processor.db_path)
        cursor = conn.cursor()
        
        # Общая статистика
        cursor.execute('SELECT COUNT(*) FROM sessions')
        total_sessions = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM alerts')
        total_alerts = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(max_confidence) FROM sessions')
        avg_confidence = cursor.fetchone()[0] or 0
        
        # Топ подозрительных сессий
        cursor.execute('''
            SELECT id, total_alerts, max_confidence, start_time 
            FROM sessions 
            ORDER BY max_confidence DESC, total_alerts DESC 
            LIMIT 10
        ''')
        suspicious_sessions = cursor.fetchall()
        
        # Статистика по типам предупреждений
        cursor.execute('''
            SELECT alert_type, COUNT(*) 
            FROM alerts 
            GROUP BY alert_type 
            ORDER BY COUNT(*) DESC
        ''')
        alert_types = dict(cursor.fetchall())
        
        conn.close()
        
        return jsonify({
            'total_sessions': total_sessions,
            'total_alerts': total_alerts,
            'avg_confidence': round(avg_confidence, 2),
            'suspicious_sessions': [
                {
                    'session_id': session[0],
                    'total_alerts': session[1],
                    'max_confidence': session[2],
                    'start_time': session[3]
                }
                for session in suspicious_sessions
            ],
            'alert_types': alert_types
        })
        
    except Exception as e:
        logger.error(f"Ошибка получения статистики: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/alerts/recent')
def get_recent_alerts():
    """Получение последних предупреждений"""
    try:
        conn = sqlite3.connect(alert_processor.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT session_id, alert_type, message, confidence, timestamp, ip_address
            FROM alerts 
            ORDER BY timestamp DESC 
            LIMIT 50
        ''')
        
        alerts = cursor.fetchall()
        conn.close()
        
        return jsonify([
            {
                'session_id': alert[0],
                'alert_type': alert[1],
                'message': alert[2],
                'confidence': alert[3],
                'timestamp': alert[4],
                'ip_address': alert[5]
            }
            for alert in alerts
        ])
        
    except Exception as e:
        logger.error(f"Ошибка получения предупреждений: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Проверка состояния сервера"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Запуск сервера плагина прокторинга RDP...")
    print("📊 Дашборд доступен по адресу: http://localhost:5000/api/dashboard")
    print("🔍 API предупреждений: http://localhost:5000/api/rdp-alert")
    print("💚 Проверка состояния: http://localhost:5000/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

