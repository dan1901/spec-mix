// Dashboard JavaScript

let i18n = {};
let currentFeature = null;
let currentArtifact = null;
let refreshInterval = null;

// Get history state from URL hash
function getCurrentStateFromHash() {
    const hash = window.location.hash;

    if (hash.startsWith('#kanban/')) {
        return { view: 'kanban', featureId: hash.substring(8) };
    } else if (hash.startsWith('#artifact/')) {
        const parts = hash.substring(10).split('/');
        return { view: 'artifact', featureId: parts[0], artifactName: parts.slice(1).join('/') };
    } else if (hash === '#constitution') {
        return { view: 'constitution' };
    } else {
        return { view: 'features' };
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadI18n();
    setupEventListeners();
    await loadFeatures();

    // Restore state from URL hash
    const hash = window.location.hash;
    if (hash.startsWith('#kanban/')) {
        const featureId = hash.substring(8);
        switchTab('features');
        await showKanban(featureId, false);
    } else if (hash.startsWith('#artifact/')) {
        const parts = hash.substring(10).split('/');
        const featureId = parts[0];
        const artifactName = parts.slice(1).join('/');
        switchTab('features');
        await showArtifact(featureId, artifactName, false);
    } else if (hash === '#constitution') {
        switchTab('constitution');
    } else {
        // Default to features tab
        switchTab('features');
    }

    // Initialize browser history state for back/forward buttons
    window.history.replaceState(
        getCurrentStateFromHash(),
        '',
        window.location.hash || '#features'
    );

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
        // Use event.state if available, otherwise restore from hash
        const state = event.state || getCurrentStateFromHash();

        if (state.view === 'features') {
            switchTab('features');
            showView('features-view');
            loadFeatures();
            currentFeature = null;
            currentArtifact = null;
        } else if (state.view === 'kanban') {
            switchTab('features');
            showKanban(state.featureId, false);
        } else if (state.view === 'artifact') {
            switchTab('features');
            showArtifact(state.featureId, state.artifactName, false);
        } else if (state.view === 'constitution') {
            switchTab('constitution');
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
        // Use history state to restore previous view (not hash, which may be overwritten)
        const currentState = window.history.state;

        if (currentState && currentState.view === 'kanban') {
            showKanban(currentState.featureId, false);
        } else if (currentState && currentState.view === 'artifact') {
            showArtifact(currentState.featureId, currentState.artifactName, false);
        } else {
            // Default to features list
            showView('features-view');
            loadFeatures();
            window.history.pushState({ view: 'features' }, '', '#features');
        }

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
    const modalDetails = document.getElementById('modal-details');
    const modalCommits = document.getElementById('modal-commits');

    // Show modal
    modal.classList.add('show');
    modalTitle.textContent = taskId;
    modalDetails.innerHTML = '<p class="loading">Loading task details...</p>';

    // Reset tabs to Details
    document.querySelectorAll('.modal-tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.tab === 'details') tab.classList.add('active');
    });
    modalDetails.style.display = 'block';
    modalCommits.style.display = 'none';

    // Setup tab switching
    setupModalTabs(featureId, taskId);

    try {
        const response = await fetch(`/api/task/${featureId}/${lane}/${taskId}`);

        if (!response.ok) {
            throw new Error('Task not found');
        }

        const taskData = await response.json();

        // Update modal title
        modalTitle.textContent = `${taskData.id}: ${taskData.title}`;

        // Build HTML with dependencies
        let html = '';

        // Add dependencies section at the top if present
        if (taskData.dependencies && taskData.dependencies.length > 0) {
            html += '<div class="task-dependencies">';
            html += '<h3>📦 Dependencies</h3>';
            html += '<div class="dependency-links">';
            taskData.dependencies.forEach(dep => {
                html += `<a href="#" class="dependency-link" data-feature-id="${featureId}" data-lane="${dep.lane}" data-task-id="${dep.id}">${dep.id}</a>`;
            });
            html += '</div>';
            html += '</div>';
        }

        // Render markdown content
        html += marked.parse(taskData.content);

        modalDetails.innerHTML = html;

        // Add click handlers to dependency links
        document.querySelectorAll('.dependency-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const depFeatureId = link.dataset.featureId;
                const depLane = link.dataset.lane;
                const depTaskId = link.dataset.taskId;
                openTaskModal(depFeatureId, depLane, depTaskId);
            });
        });

    } catch (error) {
        console.error('Failed to load task detail:', error);
        modalDetails.innerHTML = '<p class="error">Failed to load task details</p>';
    }
}

// Setup modal tab switching
function setupModalTabs(featureId, taskId) {
    let commitsLoaded = false;

    document.querySelectorAll('.modal-tab').forEach(tab => {
        // Remove old listeners by cloning
        const newTab = tab.cloneNode(true);
        tab.parentNode.replaceChild(newTab, tab);
    });

    document.querySelectorAll('.modal-tab').forEach(tab => {
        tab.addEventListener('click', async () => {
            const tabName = tab.dataset.tab;

            // Update active tab
            document.querySelectorAll('.modal-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Show/hide content
            if (tabName === 'details') {
                document.getElementById('modal-details').style.display = 'block';
                document.getElementById('modal-commits').style.display = 'none';
            } else if (tabName === 'commits') {
                document.getElementById('modal-details').style.display = 'none';
                document.getElementById('modal-commits').style.display = 'block';

                // Load commits on first access
                if (!commitsLoaded) {
                    await loadTaskCommits(featureId, taskId);
                    commitsLoaded = true;
                }
            }
        });
    });
}

// Load git commits for a task
async function loadTaskCommits(featureId, taskId) {
    const container = document.getElementById('commits-container');
    container.innerHTML = '<p class="loading">Loading commits...</p>';

    try {
        const response = await fetch(`/api/task/${featureId}/planned/${taskId}/commits`);
        const commits = await response.json();

        if (commits.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>No git commits found for this task</p>
                    <p class="hint">Commits must include <code>[${taskId}]</code> in the message</p>
                </div>
            `;
            return;
        }

        // Render commits
        let html = '<div class="commits-list">';

        for (const commit of commits) {
            html += `
                <div class="commit-item">
                    <div class="commit-header">
                        <span class="commit-hash" title="${commit.sha}">${commit.short_sha}</span>
                        <span class="commit-author">${escapeHtml(commit.author)}</span>
                        <span class="commit-date">${new Date(commit.date).toLocaleString()}</span>
                    </div>
                    <div class="commit-message">${escapeHtml(commit.message)}</div>
                    <details class="commit-files">
                        <summary>View files</summary>
                        <div class="file-list" data-commit="${commit.sha}" data-feature="${featureId}" data-task="${taskId}">
                            <p class="loading">Loading files...</p>
                        </div>
                    </details>
                </div>
            `;
        }

        html += '</div>';
        container.innerHTML = html;

        // Add listeners for file details
        document.querySelectorAll('.commit-files summary').forEach(summary => {
            summary.addEventListener('click', async (e) => {
                const details = summary.parentElement;
                const fileList = details.querySelector('.file-list');

                if (fileList.dataset.loaded === 'true') return;

                const featureId = fileList.dataset.feature;
                const taskId = fileList.dataset.task;

                await loadTaskFiles(featureId, taskId, fileList);
                fileList.dataset.loaded = 'true';
            });
        });

    } catch (error) {
        console.error('Failed to load commits:', error);
        container.innerHTML = '<p class="error">Failed to load git commits</p>';
    }
}

// Load modified files for a task
async function loadTaskFiles(featureId, taskId, container) {
    try {
        const response = await fetch(`/api/task/${featureId}/planned/${taskId}/files`);
        const files = await response.json();

        if (files.length === 0) {
            container.innerHTML = '<p class="empty-state">No files found</p>';
            return;
        }

        let html = '<ul class="file-changes">';
        files.forEach(file => {
            const actionClass = file.action === 'A' ? 'added' : file.action === 'M' ? 'modified' : 'deleted';
            const actionText = file.action === 'A' ? 'Added' : file.action === 'M' ? 'Modified' : 'Deleted';

            html += `
                <li class="file-item ${actionClass}">
                    <span class="file-action">${actionText}</span>
                    <span class="file-path">${escapeHtml(file.path)}</span>
                    <span class="file-commit">${file.commit}</span>
                </li>
            `;
        });
        html += '</ul>';

        container.innerHTML = html;
    } catch (error) {
        console.error('Failed to load files:', error);
        container.innerHTML = '<p class="error">Failed to load files</p>';
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
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
