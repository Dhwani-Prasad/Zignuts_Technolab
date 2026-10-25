const API = "/api";
const getToken = () => localStorage.getItem("taskpro_access");
const showMessage = (message, type = "success") => {
  const element = document.getElementById("message");
  if (!element) return;
  element.textContent = message;
  element.className = `alert alert-${type}`;
};
const hideMessage = () => {
  const element = document.getElementById("message");
  if (element) element.className = "alert d-none";
};
const apiRequest = async (path, options = {}) => {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (getToken()) headers.Authorization = `Bearer ${getToken()}`;
  const response = await fetch(`${API}${path}`, { ...options, headers });
  const raw = await response.text();
  let data = {};
  try { data = raw ? JSON.parse(raw) : {}; } catch { data = { detail: raw }; }
  if (!response.ok) {
    const message = typeof data === "object" ? Object.entries(data).map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(", ") : value}`).join(" | ") : "Request failed";
    throw new Error(message || "Request failed");
  }
  return data;
};

const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideMessage();
    try {
      const data = await apiRequest("/token/", {
        method: "POST",
        body: JSON.stringify({
          username: document.getElementById("username").value.trim(),
          password: document.getElementById("password").value
        })
      });
      localStorage.setItem("taskpro_access", data.access);
      localStorage.setItem("taskpro_refresh", data.refresh);
      window.location.href = "/dashboard/";
    } catch (error) {
      showMessage(error.message, "danger");
    }
  });
}

const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideMessage();
    try {
      await apiRequest("/register/", {
        method: "POST",
        body: JSON.stringify({
          username: document.getElementById("username").value.trim(),
          email: document.getElementById("email").value.trim(),
          password: document.getElementById("password").value
        })
      });
      showMessage("Account created. Redirecting to login...");
      setTimeout(() => window.location.href = "/", 900);
    } catch (error) {
      showMessage(error.message, "danger");
    }
  });
}

const taskFormPanel = document.getElementById("taskFormPanel");
if (taskFormPanel) {
  if (!getToken()) window.location.replace("/");
  const taskList = document.getElementById("taskList");
  const taskForm = document.getElementById("taskForm");

  const loadTasks = async () => {
    hideMessage();
    const params = new URLSearchParams();
    const status = document.getElementById("statusFilter").value;
    const search = document.getElementById("searchInput").value.trim();
    const priority = document.getElementById("priorityFilter").value;
    const ordering = document.getElementById("sortFilter").value;
    if (status !== "all") params.set("status", status);
    if (search) params.set("search", search);
    if (priority) params.set("priority", priority);
    if (ordering) params.set("ordering", ordering);
    try {
      const tasks = await apiRequest(`/tasks/?${params.toString()}`);
      taskList.replaceChildren();
      if (!tasks.length) {
        taskList.innerHTML = '<div class="col-12"><p class="text-secondary text-center py-4 mb-0">No tasks found. Add your first task.</p></div>';
        return;
      }
      tasks.forEach((task) => {
        const column = document.createElement("div");
        column.className = "col-md-6 col-xl-4";
        const card = document.createElement("article");
        card.className = "card h-100 border-0 shadow-sm";
        const body = document.createElement("div");
        body.className = "card-body";
        const title = document.createElement("h3");
        title.className = "h5";
        title.textContent = task.title;
        const description = document.createElement("p");
        description.className = "text-secondary";
        description.textContent = task.description || "No description";
        const meta = document.createElement("p");
        meta.className = "small mb-3";
        meta.textContent = `Due: ${task.due_date} · Priority: ${task.priority.toUpperCase()} · ${task.is_completed ? "Completed" : "Pending"}`;
        const actions = document.createElement("div");
        actions.className = "d-flex flex-wrap gap-2";
        const edit = document.createElement("button");
        edit.className = "btn btn-sm btn-outline-primary";
        edit.textContent = "Edit";
        edit.addEventListener("click", () => fillForm(task));
        const complete = document.createElement("button");
        complete.className = "btn btn-sm btn-outline-success";
        complete.textContent = task.is_completed ? "Mark pending" : "Complete";
        complete.addEventListener("click", async () => {
          try {
            await apiRequest(`/tasks/${task.id}/`, {
              method: "PATCH",
              body: JSON.stringify({ is_completed: !task.is_completed })
            });
            await loadTasks();
            showMessage("Task status updated.");
          } catch (error) { showMessage(error.message, "danger"); }
        });
        const remove = document.createElement("button");
        remove.className = "btn btn-sm btn-outline-danger";
        remove.textContent = "Delete";
        remove.addEventListener("click", async () => {
          if (!window.confirm(`Delete "${task.title}"?`)) return;
          try {
            await apiRequest(`/tasks/${task.id}/`, { method: "DELETE" });
            await loadTasks();
            showMessage("Task deleted.");
          } catch (error) { showMessage(error.message, "danger"); }
        });
        actions.append(edit, complete, remove);
        body.append(title, description, meta, actions);
        card.append(body);
        column.append(card);
        taskList.append(column);
      });
    } catch (error) {
      if (error.message.includes("token") || error.message.includes("credentials")) {
        localStorage.removeItem("taskpro_access");
        window.location.replace("/");
      } else {
        showMessage(error.message, "danger");
      }
    }
  };

  const fillForm = (task = null) => {
    taskFormPanel.classList.remove("d-none");
    document.getElementById("formHeading").textContent = task ? "Edit task" : "Add task";
    document.getElementById("taskId").value = task ? task.id : "";
    document.getElementById("title").value = task ? task.title : "";
    document.getElementById("description").value = task ? task.description : "";
    document.getElementById("due_date").value = task ? task.due_date : "";
    document.getElementById("priority").value = task ? task.priority : "medium";
    document.getElementById("is_completed").value = task ? String(task.is_completed) : "false";
    taskFormPanel.scrollIntoView({ behavior: "smooth" });
  };

  taskForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideMessage();
    const id = document.getElementById("taskId").value;
    const payload = {
      title: document.getElementById("title").value.trim(),
      description: document.getElementById("description").value.trim(),
      due_date: document.getElementById("due_date").value,
      priority: document.getElementById("priority").value,
      is_completed: document.getElementById("is_completed").value === "true"
    };
    try {
      await apiRequest(id ? `/tasks/${id}/` : "/tasks/", {
        method: id ? "PATCH" : "POST",
        body: JSON.stringify(payload)
      });
      taskForm.reset();
      document.getElementById("taskId").value = "";
      taskFormPanel.classList.add("d-none");
      await loadTasks();
      showMessage(id ? "Task updated successfully." : "Task created successfully.");
    } catch (error) {
      showMessage(error.message, "danger");
    }
  });

  document.getElementById("newTaskButton").addEventListener("click", () => fillForm());
  document.getElementById("cancelEditButton").addEventListener("click", () => taskFormPanel.classList.add("d-none"));
  ["statusFilter", "priorityFilter", "sortFilter"].forEach((id) => document.getElementById(id).addEventListener("change", loadTasks));
  let searchTimer;
  document.getElementById("searchInput").addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadTasks, 300);
  });
  document.getElementById("logoutButton").addEventListener("click", () => {
    localStorage.removeItem("taskpro_access");
    localStorage.removeItem("taskpro_refresh");
    window.location.href = "/";
  });
  loadTasks();
}
