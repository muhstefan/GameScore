// config.js должен быть настроен до этого файла
import { BASE_URL } from './config.js';

const form = document.getElementById('gameForm');
const modal = document.getElementById('myModal');
const infoModal = document.getElementById('gameInfoModal');
const gamesListContainer = document.getElementById('games_list_container');
// Глобальная переменная текущего пользователя
const UserId = window.currentUserId;

// --------- API слой ---------- //
class ApiProcessor {
  async fetchGameList(page = 1) {
    const response = await fetch(`/pages/me/games/list/?page=${page}`);
    if (!response.ok) throw new Error('Failed to fetch games');
    return await response.text();
  }

  async addGameToUser(game_id) {
    const response = await fetch(`${BASE_URL}/api/v1/users/me/games/${game_id}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error(`Failed to add game: ${response.status}`);
  }

  async removeGameFromUser(game_id) {
    const response = await fetch(`${BASE_URL}/api/v1/users/me/games/${game_id}/`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error(`Failed to remove game: ${response.status}`);
  }

  async fetchGenreNames() {
    const response = await fetch('/api/v1/users/me/genres/names/');
    if (!response.ok) throw new Error('Ошибка получения жанров');
    return await response.json();
  }

    async fetchUserGameDetails(game_id) {
    const response = await fetch(`/api/v1/users/me/games/${game_id}/`);
    if (!response.ok) throw new Error('Ошибка получения информации об игре');
    return await response.json();
  }

}



// --------- Бизнес-логика ---------- //
class BusinessLogic {
  constructor(apiProcessor) {
    this.apiProcessor = apiProcessor;
    this.eventProcessor = null;
  }

  setEventProcessor(eventProcessor) {
    this.eventProcessor = eventProcessor;
  }

  async refreshGameList(page = 1) {
    try {
      const html = await this.apiProcessor.fetchGameList(page);
      gamesListContainer.innerHTML = html;
      this.attachPaginationHandlers();
    } catch (error) {
      console.error('Error refreshing game list:', error);
      gamesListContainer.innerHTML = '<div class="error">Ошибка загрузки игр</div>';
    }
  }

  async addGame(game_id) {
    await this.apiProcessor.addGameToUser(game_id);
    await this.refreshGameList();
  }

    async GameDetails(game_id) {
    return await this.apiProcessor.fetchUserGameDetails(game_id);
  }

  async removeGame(game_id) {
    await this.apiProcessor.removeGameFromUser(game_id);
    await this.refreshGameList();
  }

  async getGenreNames() {
    return await this.apiProcessor.fetchGenreNames();
  }

  async populateGenresSelect() {
    const select = document.getElementById('genres_select');
    select.innerHTML = "";
    try {
      const genreNames = await this.getGenreNames();
      genreNames.forEach(name => {
        const opt = document.createElement('option');
        opt.value = name;
        opt.textContent = name;
        select.appendChild(opt);
      });
    } catch (e) {
      select.innerHTML = '<option disabled>Ошибка загрузки жанров</option>';
    }
  }

  attachPaginationHandlers() {
    const paginationButtons = document.querySelectorAll('.pagination-button');
    paginationButtons.forEach(button => {
      button.onclick = (event) => {
        event.preventDefault();
        const page = parseInt(button.dataset.page);
        if (!isNaN(page)) {
          this.refreshGameList(page);
        }
      };
    });
  }
}

// --------- UI/Events слой ---------- //
class EventProcessor {
  constructor(businessLogic) {
    this.businessLogic = businessLogic;

    gamesListContainer.addEventListener('click', (event) => {
      // Сначала проверяем, был ли клик по кнопке (любому вложенному button)
      const btn = event.target.closest('button');
      if (btn && gamesListContainer.contains(btn)) {
        const id = btn.dataset.id;
        const action = btn.dataset.action;

        if (action === 'edit' && id) {
          this.editGame(id);
        } else if (action === 'remove_game' && id) {
          this.businessLogic.removeGame(id);
        }
        return; // если обработали кнопку, прерываем дальше
      }

      // Если клик был не по кнопке, проверяем, был ли клик по самой плитке
      const tile = event.target.closest('.game-tile');
      if (tile && gamesListContainer.contains(tile)) {
        const id = tile.dataset.id;
        this.onGameTileClick(id, tile, event); // реализуй этот метод ниже
        return;
      }
    });

    // Закрывание модального окна по клику вне формы
    modal.addEventListener('click', this.closeModal.bind(this));
    infoModal.addEventListener('click', this.closeModal.bind(this));
  }

  async onGameTileClick(game_id, tile, event) {
    try {
      const data = await this.businessLogic.GameDetails(game_id);
      // data - UserGameRead, data.game - GameRead

      document.getElementById('info_game_title').textContent = data.game?.name || 'Информация об игре';

      // Жанры: если genres — массив строк, иначе массив объектов с name
      let genres = [];
      if (Array.isArray(data.genres)) {
        genres = data.genres;
      } else if (Array.isArray(data.game?.genres)) {
        // если genres вложены в game
        genres = data.game.genres.map(g => g.name || g);
      }
      document.getElementById('info_game_genres').textContent = genres.join(', ');

      // Ревью: data.review или data.game.description
      document.getElementById('info_game_review').textContent = data.review || data.game?.description || '(нет ревью)';

      // Оценка
      document.getElementById('info_game_rating').textContent = data.rating ?? '-';

      // Статус
      const statusLabel = (s) => {
        if (s === 'done') return 'Пройдено';
        if (s === 'wait') return 'В ожидании';
        return s || '-';
      };
      document.getElementById('info_game_status').textContent = statusLabel(data.status);

      document.getElementById('gameInfoModal').style.display = 'block';
    } catch (error) {
      alert(error.message || 'Ошибка загрузки информации об игре');
    }
  }


  async openModal() {
    await this.businessLogic.populateGenresSelect();
    modal.style.display = 'block';
  }

closeModal(event) {
  // Закрытие модального окна для формы
  if (event.target === modal) {
    form.reset();
    delete form.dataset.editingId;
    modal.style.display = 'none';
    return;
  }

  // Закрытие инфо-модального окна
  if (event.target === infoModal) {
    infoModal.style.display = 'none';
    return;
  }
}

  editGame(id) {
    // Можно добавить логику заполнения формы для редактирования
    console.log(`Game ${id} НАЖАТА РЕД.`);
    // form.dataset.editingId = id;
    this.openModal();
  }

}



// --------- Инициализация ---------- //
const apiProcessor = new ApiProcessor();
const businessLogic = new BusinessLogic(apiProcessor);
const eventProcessor = new EventProcessor(businessLogic);
businessLogic.setEventProcessor(eventProcessor);

businessLogic.refreshGameList();
