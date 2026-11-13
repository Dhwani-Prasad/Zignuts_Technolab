/**
 * TaskPro API Client
 * Centralized Fetch API client with JWT token management, auto-refresh, and error handling.
 */

const API_BASE = "/api";

const storage = {
    getAccessToken() {
        return localStorage.getItem("taskpro_access_token");
    },
    getRefreshToken() {
        return localStorage.getItem("taskpro_refresh_token");
    },
    setTokens(access, refresh) {
        if (access) localStorage.setItem("taskpro_access_token", access);
        if (refresh) localStorage.setItem("taskpro_refresh_token", refresh);
    },
    clearTokens() {
        localStorage.removeItem("taskpro_access_token");
        localStorage.removeItem("taskpro_refresh_token");
        localStorage.removeItem("taskpro_user");
    },
    getUser() {
        const u = localStorage.getItem("taskpro_user");
        try {
            return u ? JSON.parse(u) : null;
        } catch {
            return null;
        }
    },
    setUser(user) {
        if (user) localStorage.setItem("taskpro_user", JSON.stringify(user));
    }
};

/**
 * Global Toast Notification System
 */
function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `pointer-events-auto transform transition-all duration-300 ease-out translate-x-12 opacity-0 flex items-center gap-3 p-3.5 rounded-xl shadow-lg border text-xs font-semibold ${
        type === "success" 
            ? "bg-white text-emerald-800 border-emerald-200" 
            : type === "error"
            ? "bg-white text-rose-800 border-rose-200"
            : "bg-white text-indigo-800 border-indigo-200"
    }`;

    const icon = type === "success" 
        ? '<i class="fa-solid fa-circle-check text-emerald-500 text-sm"></i>'
        : type === "error"
        ? '<i class="fa-solid fa-circle-exclamation text-rose-500 text-sm"></i>'
        : '<i class="fa-solid fa-circle-info text-indigo-500 text-sm"></i>';

    toast.innerHTML = `
        <div class="flex-shrink-0">${icon}</div>
        <div class="flex-grow">${message}</div>
        <button onclick="this.parentElement.remove()" class="text-slate-400 hover:text-slate-600 pl-2">
            <i class="fa-solid fa-xmark"></i>
        </button>
    `;

    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
        toast.classList.remove("translate-x-12", "opacity-0");
    });

    // Auto dismiss after 4 seconds
    setTimeout(() => {
        toast.classList.add("translate-x-12", "opacity-0");
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

/**
 * Fetch wrapper handling JWT header and automatic 401 refresh
 */
async function fetchWithAuth(url, options = {}) {
    options.headers = options.headers || {};
    
    // Set JSON content type if payload present
    if (options.body && !(options.body instanceof FormData)) {
        options.headers["Content-Type"] = "application/json";
    }

    let token = storage.getAccessToken();
    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    let response = await fetch(url, options);

    // If 401 Unauthorized, attempt refresh
    if (response.status === 401 && storage.getRefreshToken()) {
        const refreshed = await refreshAccessToken();
        if (refreshed) {
            token = storage.getAccessToken();
            options.headers["Authorization"] = `Bearer ${token}`;
            response = await fetch(url, options);
        } else {
            // Refresh failed: session expired
            storage.clearTokens();
            if (window.location.pathname !== "/login/" && window.location.pathname !== "/register/") {
                window.location.replace("/login/");
            }
            return { ok: false, status: 401, data: { detail: "Session expired. Please log in again." } };
        }
    }

    let data = null;
    try {
        const text = await response.text();
        data = text ? JSON.parse(text) : null;
    } catch (e) {
        data = null;
    }

    return {
        ok: response.ok,
        status: response.status,
        data: data
    };
}

/**
 * Refresh JWT token
 */
async function refreshAccessToken() {
    const refreshToken = storage.getRefreshToken();
    if (!refreshToken) return false;

    try {
        const res = await fetch(`${API_BASE}/auth/refresh/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh: refreshToken })
        });

        if (res.ok) {
            const data = await res.json();
            storage.setTokens(data.access, data.refresh || refreshToken);
            return true;
        }
    } catch (e) {
        console.error("Token refresh failed", e);
    }
    return false;
}

/**
 * API Methods
 */
const api = {
    // Auth helpers
    isAuthenticated() {
        return !!storage.getAccessToken();
    },

    getCurrentUser() {
        return storage.getUser();
    },

    async login(username, password) {
        const res = await fetch(`${API_BASE}/auth/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            storage.setTokens(data.access, data.refresh);
            // Fetch user profile immediately
            const userRes = await api.getMe();
            if (userRes.ok) {
                storage.setUser(userRes.data);
            }
            return { ok: true, data };
        }
        return { ok: false, data };
    },

    async register(username, email, password, passwordConfirm) {
        const res = await fetch(`${API_BASE}/auth/register/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username,
                email,
                password,
                password_confirm: passwordConfirm
            })
        });
        const data = await res.json();
        return { ok: res.ok, data };
    },

    logout() {
        storage.clearTokens();
        window.location.replace("/login/");
    },

    async getMe() {
        return await fetchWithAuth(`${API_BASE}/auth/me/`);
    },

    // Tasks API helpers
    async getTasks(params = {}) {
        const query = new URLSearchParams();
        if (params.search) query.append("search", params.search);
        if (params.status && params.status !== "all") query.append("status", params.status);
        if (params.priority) query.append("priority", params.priority);
        if (params.ordering) query.append("ordering", params.ordering);

        const qs = query.toString();
        const url = `${API_BASE}/tasks/${qs ? `?${qs}` : ""}`;
        return await fetchWithAuth(url);
    },

    async createTask(taskData) {
        return await fetchWithAuth(`${API_BASE}/tasks/`, {
            method: "POST",
            body: JSON.stringify(taskData)
        });
    },

    async getTask(id) {
        return await fetchWithAuth(`${API_BASE}/tasks/${id}/`);
    },

    async updateTask(id, taskData) {
        return await fetchWithAuth(`${API_BASE}/tasks/${id}/`, {
            method: "PUT",
            body: JSON.stringify(taskData)
        });
    },

    async patchTask(id, patchData) {
        return await fetchWithAuth(`${API_BASE}/tasks/${id}/`, {
            method: "PATCH",
            body: JSON.stringify(patchData)
        });
    },

    async deleteTask(id) {
        return await fetchWithAuth(`${API_BASE}/tasks/${id}/`, {
            method: "DELETE"
        });
    },

    async completeTask(id) {
        return await fetchWithAuth(`${API_BASE}/tasks/${id}/complete/`, {
            method: "PATCH"
        });
    },

    async toggleTask(id) {
        return await fetchWithAuth(`${API_BASE}/tasks/${id}/toggle/`, {
            method: "PATCH"
        });
    },

    async getStats() {
        return await fetchWithAuth(`${API_BASE}/tasks/stats/`);
    },

    showToast
};
