// Dashboard JavaScript

let i18n = {};
let currentFeature = null;
let currentArtifact = null;
let refreshInterval = null;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadI18n();
    setupEventListeners();
    await loadFeatures();
    startAutoRefresh();
});

// Load i18n strings
async function loadI18n() {
    try {
        const response = await fetch('/api/i18n/current');
        i18n = await response.json();
        applyI18n();
    } catch (error) {
        console.error('Failed to load i18n:', error);
        // Fallback to English
        i18n = {
            title: 'Spec Mix Dashboard',
            features: 'Features',
            kanban: 'Kanban Board',
            constitution: 'Constitution',
            no_features: 'No features found',
            lanes: {
                planned: 'Planned',
                doing: 'Doing',
                for_review: 'For Review',
                done: 'Done'
            }
        };
        applyI18n();
    }
}

// Apply i18n to UI
function applyI18n() {
    document.getElementById('page-title').textContent = i18n.title || 'Spec Mix Dashboard';
    document.getElementById('tab-features').querySelector('.tab-label').textContent = i18n.features || 'Features';
    document.getElementById('tab-constitution').querySelector('.tab-label').textContent = i18n.constitution || 'Constitution';
    document.getElementById('features-title').textContent = i18n.features || 'Features';
    document.getElementById('constitution-title').textContent = i18n.constitution || 'Constitution';
    document.getElementById('kanban-title').textContent = i18n.kanban || 'Kanban Board';

    // Lane titles
    document.getElementById('lane-planned').textContent = i18n.lanes?.planned || 'Planned';
    document.getElementById('lane-doing').textContent = i18n.lanes?.doing || 'Doing';
    document.getElementById('lane-for-review').textContent = i18n.lanes?.for_review || 'For Review';
    document.getElementById('lane-done').textContent = i18n.lanes?.done || 'Done';
}

// Setup event listeners
function setupEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    // Refresh button
    document.getElementById('refresh-btn').addEventListener('click', async () => {
        await loadFeatures();
        if (document.getElementById('constitution-view').classList.contains('active')) {
            await loadConstitution();
        }
    });

    // Back buttons
    document.getElementById('back-to-features').addEventListener('click', () => {
        window.history.back();
    });

    document.getElementById('back-from-artifact').addEventListener('click', () => {
        window.history.back();
    });

    // Modal close button
    document.getElementById('modal-close').addEventListener('click', () => {
        closeTaskModal();
    });

    // Close modal when clicking outside
    document.getElementById('task-modal').addEventListener('click', (e) => {
        if (e.target.id === 'task-modal') {
            closeTaskModal();
        }
    });

    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeTaskModal();
        }
    });

    // Handle browser back/forward buttons
    window.addEventListener('popstate', (event) => {
        if (event.state) {
            if (event.state.view === 'features') {
                showView('features-view');
                currentFeature = null;
                currentArtifact = null;
            } else if (event.state.view === 'kanban') {
                showKanban(event.state.featureId, false);
            } else if (event.state.view === 'artifact') {
                showArtifact(event.state.featureId, event.state.artifactName, false);
            }
        }
    });
}

// Switch tabs
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Show appropriate view
    if (tabName === 'features') {
        showView('features-view');
        loadFeatures();
        window.history.pushState({ view: 'features' }, '', '#features');
    } else if (tabName === 'constitution') {
        showView('constitution-view');
        loadConstitution();
        window.history.pushState({ view: 'constitution' }, '', '#constitution');
    }
}

// Show a specific view
function showView(viewId) {
    document.querySelectorAll('.tab-content').forEach(view => {
        view.style.display = 'none';
    });
    document.getElementById(viewId).style.display = 'block';
}

// Load features
async function loadFeatures() {
    const container = document.getElementById('features-list');
    container.innerHTML = '<p class="loading">Loading features...</p>';

    try {
        const response = await fetch('/api/features');
        const features = await response.json();

        updateLastUpdate();

        if (features.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>${i18n.no_features || 'No features found'}</h3>
                    <p>Create a feature using <code>/speckit.specify</code></p>
                </div>
            `;
            document.getElementById('features-stats').textContent = '';
            return;
        }

        // Update stats
        const totalTasks = features.reduce((sum, f) => sum + (f.total_tasks || 0), 0);
        document.getElementById('features-stats').textContent =
            `${features.length} feature${features.length !== 1 ? 's' : ''} • ${totalTasks} task${totalTasks !== 1 ? 's' : ''}`;

        // Render features
        container.innerHTML = features.map(feature => renderFeatureCard(feature)).join('');

        // Add click handlers
        document.querySelectorAll('.feature-card').forEach(card => {
            card.addEventListener('click', () => {
                const featureId = card.dataset.featureId;
                showKanban(featureId);
            });
        });

        // Add artifact click handlers
        document.querySelectorAll('.artifact-badge.available').forEach(badge => {
            badge.addEventListener('click', (e) => {
                e.stopPropagation();
                const featureId = badge.dataset.featureId;
                const artifactName = badge.dataset.artifact;
                showArtifact(featureId, artifactName);
            });
        });

    } catch (error) {
        console.error('Failed to load features:', error);
        container.innerHTML = '<p class="error">Failed to load features</p>';
    }
}

// Render feature card
function renderFeatureCard(feature) {
    const badges = [];
    if (feature.worktree) {
        badges.push(`<span class="feature-badge badge-worktree">Worktree: ${feature.worktree}</span>`);
    }

    const stats = [];
    if (feature.kanban_stats) {
        const { planned, doing, for_review, done } = feature.kanban_stats;
        if (planned > 0) stats.push(`<span class="stat">📋 ${planned} planned</span>`);
        if (doing > 0) stats.push(`<span class="stat">🔨 ${doing} doing</span>`);
        if (for_review > 0) stats.push(`<span class="stat">👀 ${for_review} review</span>`);
        if (done > 0) stats.push(`<span class="stat">✅ ${done} done</span>`);
    }

    const artifacts = Object.entries(feature.artifacts || {})
        .filter(([name, exists]) => exists && name !== 'kanban')
        .map(([name]) => `
            <span class="artifact-badge available"
                  data-feature-id="${feature.id}"
                  data-artifact="${name}.md">
                ${name}
            </span>
        `).join('');

    return `
        <div class="feature-card" data-feature-id="${feature.id}">
            <div class="feature-header">
                <div class="feature-name">${feature.name}</div>
                ${badges.join('')}
            </div>
            ${stats.length > 0 ? `<div class="feature-stats">${stats.join('')}</div>` : ''}
            ${artifacts ? `<div class="artifacts">${artifacts}</div>` : ''}
        </div>
    `;
}

// Show kanban board for feature
async function showKanban(featureId, pushState = true) {
    currentFeature = featureId;
    showView('kanban-view');

    // Add to browser history
    if (pushState) {
        window.history.pushState(
            { view: 'kanban', featureId: featureId },
            '',
            `#kanban/${featureId}`
        );
    }

    document.getElementById('kanban-title').textContent = `${i18n.kanban || 'Kanban Board'}: ${featureId}`;

    // Clear lanes
    ['planned', 'doing', 'for_review', 'done'].forEach(lane => {
        document.getElementById(`lane-${lane === 'for_review' ? 'for-review' : lane}-content`).innerHTML =
            '<p class="loading">Loading...</p>';
    });

    try {
        const response = await fetch(`/api/kanban/${featureId}`);
        const data = await response.json();

        // Render lanes
        Object.entries(data.lanes).forEach(([lane, tasks]) => {
            const containerId = `lane-${lane === 'for_review' ? 'for-review' : lane}-content`;
            const container = document.getElementById(containerId);

            if (tasks.length === 0) {
                container.innerHTML = '<p class="empty-state">No tasks</p>';
            } else {
                container.innerHTML = tasks.map(task => `
                    <div class="task-card" data-task-id="${task.id}" data-lane="${lane}">
                        <strong>${task.id}</strong>
                        <div>${task.title}</div>
                    </div>
                `).join('');
            }
        });

        // Add click handlers to task cards
        document.querySelectorAll('.task-card').forEach(card => {
            card.addEventListener('click', () => {
                const taskId = card.dataset.taskId;
                const lane = card.dataset.lane;
                openTaskModal(featureId, lane, taskId);
            });
        });

    } catch (error) {
        console.error('Failed to load kanban:', error);
    }
}

// Show artifact
async function showArtifact(featureId, artifactName, pushState = true) {
    currentFeature = featureId;
    currentArtifact = artifactName;
    showView('artifact-view');

    // Add to browser history
    if (pushState) {
        window.history.pushState(
            { view: 'artifact', featureId: featureId, artifactName: artifactName },
            '',
            `#artifact/${featureId}/${artifactName}`
        );
    }

    document.getElementById('artifact-title').textContent = `${featureId} / ${artifactName}`;
    document.getElementById('artifact-content').innerHTML = '<p class="loading">Loading...</p>';

    try {
        const response = await fetch(`/api/artifact/${featureId}/${artifactName}`);
        const content = await response.text();

        // Render markdown
        const html = marked.parse(content);
        document.getElementById('artifact-content').innerHTML = html;

    } catch (error) {
        console.error('Failed to load artifact:', error);
        document.getElementById('artifact-content').innerHTML = '<p class="error">Failed to load artifact</p>';
    }
}

// Load constitution
async function loadConstitution() {
    const container = document.getElementById('constitution-content');
    container.innerHTML = '<p class="loading">Loading constitution...</p>';

    try {
        const response = await fetch('/api/constitution');
        if (response.ok) {
            const content = await response.text();
            const html = marked.parse(content);
            container.innerHTML = html;
        } else {
            container.innerHTML = '<p class="empty-state">No constitution found. Create one with <code>/speckit.constitution</code></p>';
        }
    } catch (error) {
        console.error('Failed to load constitution:', error);
        container.innerHTML = '<p class="error">Failed to load constitution</p>';
    }
}

// Auto-refresh
function startAutoRefresh() {
    refreshInterval = setInterval(async () => {
        // Only auto-refresh features view
        if (document.getElementById('features-view').classList.contains('active')) {
            await loadFeatures();
        }
    }, 2000); // 2 seconds
}

// Update last update time
function updateLastUpdate() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString();
    document.getElementById('last-update').textContent = `Updated: ${timeStr}`;
}

// Open task detail modal
async function openTaskModal(featureId, lane, taskId) {
    const modal = document.getElementById('task-modal');
    const modalTitle = document.getElementById('modal-task-title');
    const modalBody = document.getElementById('modal-task-body');

    // Show modal
    modal.classList.add('show');
    modalTitle.textContent = taskId;
    modalBody.innerHTML = '<p class="loading">Loading task details...</p>';

    try {
        const response = await fetch(`/api/task/${featureId}/${lane}/${taskId}`);

        if (!response.ok) {
            throw new Error('Task not found');
        }

        const taskData = await response.json();

        // Update modal title
        modalTitle.textContent = `${taskData.id}: ${taskData.title}`;

        // Render markdown content
        const html = marked.parse(taskData.content);
        modalBody.innerHTML = html;

    } catch (error) {
        console.error('Failed to load task detail:', error);
        modalBody.innerHTML = '<p class="error">Failed to load task details</p>';
    }
}

// Close task detail modal
function closeTaskModal() {
    const modal = document.getElementById('task-modal');
    modal.classList.remove('show');
}

// Cleanup on unload
window.addEventListener('beforeunload', () => {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});
