/**
 * Веб-плагин для обнаружения RDP подключений
 * Работает только в браузере без установки дополнительного ПО
 */

class RDPDetector {
    constructor() {
        this.suspiciousActivity = [];
        this.behaviorMetrics = {
            mouseMovements: [],
            keystrokes: [],
            screenInteractions: [],
            timingPatterns: []
        };
        this.detectionThreshold = 0.7; // Порог подозрительности
        this.isMonitoring = false;
    }

    /**
     * Инициализация детектора
     */
    async initialize() {
        console.log('🔍 Инициализация RDP детектора...');
        
        // Запрос разрешений на камеру и микрофон
        await this.requestPermissions();
        
        // Настройка мониторинга
        this.setupBehaviorMonitoring();
        this.setupScreenAnalysis();
        this.setupNetworkAnalysis();
        
        this.isMonitoring = true;
        console.log('✅ RDP детектор активирован');
    }

    /**
     * Запрос разрешений на камеру и микрофон
     */
    async requestPermissions() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
            
            // Анализ качества видео для обнаружения RDP
            this.analyzeVideoQuality(stream);
            
            console.log('✅ Разрешения получены');
            return true;
        } catch (error) {
            console.error('❌ Ошибка получения разрешений:', error);
            return false;
        }
    }

    /**
     * Анализ качества видео для обнаружения RDP
     */
    analyzeVideoQuality(stream) {
        const video = document.createElement('video');
        video.srcObject = stream;
        video.play();

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        const analyzeFrame = () => {
            if (video.videoWidth && video.videoHeight) {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                ctx.drawImage(video, 0, 0);
                
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const quality = this.calculateVideoQuality(imageData);
                
                // RDP часто имеет характерные артефакты сжатия
                if (quality.compressionArtifacts > 0.8) {
                    this.addSuspiciousActivity('RDP_COMPRESSION_ARTIFACTS', quality);
                }
            }
            
            if (this.isMonitoring) {
                requestAnimationFrame(analyzeFrame);
            }
        };

        analyzeFrame();
    }

    /**
     * Расчет качества видео
     */
    calculateVideoQuality(imageData) {
        const data = imageData.data;
        let compressionArtifacts = 0;
        let colorVariation = 0;
        
        // Анализ блоков пикселей для обнаружения артефактов сжатия
        for (let i = 0; i < data.length; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];
            
            // Простой алгоритм обнаружения артефактов JPEG/RDP сжатия
            const luminance = 0.299 * r + 0.587 * g + 0.114 * b;
            colorVariation += Math.abs(luminance - 128);
        }
        
        compressionArtifacts = colorVariation / (data.length / 4) / 128;
        
        return {
            compressionArtifacts,
            timestamp: Date.now()
        };
    }

    /**
     * Настройка мониторинга поведения пользователя
     */
    setupBehaviorMonitoring() {
        // Мониторинг движений мыши
        document.addEventListener('mousemove', (e) => {
            this.trackMouseMovement(e);
        });

        // Мониторинг нажатий клавиш
        document.addEventListener('keydown', (e) => {
            this.trackKeystroke(e);
        });

        // Мониторинг кликов
        document.addEventListener('click', (e) => {
            this.trackClick(e);
        });

        // Мониторинг прокрутки
        document.addEventListener('scroll', (e) => {
            this.trackScroll(e);
        });
    }

    /**
     * Отслеживание движений мыши
     */
    trackMouseMovement(event) {
        const movement = {
            x: event.clientX,
            y: event.clientY,
            timestamp: Date.now(),
            speed: this.calculateMouseSpeed(event)
        };

        this.behaviorMetrics.mouseMovements.push(movement);
        
        // Анализ паттернов движения
        this.analyzeMousePatterns();
        
        // Ограничение размера массива
        if (this.behaviorMetrics.mouseMovements.length > 100) {
            this.behaviorMetrics.mouseMovements.shift();
        }
    }

    /**
     * Расчет скорости мыши
     */
    calculateMouseSpeed(event) {
        if (this.behaviorMetrics.mouseMovements.length === 0) return 0;
        
        const lastMovement = this.behaviorMetrics.mouseMovements[this.behaviorMetrics.mouseMovements.length - 1];
        const timeDiff = event.timeStamp - lastMovement.timestamp;
        const distance = Math.sqrt(
            Math.pow(event.clientX - lastMovement.x, 2) + 
            Math.pow(event.clientY - lastMovement.y, 2)
        );
        
        return timeDiff > 0 ? distance / timeDiff : 0;
    }

    /**
     * Анализ паттернов движения мыши
     */
    analyzeMousePatterns() {
        if (this.behaviorMetrics.mouseMovements.length < 10) return;

        const movements = this.behaviorMetrics.mouseMovements.slice(-10);
        
        // Проверка на роботизированные движения (характерно для RDP)
        const isRobotic = this.detectRoboticMovement(movements);
        
        // Проверка на задержки (характерно для удаленных подключений)
        const hasDelays = this.detectNetworkDelays(movements);
        
        if (isRobotic || hasDelays) {
            this.addSuspiciousActivity('SUSPICIOUS_MOUSE_PATTERN', {
                robotic: isRobotic,
                delays: hasDelays,
                timestamp: Date.now()
            });
        }
    }

    /**
     * Обнаружение роботизированных движений
     */
    detectRoboticMovement(movements) {
        let perfectLines = 0;
        let totalMovements = movements.length - 1;
        
        for (let i = 1; i < movements.length; i++) {
            const prev = movements[i - 1];
            const curr = movements[i];
            
            // Проверка на идеально прямые линии (характерно для автоматизации)
            const angle = Math.atan2(curr.y - prev.y, curr.x - prev.x);
            const roundedAngle = Math.round(angle * 4) / 4; // Округление до 45 градусов
            
            if (Math.abs(angle - roundedAngle) < 0.1) {
                perfectLines++;
            }
        }
        
        return (perfectLines / totalMovements) > 0.7;
    }

    /**
     * Обнаружение сетевых задержек
     */
    detectNetworkDelays(movements) {
        const delays = [];
        
        for (let i = 1; i < movements.length; i++) {
            const timeDiff = movements[i].timestamp - movements[i - 1].timestamp;
            delays.push(timeDiff);
        }
        
        // RDP часто имеет характерные задержки
        const avgDelay = delays.reduce((a, b) => a + b, 0) / delays.length;
        const variance = delays.reduce((acc, delay) => acc + Math.pow(delay - avgDelay, 2), 0) / delays.length;
        
        return avgDelay > 50 && variance < 100; // Стабильные задержки
    }

    /**
     * Отслеживание нажатий клавиш
     */
    trackKeystroke(event) {
        const keystroke = {
            key: event.key,
            code: event.code,
            timestamp: Date.now(),
            duration: 0
        };

        this.behaviorMetrics.keystrokes.push(keystroke);
        
        // Анализ скорости набора
        this.analyzeTypingPatterns();
        
        // Ограничение размера массива
        if (this.behaviorMetrics.keystrokes.length > 50) {
            this.behaviorMetrics.keystrokes.shift();
        }
    }

    /**
     * Анализ паттернов набора текста
     */
    analyzeTypingPatterns() {
        if (this.behaviorMetrics.keystrokes.length < 5) return;

        const keystrokes = this.behaviorMetrics.keystrokes.slice(-5);
        
        // Проверка на слишком равномерные интервалы (автоматизация)
        const intervals = [];
        for (let i = 1; i < keystrokes.length; i++) {
            intervals.push(keystrokes[i].timestamp - keystrokes[i - 1].timestamp);
        }
        
        const avgInterval = intervals.reduce((a, b) => a + b, 0) / intervals.length;
        const isUniform = intervals.every(interval => Math.abs(interval - avgInterval) < 10);
        
        if (isUniform && avgInterval < 100) {
            this.addSuspiciousActivity('UNIFORM_TYPING_PATTERN', {
                avgInterval,
                timestamp: Date.now()
            });
        }
    }

    /**
     * Настройка анализа экрана
     */
    setupScreenAnalysis() {
        // Анализ разрешения экрана
        this.analyzeScreenResolution();
        
        // Анализ цветовой палитры
        this.analyzeColorPalette();
        
        // Проверка на виртуальные машины
        this.detectVirtualMachine();
    }

    /**
     * Анализ разрешения экрана
     */
    analyzeScreenResolution() {
        const screenInfo = {
            width: screen.width,
            height: screen.height,
            availWidth: screen.availWidth,
            availHeight: screen.availHeight,
            colorDepth: screen.colorDepth,
            pixelDepth: screen.pixelDepth
        };

        // RDP часто использует стандартные разрешения
        const commonRDPResolutions = [
            { width: 1024, height: 768 },
            { width: 1280, height: 720 },
            { width: 1920, height: 1080 },
            { width: 1366, height: 768 }
        ];

        const isCommonResolution = commonRDPResolutions.some(res => 
            res.width === screenInfo.width && res.height === screenInfo.height
        );

        if (isCommonResolution) {
            this.addSuspiciousActivity('COMMON_RDP_RESOLUTION', screenInfo);
        }
    }

    /**
     * Анализ цветовой палитры
     */
    analyzeColorPalette() {
        const canvas = document.createElement('canvas');
        canvas.width = 1;
        canvas.height = 1;
        const ctx = canvas.getContext('2d');
        
        // RDP часто ограничивает цветовую палитру
        ctx.fillStyle = '#FF0000';
        ctx.fillRect(0, 0, 1, 1);
        
        const imageData = ctx.getImageData(0, 0, 1, 1);
        const pixel = imageData.data;
        
        // Проверка на ограниченную цветовую палитру
        const colorVariation = Math.abs(pixel[0] - 255) + Math.abs(pixel[1] - 0) + Math.abs(pixel[2] - 0);
        
        if (colorVariation > 10) {
            this.addSuspiciousActivity('LIMITED_COLOR_PALETTE', {
                colorVariation,
                timestamp: Date.now()
            });
        }
    }

    /**
     * Обнаружение виртуальных машин
     */
    detectVirtualMachine() {
        const vmIndicators = [];
        
        // Проверка WebGL
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        
        if (gl) {
            const renderer = gl.getParameter(gl.RENDERER);
            const vendor = gl.getParameter(gl.VENDOR);
            
            // Проверка на известные VM рендереры
            const vmRenderers = ['VMware', 'VirtualBox', 'QEMU', 'Microsoft Basic Render Driver'];
            if (vmRenderers.some(vm => renderer.includes(vm) || vendor.includes(vm))) {
                vmIndicators.push('VM_RENDERER');
            }
        }
        
        // Проверка доступных API
        if (navigator.hardwareConcurrency <= 2) {
            vmIndicators.push('LIMITED_CPU_CORES');
        }
        
        if (vmIndicators.length > 0) {
            this.addSuspiciousActivity('VIRTUAL_MACHINE_DETECTED', {
                indicators: vmIndicators,
                timestamp: Date.now()
            });
        }
    }

    /**
     * Настройка анализа сети
     */
    setupNetworkAnalysis() {
        // Мониторинг изменений соединения
        window.addEventListener('online', () => {
            this.addSuspiciousActivity('NETWORK_RECONNECTION', {
                timestamp: Date.now()
            });
        });

        window.addEventListener('offline', () => {
            this.addSuspiciousActivity('NETWORK_DISCONNECTION', {
                timestamp: Date.now()
            });
        });

        // Анализ времени отклика
        this.analyzeResponseTimes();
    }

    /**
     * Анализ времени отклика
     */
    async analyzeResponseTimes() {
        const startTime = performance.now();
        
        try {
            // Простой запрос для измерения задержки
            await fetch(window.location.href, { method: 'HEAD' });
            const responseTime = performance.now() - startTime;
            
            // RDP может увеличивать задержку сети
            if (responseTime > 200) {
                this.addSuspiciousActivity('HIGH_NETWORK_LATENCY', {
                    responseTime,
                    timestamp: Date.now()
                });
            }
        } catch (error) {
            console.log('Ошибка анализа сети:', error);
        }
    }

    /**
     * Добавление подозрительной активности
     */
    addSuspiciousActivity(type, data) {
        const activity = {
            type,
            data,
            timestamp: Date.now(),
            severity: this.calculateSeverity(type)
        };

        this.suspiciousActivity.push(activity);
        
        // Ограничение размера массива
        if (this.suspiciousActivity.length > 100) {
            this.suspiciousActivity.shift();
        }

        // Проверка общего уровня подозрительности
        this.checkOverallSuspicion();
    }

    /**
     * Расчет серьезности активности
     */
    calculateSeverity(type) {
        const severityMap = {
            'RDP_COMPRESSION_ARTIFACTS': 0.8,
            'SUSPICIOUS_MOUSE_PATTERN': 0.6,
            'UNIFORM_TYPING_PATTERN': 0.7,
            'COMMON_RDP_RESOLUTION': 0.3,
            'LIMITED_COLOR_PALETTE': 0.4,
            'VIRTUAL_MACHINE_DETECTED': 0.9,
            'HIGH_NETWORK_LATENCY': 0.5,
            'NETWORK_RECONNECTION': 0.6
        };

        return severityMap[type] || 0.5;
    }

    /**
     * Проверка общего уровня подозрительности
     */
    checkOverallSuspicion() {
        if (this.suspiciousActivity.length < 3) return;

        const recentActivity = this.suspiciousActivity.slice(-10);
        const avgSeverity = recentActivity.reduce((sum, activity) => sum + activity.severity, 0) / recentActivity.length;
        
        if (avgSeverity > this.detectionThreshold) {
            this.triggerRDPAlert();
        }
    }

    /**
     * Срабатывание предупреждения о RDP
     */
    triggerRDPAlert() {
        const alert = {
            message: 'Обнаружена подозрительная активность, указывающая на возможное RDP подключение',
            timestamp: Date.now(),
            evidence: this.suspiciousActivity.slice(-5),
            confidence: this.calculateConfidence()
        };

        console.warn('🚨 RDP ALERT:', alert);
        
        // Отправка данных на сервер
        this.sendAlertToServer(alert);
        
        // Уведомление пользователя
        this.notifyUser(alert);
    }

    /**
     * Расчет уверенности в обнаружении
     */
    calculateConfidence() {
        const recentActivity = this.suspiciousActivity.slice(-10);
        const highSeverityCount = recentActivity.filter(a => a.severity > 0.7).length;
        
        return Math.min(highSeverityCount / 5, 1.0);
    }

    /**
     * Отправка предупреждения на сервер
     */
    async sendAlertToServer(alert) {
        try {
            await fetch('/api/rdp-alert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(alert)
            });
        } catch (error) {
            console.error('Ошибка отправки предупреждения:', error);
        }
    }

    /**
     * Уведомление пользователя
     */
    notifyUser(alert) {
        // Создание уведомления
        const notification = document.createElement('div');
        notification.className = 'rdp-alert-notification';
        notification.innerHTML = `
            <div class="alert-content">
                <h3>⚠️ Предупреждение о безопасности</h3>
                <p>${alert.message}</p>
                <p>Уверенность: ${Math.round(alert.confidence * 100)}%</p>
                <button onclick="this.parentElement.parentElement.remove()">Закрыть</button>
            </div>
        `;
        
        // Стили для уведомления
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff4444;
            color: white;
            padding: 15px;
            border-radius: 8px;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        
        document.body.appendChild(notification);
        
        // Автоматическое удаление через 10 секунд
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 10000);
    }

    /**
     * Получение отчета о подозрительной активности
     */
    getReport() {
        return {
            totalActivities: this.suspiciousActivity.length,
            recentActivities: this.suspiciousActivity.slice(-10),
            overallSuspicion: this.calculateOverallSuspicion(),
            timestamp: Date.now()
        };
    }

    /**
     * Расчет общего уровня подозрительности
     */
    calculateOverallSuspicion() {
        if (this.suspiciousActivity.length === 0) return 0;
        
        const avgSeverity = this.suspiciousActivity.reduce((sum, activity) => sum + activity.severity, 0) / this.suspiciousActivity.length;
        return avgSeverity;
    }

    /**
     * Остановка мониторинга
     */
    stop() {
        this.isMonitoring = false;
        console.log('🛑 RDP детектор остановлен');
    }
}

// Экспорт для использования
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RDPDetector;
} else {
    window.RDPDetector = RDPDetector;
}

// Автоматическая инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    const detector = new RDPDetector();
    detector.initialize();
    
    // Глобальный доступ для отладки
    window.rdpDetector = detector;
});

