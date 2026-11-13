/**
 * TaskPro Dashboard Logic
 */

let currentFilters = {
    search: "",
    status: "all",
    priority: "",
    ordering: "due_date"
};

let debounceTimer = null;
let taskToDeleteId = null;

// Auth check on load
if (!api.isAuthenticated()) {
    window.location.replace("/login/");
}

document.addEventListener("DOMContentLoaded", () => {
    initUser();
    loadStats();
    loadTasks();
});

/**
 * Initialize current user greeting & avatar
 */
async function initUser() {
    const userRes = await api.getMe();
    if (userRes.ok && userRes.data) {
        const user = userRes.data;
        const name = user.username || "User";
        document.getElementById("user-display-name").textContent = name;
        document.getElementById("user-avatar").textContent = name.charAt(0).toUpperCase();
    }
}

/**
 * Handle user logout
 */
function handleLogout() {
    api.logout();
}

/**
 * Load dashboard statistics
 */
async function loadStats() {
    try {
        const res = await api.getStats();
        if (res.ok && res.data) {
            const stats = res.data;
            document.getElementById("stat-total").textContent = stats.total || 0;
            document.getElementById("stat-pending").textContent = stats.pending || 0;
            document.getElementById("stat-completed").textContent = stats.completed || 0;
            document.getElementById("stat-high").textContent = stats.high_priority || 0;
        }
    } catch (e) {
        console.error("Failed to load stats", e);
    }
}

/**
 * Load tasks list from API with current filters
 */
async function loadTasks() {
    const container = document.getElementById("tasks-container");
    const emptyState = document.getElementById("empty-state");
    const loadingState = document.getElementById("tasks-loading");

    loadingState.classList.remove("hidden");
    emptyState.classList.add("hidden");

    try {
        const res = await api.getTasks(currentFilters);
        loadingState.classList.add("hidden");

        if (!res.ok) {
            container.innerHTML = `
                <div class="p-6 bg-red-50 text-red-700 rounded-2xl border border-red-200 text-sm font-medium">
                    Failed to load tasks. Please refresh or check connection.
                </div>
            `;
            return;
        }

        const tasks = res.data;
        if (!tasks || tasks.length === 0) {
            // Remove previous cards except loading skeleton
            container.innerHTML = "";
            container.appendChild(loadingState);
            emptyState.classList.remove("hidden");
            
            // Contextual empty message
            const emptyMsg = document.getElementById("empty-state-msg");
            if (currentFilters.search) {
                emptyMsg.textContent = `No tasks matching "${currentFilters.search}".`;
            } else if (currentFilters.status !== "all") {
                emptyMsg.textContent = `No ${currentFilters.status} tasks found.`;
            } else {
                emptyMsg.textContent = "You don't have any tasks yet. Create your first task to get started!";
            }
            return;
        }

        emptyState.classList.add("hidden");
        container.innerHTML = "";
        container.appendChild(loadingState);

        tasks.forEach(task => {
            const card = renderTaskCard(task);
            container.appendChild(card);
        });

    } catch (e) {
        loadingState.classList.add("hidden");
        console.error("Error loading tasks", e);
    }
}

/**
 * Format due date and overdue status
 */
function getDueDateBadge(dueDateStr, isCompleted) {
    if (!dueDateStr) return "";

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const parts = dueDateStr.split("-");
    const dueDate = new Date(parts[0], parts[1] - 1, parts[2]);
    dueDate.setHours(0, 0, 0, 0);

    const diffDays = Math.round((dueDate - today) / (1000 * 60 * 60 * 24));

    let label = dueDateStr;
    const options = { month: "short", day: "numeric", year: "numeric" };
    label = dueDate.toLocaleDateString(undefined, options);

    if (diffDays === 0) {
        label = `Due Today (${label})`;
    } else if (diffDays === 1) {
        label = `Due Tomorrow (${label})`;
    } else if (diffDays === -1) {
        label = `Yesterday (${label})`;
    }

    if (isCompleted) {
        return `
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-500">
                <i class="fa-regular fa-calendar text-[11px]"></i>
                ${label}
            </span>
        `;
    }

    if (diffDays < 0) {
        // Overdue!
        return `
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-100 text-rose-700 animate-pulse">
                <i class="fa-solid fa-triangle-exclamation text-[11px]"></i>
                Overdue: ${label}
            </span>
        `;
    } else if (diffDays === 0) {
        // Due today
        return `
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800">
                <i class="fa-regular fa-clock text-[11px]"></i>
                ${label}
            </span>
        `;
    } else {
        return `
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-600">
                <i class="fa-regular fa-calendar text-[11px]"></i>
                ${label}
            </span>
        `;
    }
}

/**
 * Render single Task card
 */
function renderTaskCard(task) {
    const card = document.createElement("div");
    card.id = `task-card-${task.id}`;
    const isCompleted = task.status === "completed";

    card.className = `p-4 sm:p-5 rounded-2xl border transition-all duration-200 bg-white hover:shadow-md ${
        isCompleted 
            ? "border-slate-200/60 bg-slate-50/50 opacity-90" 
            : "border-slate-200 hover:border-indigo-300"
    }`;

    // Priority badge HTML
    let priorityBadge = "";
    if (task.priority === "high") {
        priorityBadge = `<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider bg-rose-50 text-rose-700 border border-rose-200/80">
            <i class="fa-solid fa-fire text-[10px]"></i> High
        </span>`;
    } else if (task.priority === "medium") {
        priorityBadge = `<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider bg-amber-50 text-amber-700 border border-amber-200/80">
            <i class="fa-solid fa-flag text-[10px]"></i> Medium
        </span>`;
    } else {
        priorityBadge = `<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-200/80">
            <i class="fa-solid fa-arrow-down text-[10px]"></i> Low
        </span>`;
    }

    // Status badge HTML
    const statusBadge = isCompleted
        ? `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800">
            <i class="fa-solid fa-check text-[10px]"></i> Completed
           </span>`
        : `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-indigo-50 text-indigo-700">
            <i class="fa-regular fa-clock text-[10px]"></i> Pending
           </span>`;

    const dueDateBadge = getDueDateBadge(task.due_date, isCompleted);

    card.innerHTML = `
        <div class="flex items-start gap-3.5">
            <!-- Complete Checkbox Button -->
            <button 
                onclick="toggleTaskStatus(${task.id})"
                title="${isCompleted ? 'Mark as Pending' : 'Mark as Complete'}"
                class="mt-1 flex-shrink-0 w-6 h-6 rounded-lg border-2 flex items-center justify-center transition-all ${
                    isCompleted 
                        ? 'bg-emerald-600 border-emerald-600 text-white shadow-sm shadow-emerald-200' 
                        : 'border-slate-300 hover:border-indigo-600 text-transparent hover:text-indigo-400 bg-white'
                }"
            >
                <i class="fa-solid fa-check text-xs"></i>
            </button>

            <!-- Task Info Body -->
            <div class="flex-grow min-w-0">
                <div class="flex flex-wrap items-center gap-2 mb-1.5">
                    ${priorityBadge}
                    ${statusBadge}
                    ${dueDateBadge}
                </div>

                <h4 class="text-base font-semibold text-slate-800 break-words ${isCompleted ? 'line-through text-slate-400' : ''}">
                    ${escapeHtml(task.title)}
                </h4>

                ${task.description ? `
                    <p class="text-xs text-slate-500 mt-1 whitespace-pre-line leading-relaxed ${isCompleted ? 'text-slate-400' : ''}">
                        ${escapeHtml(task.description)}
                    </p>
                ` : ""}
            </div>

            <!-- Action Buttons: Edit & Delete -->
            <div class="flex items-center gap-1 flex-shrink-0 ml-2">
                <button 
                    onclick="openEditModal(${task.id})" 
                    title="Edit Task"
                    class="p-2 rounded-xl text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 transition-colors"
                >
                    <i class="fa-regular fa-pen-to-square text-sm"></i>
                </button>
                <button 
                    onclick="openDeleteModal(${task.id}, '${escapeQuote(task.title)}')" 
                    title="Delete Task"
                    class="p-2 rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                >
                    <i class="fa-regular fa-trash-can text-sm"></i>
                </button>
            </div>
        </div>
    `;

    return card;
}

/**
 * Filter Handlers
 */
function setStatusFilter(status) {
    currentFilters.status = status;
    
    // Update tabs UI
    document.querySelectorAll(".status-tab").forEach(tab => {
        tab.className = "status-tab px-4 py-2 rounded-lg transition-all hover:text-slate-800 text-slate-600";
    });
    const activeTab = document.getElementById(`tab-${status}`);
    if (activeTab) {
        activeTab.className = "status-tab px-4 py-2 rounded-lg transition-all bg-white text-indigo-600 shadow-sm font-semibold";
    }

    loadTasks();
}

function handleSearchInput(e) {
    const val = e.target.value;
    const clearBtn = document.getElementById("clear-search-btn");
    
    if (val.trim()) {
        clearBtn.classList.remove("hidden");
    } else {
        clearBtn.classList.add("hidden");
    }

    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        currentFilters.search = val.trim();
        loadTasks();
    }, 300);
}

function clearSearch() {
    const searchInput = document.getElementById("search-input");
    searchInput.value = "";
    document.getElementById("clear-search-btn").classList.add("hidden");
    currentFilters.search = "";
    loadTasks();
}

function handlePriorityChange(e) {
    currentFilters.priority = e.target.value;
    loadTasks();
}

function handleSortChange(e) {
    currentFilters.ordering = e.target.value;
    loadTasks();
}

/**
 * Toggle Task Completion
 */
async function toggleTaskStatus(id) {
    try {
        const res = await api.toggleTask(id);
        if (res.ok) {
            const isDone = res.data.status === "completed";
            api.showToast(isDone ? "Task completed! 🎉" : "Task marked pending.", "success");
            loadStats();
            loadTasks();
        } else {
            api.showToast("Failed to update status", "error");
        }
    } catch (e) {
        api.showToast("Network error updating task", "error");
    }
}

/**
 * Modal Handling (Create & Edit)
 */
function openCreateModal() {
    document.getElementById("task-form").reset();
    document.getElementById("task-id").value = "";
    document.getElementById("modal-title").textContent = "Create New Task";
    document.getElementById("modal-icon").className = "fa-solid fa-plus";
    document.getElementById("modal-submit-text").textContent = "Create Task";
    document.getElementById("modal-alert").classList.add("hidden");

    // Set default due date to today
    const today = new Date().toISOString().split("T")[0];
    document.getElementById("task-due-date").value = today;
    document.getElementById("task-priority").value = "medium";
    document.getElementById("task-status").value = "pending";

    document.getElementById("task-modal").classList.remove("hidden");
    document.getElementById("task-title").focus();
}

async function openEditModal(id) {
    document.getElementById("modal-alert").classList.add("hidden");
    try {
        const res = await api.getTask(id);
        if (!res.ok) {
            api.showToast("Could not fetch task details", "error");
            return;
        }

        const task = res.data;
        document.getElementById("task-id").value = task.id;
        document.getElementById("task-title").value = task.title;
        document.getElementById("task-description").value = task.description || "";
        document.getElementById("task-due-date").value = task.due_date;
        document.getElementById("task-priority").value = task.priority;
        document.getElementById("task-status").value = task.status;

        document.getElementById("modal-title").textContent = "Edit Task";
        document.getElementById("modal-icon").className = "fa-regular fa-pen-to-square";
        document.getElementById("modal-submit-text").textContent = "Save Changes";

        document.getElementById("task-modal").classList.remove("hidden");
        document.getElementById("task-title").focus();
    } catch (e) {
        api.showToast("Network error loading task", "error");
    }
}

function closeModal() {
    document.getElementById("task-modal").classList.add("hidden");
}

async function handleTaskSubmit(e) {
    e.preventDefault();
    const id = document.getElementById("task-id").value;
    const title = document.getElementById("task-title").value.trim();
    const description = document.getElementById("task-description").value.trim();
    const due_date = document.getElementById("task-due-date").value;
    const priority = document.getElementById("task-priority").value;
    const status = document.getElementById("task-status").value;

    if (!title) {
        showModalError("Task title is required.");
        return;
    }
    if (!due_date) {
        showModalError("Due date is required.");
        return;
    }

    const payload = { title, description, due_date, priority, status };
    const submitBtn = document.getElementById("modal-submit-btn");
    const submitText = document.getElementById("modal-submit-text");
    const spinner = document.getElementById("modal-submit-spinner");

    submitBtn.disabled = true;
    spinner.classList.remove("hidden");

    try {
        let res;
        if (id) {
            res = await api.updateTask(id, payload);
        } else {
            res = await api.createTask(payload);
        }

        if (res.ok) {
            closeModal();
            api.showToast(id ? "Task updated successfully!" : "Task created successfully!", "success");
            loadStats();
            loadTasks();
        } else {
            let errorMsg = "Failed to save task. Please check the inputs.";
            if (res.data) {
                if (res.data.title) errorMsg = `Title: ${res.data.title[0]}`;
                else if (res.data.due_date) errorMsg = `Due Date: ${res.data.due_date[0]}`;
                else if (res.data.detail) errorMsg = res.data.detail;
            }
            showModalError(errorMsg);
        }
    } catch (err) {
        showModalError("Server communication error. Please try again.");
    } finally {
        submitBtn.disabled = false;
        spinner.classList.add("hidden");
    }
}

function showModalError(msg) {
    const alert = document.getElementById("modal-alert");
    const alertMsg = document.getElementById("modal-alert-msg");
    alertMsg.textContent = msg;
    alert.classList.remove("hidden");
}

/**
 * Delete Modal Handlers
 */
function openDeleteModal(id, title) {
    taskToDeleteId = id;
    document.getElementById("delete-task-title").textContent = title;
    document.getElementById("delete-modal").classList.remove("hidden");
}

function closeDeleteModal() {
    taskToDeleteId = null;
    document.getElementById("delete-modal").classList.add("hidden");
}

async function confirmDelete() {
    if (!taskToDeleteId) return;

    const btn = document.getElementById("confirm-delete-btn");
    btn.disabled = true;
    btn.textContent = "Deleting...";

    try {
        const res = await api.deleteTask(taskToDeleteId);
        if (res.ok || res.status === 204) {
            api.showToast("Task deleted successfully.", "success");
            closeDeleteModal();
            loadStats();
            loadTasks();
        } else {
            api.showToast("Failed to delete task.", "error");
        }
    } catch (e) {
        api.showToast("Network error deleting task.", "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "Delete";
    }
}

/**
 * String safety helpers
 */
function escapeHtml(str) {
    if (!str) return "";
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function escapeQuote(str) {
    if (!str) return "";
    return str.replace(/'/g, "\\'").replace(/"/g, "&quot;");
}
