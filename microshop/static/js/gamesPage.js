const containers = document.querySelectorAll('.game-container');
const modal = document.getElementById('myModal');
const add_game_btn = document.getElementById('add_game');
import { BASE_URL } from './config.js';


for (let i = 0; i < containers.length; i++) {
  const container = containers[i];
  const gameId = container.id.replace('container_', '');
  const gameData = games.find(g => String(g.id) === gameId);

  const editBtn = document.getElementById(`edit_game_${gameId}`);
  const deleteBtn = document.getElementById(`delete_game_${gameId}`);

  editBtn.onclick = function(event) {
    console.log('Кнопка нажата!');
  };  // <-- закрываем функцию обработчика

  // Если хотите, можно добавить обработчик для deleteBtn тоже:
  deleteBtn.onclick = function(event) {
    console.log('Кнопка удаления нажата!');
    delete_game(gameId)
  };
}  // <-- закрываем цикл for

function delete_game(id){
fetch(`${BASE_URL}/api/v1/games/${id}/`, {
  method: 'DELETE'
})
}

// Работа с модальным окном.

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

