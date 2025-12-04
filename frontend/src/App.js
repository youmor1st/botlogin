import React, { useEffect, useState } from "react";
import styled from "styled-components";
import axios from "axios";

// базовый контейнер мини-приложения
const Container = styled.div`
  font-family: Arial, sans-serif;
  padding: 20px;
  background: #0f172a;
  min-height: 100vh;
  color: #e5e7eb;
`;

// карточка по центру экрана
const Card = styled.div`
  max-width: 400px;
  margin: 0 auto;
  background: #111827;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
`;

// заголовок блока
const Title = styled.h1`
  font-size: 20px;
  margin-bottom: 16px;
`;

// текстовое поле
const Input = styled.input`
  width: 100%;
  padding: 10px 12px;
  margin-bottom: 12px;
  border-radius: 8px;
  border: 1px solid #374151;
  background: #020617;
  color: #e5e7eb;

  &:focus {
    outline: none;
    border-color: #22c55e;
  }
`;

// кнопка действия
const Button = styled.button`
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: none;
  background: #22c55e;
  color: #022c22;
  font-weight: 600;
  cursor: pointer;
  margin-top: 4px;

  &:disabled {
    background: #4b5563;
    cursor: default;
  }
`;

// блок сообщений
const Message = styled.div`
  margin-top: 12px;
  font-size: 14px;
`;

// основной компонент mini-app
function App() {
  // telegram_id текущего пользователя
  const [telegramId, setTelegramId] = useState(null);
  // информация о привязанном пользователе
  const [user, setUser] = useState(null);
  // признак, привязан ли уже telegram_id
  const [bound, setBound] = useState(null);
  // состояние загрузки
  const [loading, setLoading] = useState(true);
  // данные формы логина и пароля
  const [form, setForm] = useState({ username: "", password: "" });
  // текст ошибки
  const [error, setError] = useState("");

  useEffect(() => {
    // при монтировании пробуем инициализировать Telegram WebApp
    try {
      const tg = window.Telegram && window.Telegram.WebApp;
      const tgUser = tg && tg.initDataUnsafe && tg.initDataUnsafe.user;

      if (tgUser && tgUser.id) {
        // сохраняем telegram_id как строку
        const idStr = String(tgUser.id);
        setTelegramId(idStr);
        // сразу проверяем, есть ли привязка на бэкенде
        checkTelegramBinding(idStr);
      } else {
        // не смогли получить Telegram ID — скорее всего, приложение открыто не через Telegram
        setError(
          "Не удалось получить Telegram ID. Откройте мини‑приложение через бота в Telegram."
        );
        setLoading(false);
      }
    } catch (_e) {
      // любая ошибка инициализации
      setError("Ошибка инициализации Telegram WebApp.");
      setLoading(false);
    }
  }, []);

  const checkTelegramBinding = async (tgId) => {
    // запрос на бэкенд: проверяем привязку telegram_id
    try {
      const res = await axios.post(
        "https://YOUR_DOMAIN/api/auth/telegram-check/",
        {
          telegram_id: tgId
        }
      );
      setBound(res.data.bound);
      if (res.data.bound) {
        setUser(res.data.user);
      }
    } catch (_e) {
      // ошибка при запросе статуса привязки
      setError("Ошибка при запросе статуса привязки.");
    } finally {
      setLoading(false);
    }
  };

  const handleBind = async () => {
    // обработка отправки формы: первая привязка telegram_id
    setError("");
    if (!telegramId) {
      setError("Telegram ID не определён.");
      return;
    }

    try {
      const res = await axios.post("https://YOUR_DOMAIN/api/auth/bind/", {
        telegram_id: telegramId,
        username: form.username,
        password: form.password
      });

      if (res.data.bound) {
        // если привязка успешно выполнена, сохраняем пользователя
        setUser(res.data.user);
        setBound(true);
      }
    } catch (e) {
      // показываем сообщение из ответа или общее
      const message =
        e.response && e.response.data && e.response.data.detail
          ? e.response.data.detail
          : "Ошибка привязки.";
      setError(message);
    }
  };

  // экран загрузки
  if (loading) {
    return (
      <Container>
        <Card>
          <Title>Загрузка…</Title>
        </Card>
      </Container>
    );
  }

  return (
    <Container>
      <Card>
        <Title>Мини‑приложение авторизации</Title>

        {/* если привязка уже есть */}
        {bound && user && (
          <Message>
            Вы уже авторизованы как <b>{user.username}</b>. Повторный ввод логина
            и пароля не требуется.
          </Message>
        )}

        {/* если привязки нет — показываем форму */}
        {bound === false && (
          <>
            <Message>
              Введите логин и пароль, которые вы получили от администратора.
              После первого успешного входа ваш Telegram ID будет привязан.
            </Message>

            <Input
              placeholder="Логин"
              value={form.username}
              onChange={(e) =>
                setForm({ ...form, username: e.target.value })
              }
            />

            <Input
              placeholder="Пароль"
              type="password"
              value={form.password}
              onChange={(e) =>
                setForm({ ...form, password: e.target.value })
              }
            />

            <Button onClick={handleBind}>Привязать Telegram ID</Button>
          </>
        )}

        {/* вывод ошибок, если есть */}
        {error && <Message style={{ color: "#f97316" }}>{error}</Message>}
      </Card>
    </Container>
  );
}

export default App;



