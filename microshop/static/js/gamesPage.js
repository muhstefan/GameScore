const containers = document.querySelectorAll('.game-container');
const modal = document.getElementById('myModal');
const add_game_btn = document.getElementById('add_game');
const save_game = document.getElementById('save_game');
const form = document.getElementById('gameForm');
const formData = new FormData(form);
const gamesListContainer = document.getElementById('games_list_container');
import { BASE_URL } from './config.js';



gamesListContainer.addEventListener('click', (event) => {
  const btn = event.target.closest('button');
  if (!btn) return; // Клик не по кнопке — игнорируем

  const id = btn.dataset.id;       // Получаем ID игры из data-атрибута
  const action = btn.dataset.action; // Получаем действие (edit/delete)

  if (!id || !action) return; // Если нет нужных данных — игнорируем

  if (action === 'delete') {
    delete_game(id);
  } else if (action === 'edit') {
    edit_game(id);
  }
});


function get_input_data() {
  const formData = new FormData(form); // создаём здесь, чтобы получить актуальные данные

  const data = {
    name: formData.get('title').trim(),
    description: formData.get('description').trim(),
    rating: parseFloat(formData.get('rating'))
  };

  return data;
}

function create_game(){
    const data = get_input_data();
    console.log('Тело запроса (data):', data);  // Логируем данные перед отправкой

    fetch(`${BASE_URL}/api/v1/games/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
}

function refreshGameList() {
  fetch('/pages/games/list/')  // URL, который возвращает готовый HTML списка
    .then(response => response.text())
    .then(html => {
      document.getElementById('games_list_container').innerHTML = html;
    })
    .catch(console.error);
}


function delete_game(id) {
  fetch(`${BASE_URL}/api/v1/games/${id}/`, {
    method: 'DELETE'
  })
  .then(() => {  // Ждем завершения
    refreshGameList();
  });
}

// Работа с модальным окном.

save_game.addEventListener('click', function(event) {
  event.preventDefault(); // Отменяем стандартное поведение кнопки submit
  create_game();
  refreshGameList();
  form.reset();  // <-- очищаем поля формы
  modal.style.display = 'none';
});

add_game_btn.onclick = openModal;
modal.onclick = closeModal;
function openModal() {
  modal.style.display = 'block';
}

function closeModal(event) {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
};

