<script>
  import { onMount } from 'svelte';
  let todos = [];
  let newTitle = '';

  // Edit state
  let editingId = null;
  let editTitle = '';

  async function loadTodos() {
    try {
      const res = await fetch('http://localhost:8000/todos');
      if (res.ok) todos = await res.json();
    } catch (e) {
      console.error('Load failed:', e);
    }
  }

  async function addTodo() {
    if (!newTitle.trim()) return;
    await fetch('http://localhost:8000/todos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newTitle, completed: false })
    });
    newTitle = '';
    loadTodos();
  }

  async function toggleTodo(id, completed, title) {
    await fetch(`http://localhost:8000/todos/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, completed: !completed })
    });
    loadTodos();
  }

  async function deleteTodo(id) {
    await fetch(`http://localhost:8000/todos/${id}`, { method: 'DELETE' });
    loadTodos();
  }

  // Edit Mode
  function startEdit(id, title) {
    editingId = id;
    editTitle = title;
  }

  function cancelEdit() {
    editingId = null;
    editTitle = '';
  }

  async function saveEdit(id) {
    if (!editTitle.trim()) {
      cancelEdit();
      return;
    }
    await fetch(`http://localhost:8000/todos/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: editTitle })
    });
    cancelEdit();
    loadTodos();
  }

  onMount(loadTodos);
</script>

<main>
  <h1>Todo App</h1>

  <!-- Add New Todo -->
  <form on:submit|preventDefault={addTodo}>
    <input bind:value={newTitle} placeholder="What needs doing?" />
    <button type="submit">Add</button>
  </form>

  <!-- Todo List -->
  <ul class="todo-list">
    {#each todos as todo}
      <li class="todo-row">
        {#if editingId === todo.id}
          <!-- EDIT MODE -->
          <form on:submit|preventDefault={() => saveEdit(todo.id)} class="edit-form">
            <input
              bind:value={editTitle}
              on:keydown={(e) => e.key === 'Escape' && cancelEdit()}
              autofocus
              class="edit-input"
            />
            <button type="submit" class="small">Save</button>
            <button type="button" on:click={cancelEdit} class="small cancel">Cancel</button>
          </form>
        {:else}
          <!-- NORMAL MODE -->
          <label class="todo-main">
            <input
              type="checkbox"
              checked={todo.completed}
              on:change={() => toggleTodo(todo.id, todo.completed, todo.title)}
            />
            <span class="todo-text" class:done={todo.completed}>
              {todo.title}
            </span>
          </label>

          <div class="todo-actions">
            <button on:click={() => startEdit(todo.id, todo.title)} class="small">Edit</button>
            <button on:click={() => deleteTodo(todo.id)} class="small delete">×</button>
          </div>
        {/if}
      </li>
    {/each}
  </ul>
</main>

<style>
  :global(body) {
    background: #1a1a1a;
    color: #eee;
    margin: 0;
    font-family: system-ui, -apple-system, sans-serif;
  }

  main {
    max-width: 560px;
    margin: 2rem auto;
    padding: 0 1rem;
  }

  h1 {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    text-align: center;
    color: #fff;
  }

  /* Add Form */
  form {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
  }

  input:not([type="checkbox"]) {
    flex: 1;
    padding: 0.75rem;
    font-size: 1rem;
    background: #333;
    border: 1px solid #555;
    border-radius: 6px;
    color: #fff;
  }

  input::placeholder {
    color: #aaa;
  }

  button {
    padding: 0.75rem 1.2rem;
    background: #444;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 0.95rem;
    cursor: pointer;
    transition: background 0.2s;
  }

  button:hover {
    background: #555;
  }

  /* Todo List */
  .todo-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .todo-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.85rem 0;
    border-bottom: 1px solid #333;
    gap: 1rem;
  }

  .todo-main {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex: 1;
    min-width: 0;
  }

  .todo-main input[type="checkbox"] {
    width: 1.3rem;
    height: 1.3rem;
    margin: 0;
    cursor: pointer;
    accent-color: #9f72e6;
  }

  .todo-text {
    flex: 1;
    min-width: 0;
    font-size: 1rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #eee;
  }

  .todo-text.done {
    text-decoration: line-through;
    color: #888;
  }

  .todo-actions {
    display: flex;
    gap: 0.4rem;
    flex-shrink: 0;
  }

  .small {
    padding: 0.35rem 0.65rem;
    font-size: 0.8rem;
    background: #444;
    color: #ccc;
    border-radius: 4px;
  }

  .small:hover {
    background: #555;
  }

  .small.delete {
    background: #c33;
    color: white;
  }

  .small.delete:hover {
    background: #e44;
  }

  .small.cancel {
    background: #555;
    color: #aaa;
  }

  /* Edit Mode */
  .edit-form {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    flex: 1;
  }

  .edit-input {
    flex: 1;
    padding: 0.5rem;
    font-size: 1rem;
    background: #444;
    border: 1px solid #666;
    border-radius: 4px;
    color: #fff;
  }

  /* Responsive */
  @media (max-width: 500px) {
    .todo-row {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.75rem;
    }
    .todo-actions,
    .edit-form {
      align-self: stretch;
    }
    .edit-form {
      flex-direction: column;
    }
    .edit-input,
    .edit-form button {
      width: 100%;
    }
  }
</style>