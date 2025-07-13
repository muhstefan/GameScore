const containers = document.querySelectorAll('.game-container');
const modal = document.getElementById('myModal');
const add_game_btn = document.getElementById('add_game');
const save_game = document.getElementById('save_game');
const form = document.getElementById('gameForm');
const formData = new FormData(form);
const gamesListContainer = document.getElementById('games_list_container');
import { BASE_URL } from './config.js';


class ApiProcessor {

  setEventProcessor(eventProcessor) {
    this.EventProcessor = eventProcessor;
  }

    refreshGameList(page = 1) {
      fetch(`/pages/games/list/?page=${page}`)
        .then(response => response.text())
        .then(html => {
          document.getElementById('games_list_container').innerHTML = html;
          this.EventProcessor.attachPaginationHandlers(); // Навесить обработчики на новые кнопки пагинации
        })
        .catch(console.error);
    }

  delete_game(id) {
    fetch(`${BASE_URL}/api/v1/games/${id}/`, {
      method: 'DELETE'
    })
    .then(() => {  // Ждем завершения
      this.refreshGameList();
    });
  }

  async create_game() {
    const data = this.get_input_data();
    const response = await fetch(`${BASE_URL}/api/v1/games/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  async update_game(id) {
    const data = this.get_input_data();
    const response = await fetch(`${BASE_URL}/api/v1/games/${id}/`, {
      method: 'PUT', // или PATCH
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  edit_game(id) {
    form.dataset.editingId = id;
    fetch(`${BASE_URL}/api/v1/games/${id}/`)
      .then(response => response.json())
      .then(game => {
        // Заполняем форму
        form.elements['title'].value = game.name;
        form.elements['description'].value = game.description;
        form.elements['rating'].value = game.rating;

        this.EventProcessor.openModal();
      });
  }


  get_input_data() {
    const formData = new FormData(form); // создаём здесь, чтобы получить актуальные данные

    const data = {
      name: formData.get('title').trim(),
      description: formData.get('description').trim(),
      rating: parseFloat(formData.get('rating'))
    };
    return data;
  }
}


class BusinessLogic {

  constructor(apiProcessor) {
    this.apiProcessor = apiProcessor;

    // Назначаем обработчик на кнопку save_game
    save_game.addEventListener('click', async (event) => {
      event.preventDefault(); // Отменяем стандартное поведение кнопки submit
      const id = form.dataset.editingId; // Проверяем, есть ли id редактируемой игры
      if (id) {
        await this.apiProcessor.update_game(id);
      } else {
        await this.apiProcessor.create_game();
      }
      form.reset();  //Очистка полей
      delete form.dataset.editingId; // Сброс editingId
      await this.apiProcessor.refreshGameList();
      modal.style.display = 'none';
    });
  }
}


class EventProcessor {
  constructor(apiProcessor, businessLogic) {
    this.apiProcessor = apiProcessor;
    this.businessLogic = businessLogic;

    gamesListContainer.addEventListener('click', (event) => {
      const btn = event.target.closest('button');
      if (!btn) return;

      const id = btn.dataset.id;
      const action = btn.dataset.action;

      if (!id || !action) return;

      if (action === 'delete') {
        this.apiProcessor.delete_game(id);
      } else if (action === 'edit') {
        this.apiProcessor.edit_game(id);
      }
    });

    add_game_btn.onclick = this.openModal.bind(this);
    modal.onclick = this.closeModal.bind(this);
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

  openModal() {
    modal.style.display = 'block';
  }

  closeModal(event) {
    if (event.target === modal) {
      form.reset();
      delete form.dataset.editingId;
      modal.style.display = 'none';
    }
  }
}



// --- Инициализация ---

const apiProcessor = new ApiProcessor();
const businessLogic = new BusinessLogic(apiProcessor);
const eventProcessor = new EventProcessor(apiProcessor, businessLogic);
apiProcessor.setEventProcessor(eventProcessor);
apiProcessor.refreshGameList();
