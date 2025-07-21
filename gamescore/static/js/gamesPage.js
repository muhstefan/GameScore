const gamesListContainer = document.getElementById('games_list_container');

// Допустим, глобальная переменная с id пользователя
const UserId = window.currentUserId;

import { BASE_URL } from './config.js';

class ApiProcessor {
    constructor() {
    this.currentPage = 1; // текущая страница по умолчанию
  }

  async refreshGameList(page = 1) {
    try {
      const response = await fetch(`/pages/games/list/?page=${page}`);
      const html = await response.text();
      gamesListContainer.innerHTML = html;
      this.EventProcessor?.attachPaginationHandlers();
      this.currentPage = page; // запоминаем текущую страницу
    } catch (error) {
      console.error('Error refreshing game list:', error);
    }
  }

  async add_game_to_user(game_id) {
    try {
      const response = await fetch(`${BASE_URL}/api/v1/users/me/games/${game_id}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
        // без body
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to add game: ${response.status} ${errorText}`);
      }

      console.log(`Game ${game_id} added to user`);

      // После успешного добавления обновляем список игр,
      // чтобы перерисовать кнопки

      await this.refreshGameList(this.currentPage);
      console.log(this.currentPage);
    } catch (error) {
      console.error(error);
    }
  }

  async remove_game_from_user(game_id) {
  try {
    const response = await fetch(`${BASE_URL}/api/v1/users/me/games/${game_id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to remove game: ${response.status} ${errorText}`);
    }

    await this.refreshGameList(this.currentPage);
    console.log(this.currentPage);

  } catch (error) {
    console.error(error);
  }
}


  setEventProcessor(eventProcessor) {
    this.EventProcessor = eventProcessor;
  }
}

class EventProcessor {
  constructor(apiProcessor) {
    this.apiProcessor = apiProcessor;

    gamesListContainer.addEventListener('click', (event) => {
      const btn = event.target.closest('button');
      if (!btn) return;

      const id = btn.dataset.id;
      const action = btn.dataset.action;

      if (action === 'add_game' && id) {
        this.apiProcessor.add_game_to_user(id);
      } else if (action === 'remove_game' && id) {
        this.apiProcessor.remove_game_from_user(id);
      }
    });
  }

  attachPaginationHandlers() {
    const paginationButtons = document.querySelectorAll('.pagination-button');
    paginationButtons.forEach(button => {
      button.onclick = (event) => {
        event.preventDefault();
        const page = parseInt(button.dataset.page);
        if (!isNaN(page)) {
          this.apiProcessor.refreshGameList(page);
        }
      };
    });
  }
}

// Инициализация
const apiProcessor = new ApiProcessor();
const eventProcessor = new EventProcessor(apiProcessor);
apiProcessor.setEventProcessor(eventProcessor);
apiProcessor.refreshGameList();
