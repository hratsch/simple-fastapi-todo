<script>
	import { onMount } from 'svelte';
	let todos = [];
	let newTitle = '';
	const API_URL = 'http://localhost:8000'; // backend

	async function loadTodos() {
		const res = await fetch(`${API_URL}/todos`);
		todos = await res.json();
	}

	async function addTodo() {
		if (!newTitle) return;
		const res = await fetch(`${API_URL}/todos`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ title: newTitle, completed: false })
		});
		if (res.ok) {
			newTitle = '';
			loadTodos();
		}
	}

	async function toggleTodo(id, completed) {
		const res = await fetch(`${API_URL}/todos/${id}`, {
			method: 'PUT',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ title: todos.find(t => t.id === id).title, completed: !completed})
		});
		if (res.ok) loadTodos();
	}

	async function deleteTodo(id) {
		await fetch(`${API_URL}/todos/${id}`, { method: 'DELETE' });
		loadTodos();
	}

	onMount(loadTodos);
</script>

<main>
	<h1>My Todos</h1>
	<div>
		<input bind:value={newTitle} placeholder="New todo..." on:keydown={(e) => e.key === 'Enter' && addTodo()} />
		<button on:click={addTodo}>Add</button>
	</div>
	<ul>
		{#each todos as todo}
			<li>
				<input 
					type="checkbox" 
					bind:checked={todo.completed} 
					on:change={() => toggleTodo(todo.id, todo.completed)} 
				/>
			<span class:done={todo.completed}>{todo.title}</span>
			<button on:click={() => deleteTodo(todo.id)}>Delete</button>
		</li>
		{/each}
	</ul>
</main>

<style>
	.done {
		text-decoration: line-through;
		opacity: 0.6;
	}
	li {
		display: flex;
		align-items: center;
		gap: 10px;
		margin: 5px 0;
	}
</style>