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

  async updateUserGame(game_id, userGameUpdate) {
    const response = await fetch(`${BASE_URL}/api/v1/users/me/games/${game_id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userGameUpdate),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to update game ${game_id}: ${response.status} ${errorText}`);
    }

    return await response.json();
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
      const genres = await this.getGenreNames(); // [{id, name}, ...]
      genres.forEach(({ id, name }) => {
        const opt = document.createElement('option');
        opt.value = id;
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

  async updateUserGame(game_id, userGameUpdate) {
    return await this.apiProcessor.updateUserGame(game_id, userGameUpdate);
  }
}

// --------- UI/Events слой ---------- //
class EventProcessor {
  constructor(businessLogic) {
    this.businessLogic = businessLogic;

    gamesListContainer.addEventListener('click', (event) => {
      const btn = event.target.closest('button');
      if (btn && gamesListContainer.contains(btn)) {
        const id = btn.dataset.id;
        const action = btn.dataset.action;

        if (action === 'edit' && id) {
          this.openEditModal(id);
        } else if (action === 'remove_game' && id) {
          this.businessLogic.removeGame(id);
        }
        return;
      }

      const tile = event.target.closest('.game-tile');
      if (tile && gamesListContainer.contains(tile)) {
        const id = tile.dataset.id;
        this.onGameTileClick(id, tile, event);
        return;
      }
    });

    modal.addEventListener('click', this.closeModal.bind(this));
    infoModal.addEventListener('click', this.closeModal.bind(this));

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const gameId = form.dataset.editingId;
      if (!gameId) {
        alert('Ошибка: не указан id игры для обновления');
        return;
      }
      this.saveGame(gameId);
    });
  }

  async onGameTileClick(game_id, tile, event) {
    try {
      const data = await this.businessLogic.GameDetails(game_id);

      document.getElementById('info_game_title').textContent = data.game?.name || 'Информация об игре';

      let genres = [];
      if (Array.isArray(data.genres)) {
        genres = data.genres;
      } else if (Array.isArray(data.game?.genres)) {
        genres = data.game.genres.map(g => g.name || g);
      }
      document.getElementById('info_game_genres').textContent = genres.map(g => g.name).join(', ');

      document.getElementById('info_game_review').textContent = data.review || data.game?.description || '(нет ревью)';
      document.getElementById('info_game_rating').textContent = data.rating ?? '-';

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

  async openEditModal(id) {
    try {
      const data = await this.businessLogic.GameDetails(id);

      form.dataset.editingId = id;

      form.elements['status'].value = data.status || '';
      form.elements['rating'].value = data.rating !== null ? data.rating : '';
      form.elements['review'].value = data.review || '';

      const genresSelect = document.getElementById('genres_select');
      if (genresSelect) {
        const userGenreIds = data.genre_ids || (data.genres ? data.genres.map(g => g.id) : []);
        Array.from(genresSelect.options).forEach(opt => {
          opt.selected = userGenreIds.includes(parseInt(opt.value));
        });
      }

      await this.businessLogic.populateGenresSelect(); // Чтобы жанры были в селекте
      modal.style.display = 'block';
    } catch (error) {
      alert('Ошибка загрузки данных для редактирования: ' + error.message);
    }
  }

  async saveGame(id) {
    try {
      const status = form.elements['status']?.value || null;
      const ratingStr = form.elements['rating']?.value;
      const rating = ratingStr ? parseInt(ratingStr) : null;
      const review = form.elements['review']?.value || null;

      const genresSelect = document.getElementById('genres_select');
      let genre_ids = [];
      if (genresSelect) {
        genre_ids = Array.from(genresSelect.selectedOptions).map(opt => parseInt(opt.value));
      }

      const userGameUpdate = {};

      if (status) userGameUpdate.status = status;
      if (!isNaN(rating)) userGameUpdate.rating = rating;
      if (review) userGameUpdate.review = review;
      if (genre_ids.length > 0) userGameUpdate.genre_ids = genre_ids;

      if (Object.keys(userGameUpdate).length === 0) {
        alert('Нет данных для обновления');
        return;
      }

      await this.businessLogic.updateUserGame(id, userGameUpdate);

      modal.style.display = 'none';
      form.reset();
      delete form.dataset.editingId;

      await this.businessLogic.refreshGameList();

    } catch (error) {
      alert('Ошибка при сохранении игры: ' + (error.message || error));
      console.error(error);
    }
  }

  closeModal(event) {
    if (event.target === modal) {
      form.reset();
      delete form.dataset.editingId;
      modal.style.display = 'none';
      return;
    }

    if (event.target === infoModal) {
      infoModal.style.display = 'none';
      return;
    }
  }
}

// --------- Инициализация ---------- //
const apiProcessor = new ApiProcessor();
const businessLogic = new BusinessLogic(apiProcessor);
const eventProcessor = new EventProcessor(businessLogic);
businessLogic.setEventProcessor(eventProcessor);

businessLogic.refreshGameList();
