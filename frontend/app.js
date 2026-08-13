const API_URL = "https://devops-basics-l2bn.onrender.com/api/tasks";

// const API_URL = "http://localhost:8000/api/tasks";

const form = document.getElementById("task-form");
const input = document.getElementById("task-input");
const list = document.getElementById("task-list");


// -----------------------------
// Get tasks from the backend
// -----------------------------

async function loadTasks() {
    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const tasks = await response.json();

        renderTasks(tasks);

    } catch (error) {
        console.error("Failed to load tasks:", error);
    }
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

            <button onclick="editTask(${task.id}, '${escapeHtml(task.title)}')">
                Edit
            </button>

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

    try {

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
            throw new Error(`HTTP ${response.status}`);
        }

        input.value = "";

        await loadTasks();

    } catch (error) {
        console.error("Failed to create task:", error);
    }
});


// -----------------------------
// Edit task
// -----------------------------

async function editTask(id, currentTitle) {

    const newTitle = prompt("Edit task:", currentTitle);

    if (newTitle === null) {
        return;
    }

    const title = newTitle.trim();

    if (!title) {
        return;
    }

    try {

        const response = await fetch(`${API_URL}/${id}`, {

            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                title: title,
                completed: false
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        await loadTasks();

    } catch (error) {
        console.error("Failed to update task:", error);
    }
}


// -----------------------------
// Delete task
// -----------------------------

async function deleteTask(id) {

    try {

        const response = await fetch(`${API_URL}/${id}`, {

            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        await loadTasks();

    } catch (error) {
        console.error("Failed to delete task:", error);
    }
}


// -----------------------------
// Simple HTML escaping
// -----------------------------

function escapeHtml(value) {

    return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// -----------------------------
// Initial load
// -----------------------------

loadTasks();