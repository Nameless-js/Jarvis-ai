import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("Нажми на микрофон или пиши вопрос")
  const [isListening, setIsListening] = useState(false)
  const [isAiSpeaking, setIsAiSpeaking] = useState(false)

  // --- 1. ГОВОРИЛКА (TTS) ---
  const speak = (text) => {
    if (!text) return;
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "ru-RU";
    
    // Включаем видео разговора
    setIsAiSpeaking(true);
    
    utterance.onend = () => {
      setIsAiSpeaking(false); // Выключаем, когда договорил
    };
    
    utterance.onerror = () => {
      setIsAiSpeaking(false); // Выключаем, если ошибка
    };

    window.speechSynthesis.speak(utterance);
  };

  // --- 2. СЛУШАЛКА (STT) ---
  const startListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Нужен Google Chrome для голосового ввода");
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'ru-RU';
    
    setIsListening(true);
    recognition.start();

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setIsListening(false);
      handleSend(transcript);
    };

    recognition.onerror = (e) => {
      console.error("Ошибка микрофона:", e);
      setIsListening(false);
    };
    recognition.onend = () => setIsListening(false);
  };

  // --- 3. ОТПРАВКА ВОПРОСА ---
  const handleSend = async (text) => {
    if (!text.trim()) return;
    
    setAnswer("Думаю...");
    console.log("Отправляю:", text);

    try {
      const response = await axios.post('http://127.0.0.1:8000/ask', {
        text: text,
        language: "ru"
      });
      
      const botResponse = response.data.response;
      console.log("Пришел ответ:", botResponse);
      
      if (botResponse) {
        setAnswer(botResponse);
        speak(botResponse);
      } else {
        setAnswer("Бэкенд вернул пустой ответ 🤔");
      }
      
      setQuestion(""); // Очищаем поле ввода

    } catch (error) {
      console.error("Ошибка:", error);
      setAnswer("Ошибка связи с сервером 💀");
      setIsAiSpeaking(false);
    }
  };

  // Обработчик нажатия Enter (чтобы не перезагружал страницу)
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault(); // <--- ВОТ ГЛАВНОЕ ЛЕКАРСТВО
      handleSend(question);
    }
  };

  return (
    <div className="app-container">
      {/* Видео-фоны */}
      <video className={`video-bg ${isAiSpeaking ? 'hidden' : 'visible'}`} autoPlay loop muted playsInline src="/idle.mp4" />
      <video className={`video-bg ${isAiSpeaking ? 'visible' : 'hidden'}`} autoPlay loop muted playsInline src="/speaking.mp4" />

      <div className="interface">
        <h1>JARVIS AI</h1>
        
        {/* Блок ответа */}
        <div style={{ minHeight: "80px", margin: "20px 0", fontSize: "1.3rem", whiteSpace: "pre-wrap" }}>
          {answer}
        </div>
        
        {/* Кнопка микрофона */}
        <button 
          className={`mic-btn ${isListening ? 'listening' : ''}`} 
          onClick={startListening}
          title="Голосовой ввод"
        >
          {isListening ? '👂' : '🎙️'}
        </button>

        {/* Текстовый ввод */}
        <div style={{ marginTop: "20px", display: "flex", gap: "10px", justifyContent: "center" }}>
          <input 
            type="text" 
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown} // Используем защищенный обработчик
            placeholder="Напиши вопрос..."
            style={{ padding: "12px", borderRadius: "8px", border: "none", width: "70%", fontSize: "16px" }}
          />
          <button 
            type="button" // <--- Важно: чтобы кнопка не обновляла страницу
            onClick={() => handleSend(question)} 
            style={{ padding: "12px", cursor: "pointer", borderRadius: "8px", border: "none" }}
          >
            🚀
          </button>
        </div>
      </div>
    </div>
  )
}

export default App