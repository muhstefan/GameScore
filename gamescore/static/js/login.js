document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const errorMessage = document.getElementById('error-message');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);  // собираем данные формы

    try {
      const response = await fetch('/api/v1/auth/login/', {
        method: 'POST',
        body: formData,  // отправляем как form-data
      });

      if (response.ok) {
        const result = await response.json();
        // Обработка успешного входа, например, редирект
        window.location.href = '/';
      } else {
        const errorData = await response.json();
        errorMessage.textContent = errorData.detail || 'Ошибка входа';
      }
    } catch (err) {
      errorMessage.textContent = 'Ошибка сети';
    }
  });
});
