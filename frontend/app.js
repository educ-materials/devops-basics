const API_URL = "https://devops-basics-l2bn.onrender.com/api/tasks";

// const API_URL = "http://localhost:8000/api/tasks";

const form = document.getElementById("task-form");
const input = document.getElementById("task-input");
const list = document.getElementById("task-list");


// -----------------------------
// Get tasks from the backend
// -----------------------------

async function loadTasks() {

    const response = await fetch(API_URL);

    if (!response.ok) {
        throw new Error("Failed to load tasks");
    }

    const tasks = await response.json();

    renderTasks(tasks);
}


// -----------------------------
// Display tasks
// -----------------------------

function renderTasks(tasks) {

    list.innerHTML = "";

    tasks.forEach((task) => {

        const li = document.createElement("li");

        li.innerHTML = `
            <span>${task.title}</span>

            <button onclick="deleteTask(${task.id})">
                Delete
            </button>
        `;

        list.appendChild(li);
    });
}


// -----------------------------
// Create task
// -----------------------------

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const title = input.value.trim();

    if (!title) {
        return;
    }

    const response = await fetch(API_URL, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: title
        })
    });

    if (!response.ok) {
        throw new Error("Failed to create task");
    }

    input.value = "";

    loadTasks();
});


// -----------------------------
// Delete task
// -----------------------------

async function deleteTask(id) {

    const response = await fetch(`${API_URL}/${id}`, {

        method: "DELETE"
    });

    if (!response.ok) {
        throw new Error("Failed to delete task");
    }

    loadTasks();
}


// -----------------------------
// Initial load
// -----------------------------

loadTasks();