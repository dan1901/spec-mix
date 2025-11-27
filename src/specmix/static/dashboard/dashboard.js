// Dashboard JavaScript

let i18n = {};
let currentFeature = null;
let currentArtifact = null;
let currentWalkthroughFiles = [];
let refreshInterval = null;

// Get history state from URL hash
function getCurrentStateFromHash() {
    const hash = window.location.hash;

    if (hash.startsWith('#kanban/')) {
        return { view: 'kanban', featureId: hash.substring(8) };
    } else if (hash.startsWith('#artifact/')) {
        const parts = hash.substring(10).split('/');
        return { view: 'artifact', featureId: parts[0], artifactName: parts.slice(1).join('/') };
    } else if (hash === '#untracked') {
        return { view: 'untracked' };
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
    await updateUntrackedBadge(); // Initialize badge count

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
    } else if (hash === '#untracked') {
        switchTab('untracked');
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
        if (document.getElementById('untracked-view').classList.contains('active')) {
            await loadUntrackedCommits();
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
        } else if (state.view === 'untracked') {
            switchTab('untracked');
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

    } else if (tabName === 'untracked') {
        showView('untracked-view');
        loadUntrackedCommits();
        window.history.pushState({ view: 'untracked' }, '', '#untracked');

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

        // Sort features by number descending (e.g., 003 > 002 > 001)
        const sortedFeatures = [...features].sort((a, b) => {
            const numA = parseInt((a.id || '').match(/^(\d+)/)?.[1] || '0', 10);
            const numB = parseInt((b.id || '').match(/^(\d+)/)?.[1] || '0', 10);
            return numB - numA;
        });

        // Render features
        container.innerHTML = sortedFeatures.map(feature => renderFeatureCard(feature)).join('');

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

    // Mode badge
    if (feature.mode === 'normal') {
        badges.push(`<span class="feature-badge badge-mode-normal">Normal Mode</span>`);
    } else if (feature.mode === 'pro') {
        badges.push(`<span class="feature-badge badge-mode-pro">Pro Mode</span>`);
    }

    if (feature.worktree) {
        badges.push(`<span class="feature-badge badge-worktree">Worktree: ${feature.worktree}</span>`);
    }

    const stats = [];

    // Check if it's phase-based (Normal mode)
    if (feature.is_phase_mode && feature.phases) {
        const phases = Object.values(feature.phases);
        const totalPhases = phases.length;
        const completedPhases = phases.filter(p => p.status === 'done').length;
        const currentPhase = phases.find(p => p.status === 'doing');

        stats.push(`<span class="stat">📊 ${completedPhases}/${totalPhases} phases</span>`);
        if (currentPhase) {
            stats.push(`<span class="stat">⏳ ${currentPhase.title}</span>`);
        }
    } else if (feature.kanban_stats) {
        // Standard kanban stats (Pro mode)
        const { planned, doing, for_review, done } = feature.kanban_stats;
        if (planned > 0) stats.push(`<span class="stat">📋 ${planned} planned</span>`);
        if (doing > 0) stats.push(`<span class="stat">🔨 ${doing} doing</span>`);
        if (for_review > 0) stats.push(`<span class="stat">👀 ${for_review} review</span>`);
        if (done > 0) stats.push(`<span class="stat">✅ ${done} done</span>`);
    }

    const artifacts = Object.entries(feature.artifacts || {})
        .filter(([name, exists]) => exists && name !== 'kanban' && name !== 'phase_walkthroughs')
        .map(([name]) => `
            <span class="artifact-badge available"
                  data-feature-id="${feature.id}"
                  data-artifact="${name}.md">
                ${name}
            </span>
        `).join('');

    // Add phase walkthrough badges if available
    let walkthroughBadges = '';
    if (feature.walkthrough_files && feature.walkthrough_files.length > 0) {
        walkthroughBadges = feature.walkthrough_files.map(file => `
            <span class="artifact-badge available walkthrough-badge"
                  data-feature-id="${feature.id}"
                  data-artifact="${file}">
                ${file.replace('.md', '')}
            </span>
        `).join('');
    }

    return `
        <div class="feature-card" data-feature-id="${feature.id}" data-mode="${feature.mode || 'pro'}" data-phase-mode="${feature.is_phase_mode || false}">
            <div class="feature-header">
                <div class="feature-name">${feature.name}</div>
                ${badges.join('')}
            </div>
            ${stats.length > 0 ? `<div class="feature-stats">${stats.join('')}</div>` : ''}
            ${artifacts || walkthroughBadges ? `<div class="artifacts">${artifacts}${walkthroughBadges}</div>` : ''}
        </div>
    `;
}

// Show kanban board for feature
async function showKanban(featureId, pushState = true) {
    currentFeature = featureId;
    currentWalkthroughFiles = [];
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

    // Reset to board tab
    resetKanbanTabs();

    // Clear lanes
    ['planned', 'doing', 'for_review', 'done'].forEach(lane => {
        document.getElementById(`lane-${lane === 'for_review' ? 'for-review' : lane}-content`).innerHTML =
            '<p class="loading">Loading...</p>';
    });

    try {
        // Fetch both kanban data and feature info for walkthrough files
        const [kanbanResponse, featuresResponse] = await Promise.all([
            fetch(`/api/kanban/${featureId}`),
            fetch('/api/features')
        ]);

        const data = await kanbanResponse.json();
        const features = await featuresResponse.json();

        // Find current feature to get walkthrough files
        const feature = features.find(f => f.id === featureId);
        if (feature) {
            // Collect all walkthrough files
            currentWalkthroughFiles = [];

            // Add single walkthrough.md if exists (Pro mode)
            if (feature.artifacts && feature.artifacts.walkthrough) {
                currentWalkthroughFiles.push('walkthrough.md');
            }

            // Add phase walkthroughs (Normal mode)
            if (feature.walkthrough_files && feature.walkthrough_files.length > 0) {
                currentWalkthroughFiles.push(...feature.walkthrough_files);
            }
        }

        // Setup kanban tabs with walkthrough info
        setupKanbanTabs(featureId);

        // Check if it's phase-based mode (Normal mode)
        if (data.is_phase_mode && data.phases) {
            renderPhaseBoard(featureId, data);
        } else {
            renderKanbanBoard(featureId, data);
        }

    } catch (error) {
        console.error('Failed to load kanban:', error);
    }
}

// Render standard kanban board (Pro mode)
function renderKanbanBoard(featureId, data) {
    // Update lane titles for standard kanban
    document.getElementById('lane-planned').textContent = i18n.lanes?.planned || 'Planned';
    document.getElementById('lane-doing').textContent = i18n.lanes?.doing || 'Doing';
    document.getElementById('lane-for-review').textContent = i18n.lanes?.for_review || 'For Review';
    document.getElementById('lane-done').textContent = i18n.lanes?.done || 'Done';

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
}

// Render phase-based board (Normal mode)
function renderPhaseBoard(featureId, data) {
    // Update lane titles for phase mode
    document.getElementById('lane-planned').textContent = '📋 Pending';
    document.getElementById('lane-doing').textContent = '⏳ In Progress';
    document.getElementById('lane-for-review').textContent = '👀 Review';
    document.getElementById('lane-done').textContent = '✅ Completed';

    // Group phases by status
    const phasesByStatus = {
        planned: [],
        doing: [],
        for_review: [],
        done: []
    };

    Object.values(data.phases).forEach(phase => {
        phasesByStatus[phase.status].push(phase);
    });

    // Render phases as cards in lanes
    Object.entries(phasesByStatus).forEach(([status, phases]) => {
        const containerId = `lane-${status === 'for_review' ? 'for-review' : status}-content`;
        const container = document.getElementById(containerId);

        if (phases.length === 0) {
            container.innerHTML = '<p class="empty-state">No phases</p>';
        } else {
            container.innerHTML = phases.map(phase => `
                <div class="task-card phase-card" data-task-id="${phase.id}" data-lane="${status}" data-phase-num="${phase.phase_num}">
                    <div class="phase-header">
                        <strong>${phase.title}</strong>
                    </div>
                    <div class="phase-progress">
                        <span class="progress-badge">Progress: ${phase.progress}</span>
                    </div>
                </div>
            `).join('');
        }
    });

    // Add click handlers to phase cards
    document.querySelectorAll('.phase-card').forEach(card => {
        card.addEventListener('click', () => {
            const taskId = card.dataset.taskId;
            const lane = card.dataset.lane;
            openTaskModal(featureId, lane, taskId);
        });
    });
}

// Reset kanban tabs to initial state
function resetKanbanTabs() {
    // Reset to board tab
    document.querySelectorAll('.kanban-tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.kanbanTab === 'board') {
            tab.classList.add('active');
        }
    });

    // Show board, hide walkthrough
    document.getElementById('kanban-board').style.display = 'grid';
    document.getElementById('kanban-walkthrough').style.display = 'none';

    // Reset walkthrough content
    document.getElementById('walkthrough-selector').innerHTML = '';
    document.getElementById('walkthrough-content').innerHTML = '<p class="empty-state">Select a walkthrough to view</p>';
}

// Setup kanban tab switching
function setupKanbanTabs(featureId) {
    const walkthroughCountEl = document.getElementById('walkthrough-count');

    // Update walkthrough count badge
    if (currentWalkthroughFiles.length > 0) {
        walkthroughCountEl.textContent = currentWalkthroughFiles.length;
        walkthroughCountEl.style.display = 'inline-block';
    } else {
        walkthroughCountEl.style.display = 'none';
    }

    // Setup tab click handlers
    document.querySelectorAll('.kanban-tab').forEach(tab => {
        // Remove old listeners by cloning
        const newTab = tab.cloneNode(true);
        tab.parentNode.replaceChild(newTab, tab);
    });

    document.querySelectorAll('.kanban-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.kanbanTab;

            // Update active tab
            document.querySelectorAll('.kanban-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Show/hide content
            if (tabName === 'board') {
                document.getElementById('kanban-board').style.display = 'grid';
                document.getElementById('kanban-walkthrough').style.display = 'none';
            } else if (tabName === 'walkthrough') {
                document.getElementById('kanban-board').style.display = 'none';
                document.getElementById('kanban-walkthrough').style.display = 'block';

                // Populate walkthrough selector if not already done
                const selector = document.getElementById('walkthrough-selector');
                if (selector.innerHTML === '') {
                    renderWalkthroughSelector(featureId);
                }
            }
        });
    });
}

// Render walkthrough file selector
function renderWalkthroughSelector(featureId) {
    const selector = document.getElementById('walkthrough-selector');

    if (currentWalkthroughFiles.length === 0) {
        selector.innerHTML = '';
        document.getElementById('walkthrough-content').innerHTML = `
            <div class="empty-state">
                <p>No walkthroughs available for this feature</p>
                <p class="hint">Walkthroughs are generated during implementation using <code>/spec-mix.implement</code></p>
            </div>
        `;
        return;
    }

    // Sort files: walkthrough.md first, then phase walkthroughs in order
    const sortedFiles = [...currentWalkthroughFiles].sort((a, b) => {
        if (a === 'walkthrough.md') return -1;
        if (b === 'walkthrough.md') return 1;
        // Extract phase numbers for sorting
        const aMatch = a.match(/walkthrough-phase-(\d+)/);
        const bMatch = b.match(/walkthrough-phase-(\d+)/);
        if (aMatch && bMatch) {
            return parseInt(aMatch[1]) - parseInt(bMatch[1]);
        }
        return a.localeCompare(b);
    });

    // Render selector buttons
    selector.innerHTML = sortedFiles.map((file, index) => {
        const displayName = file === 'walkthrough.md'
            ? 'Summary'
            : file.replace('.md', '').replace('walkthrough-', '').replace('-', ' ');
        return `
            <button class="walkthrough-btn ${index === 0 ? 'active' : ''}"
                    data-file="${file}">
                ${displayName}
            </button>
        `;
    }).join('');

    // Add click handlers
    document.querySelectorAll('.walkthrough-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            document.querySelectorAll('.walkthrough-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Load walkthrough content
            loadWalkthrough(featureId, btn.dataset.file);
        });
    });

    // Auto-load first walkthrough
    if (sortedFiles.length > 0) {
        loadWalkthrough(featureId, sortedFiles[0]);
    }
}

// Load walkthrough content
async function loadWalkthrough(featureId, fileName) {
    const container = document.getElementById('walkthrough-content');
    container.innerHTML = '<p class="loading">Loading walkthrough...</p>';

    try {
        const response = await fetch(`/api/artifact/${featureId}/${fileName}`);

        if (!response.ok) {
            throw new Error('Walkthrough not found');
        }

        const content = await response.text();
        const html = marked.parse(content);
        container.innerHTML = html;

    } catch (error) {
        console.error('Failed to load walkthrough:', error);
        container.innerHTML = '<p class="error">Failed to load walkthrough</p>';
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
        // Auto-refresh features view
        if (document.getElementById('features-view').classList.contains('active')) {
            await loadFeatures();
        }
        // Auto-refresh untracked commits view
        if (document.getElementById('untracked-view').classList.contains('active')) {
            await loadUntrackedCommits();
        }
        // Always refresh badge count even if not on the tab
        await updateUntrackedBadge();
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
    const modalReviews = document.getElementById('modal-reviews');

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
    modalReviews.style.display = 'none';

    // Setup tab switching
    setupModalTabs(featureId, taskId, lane);

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
function setupModalTabs(featureId, taskId, lane) {
    let commitsLoaded = false;
    let reviewsLoaded = false;

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
                document.getElementById('modal-reviews').style.display = 'none';
            } else if (tabName === 'commits') {
                document.getElementById('modal-details').style.display = 'none';
                document.getElementById('modal-commits').style.display = 'block';
                document.getElementById('modal-reviews').style.display = 'none';

                // Load commits on first access
                if (!commitsLoaded) {
                    await loadTaskCommits(featureId, taskId, lane);
                    commitsLoaded = true;
                }
            } else if (tabName === 'reviews') {
                document.getElementById('modal-details').style.display = 'none';
                document.getElementById('modal-commits').style.display = 'none';
                document.getElementById('modal-reviews').style.display = 'block';

                // Load reviews on first access
                if (!reviewsLoaded) {
                    await loadTaskReviews(featureId, taskId, lane);
                    reviewsLoaded = true;
                }
            }
        });
    });
}

// Load git commits for a task
async function loadTaskCommits(featureId, taskId, lane) {
    const container = document.getElementById('commits-container');
    container.innerHTML = '<p class="loading">Loading commits...</p>';

    try {
        const response = await fetch(`/api/task/${featureId}/${lane}/${taskId}/commits`);
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
                        <div class="file-list" data-commit="${commit.sha}" data-feature="${featureId}" data-task="${taskId}" data-lane="${lane}">
                            <p class="loading">Loading files...</p>
                        </div>
                    </details>
                    <details class="commit-diff">
                        <summary>View diff</summary>
                        <div class="diff-content" data-commit="${commit.sha}" data-loaded="false">
                            <p class="loading">Loading diff...</p>
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
                const lane = fileList.dataset.lane;

                await loadTaskFiles(featureId, taskId, lane, fileList);
                fileList.dataset.loaded = 'true';
            });
        });

        // Add listeners for diff details
        document.querySelectorAll('.commit-diff summary').forEach(summary => {
            summary.addEventListener('click', async (e) => {
                const details = summary.parentElement;
                const diffContainer = details.querySelector('.diff-content');

                if (diffContainer.dataset.loaded === 'true') return;

                const commitSha = diffContainer.dataset.commit;
                await loadCommitDiff(commitSha, diffContainer);
                diffContainer.dataset.loaded = 'true';
            });
        });

    } catch (error) {
        console.error('Failed to load commits:', error);
        container.innerHTML = '<p class="error">Failed to load git commits</p>';
    }
}

// Load modified files for a task
async function loadTaskFiles(featureId, taskId, lane, container) {
    try {
        const response = await fetch(`/api/task/${featureId}/${lane}/${taskId}/files`);
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

// Load commit diff
async function loadCommitDiff(commitSha, container) {
    try {
        const response = await fetch(`/api/diff/${commitSha}`);

        if (!response.ok) {
            throw new Error('Failed to fetch diff');
        }

        const diffText = await response.text();

        if (!diffText || diffText.trim() === '') {
            container.innerHTML = '<p class="empty-state">No diff available</p>';
            return;
        }

        // Parse diff by file
        const fileDiffs = parseDiffByFile(diffText);

        if (fileDiffs.length === 0) {
            container.innerHTML = '<p class="empty-state">No diff available</p>';
            return;
        }

        // Create expandable sections for each file
        const html = fileDiffs.map(({fileName, diffContent}) => {
            const highlightedDiff = highlightDiff(diffContent);
            return `
                <details class="file-diff-section" open>
                    <summary class="file-diff-header">
                        <span class="file-diff-icon">📄</span>
                        <span class="file-diff-name">${escapeHtml(fileName)}</span>
                    </summary>
                    <pre class="diff-code">${highlightedDiff}</pre>
                </details>
            `;
        }).join('');

        container.innerHTML = html;
    } catch (error) {
        console.error('Failed to load diff:', error);
        container.innerHTML = '<p class="error">Failed to load diff</p>';
    }
}

// Parse git diff into separate files
function parseDiffByFile(diffText) {
    const lines = diffText.split('\n');
    const files = [];
    let currentFile = null;
    let currentContent = [];

    for (const line of lines) {
        if (line.startsWith('diff --git ')) {
            // Save previous file if exists
            if (currentFile) {
                files.push({
                    fileName: currentFile,
                    diffContent: currentContent.join('\n')
                });
            }

            // Extract file name from "diff --git a/path/to/file b/path/to/file"
            const match = line.match(/diff --git a\/(.*?) b\//);
            currentFile = match ? match[1] : 'unknown';
            currentContent = [line];
        } else if (currentFile) {
            currentContent.push(line);
        }
    }

    // Save last file
    if (currentFile && currentContent.length > 0) {
        files.push({
            fileName: currentFile,
            diffContent: currentContent.join('\n')
        });
    }

    return files;
}

// Highlight git diff syntax
function highlightDiff(diffText) {
    return diffText
        .split('\n')
        .map(line => {
            // Escape HTML first
            const escaped = escapeHtml(line);

            // Apply syntax highlighting
            if (line.startsWith('+') && !line.startsWith('+++')) {
                return `<span class="diff-add">${escaped}</span>`;
            } else if (line.startsWith('-') && !line.startsWith('---')) {
                return `<span class="diff-del">${escaped}</span>`;
            } else if (line.startsWith('@@')) {
                return `<span class="diff-hunk">${escaped}</span>`;
            } else if (line.startsWith('diff --git') || line.startsWith('index ')) {
                return `<span class="diff-file">${escaped}</span>`;
            } else if (line.startsWith('+++') || line.startsWith('---')) {
                return `<span class="diff-file-path">${escaped}</span>`;
            } else {
                return `<span class="diff-normal">${escaped}</span>`;
            }
        })
        .join('\n');
}

// Load review history for a task
async function loadTaskReviews(featureId, taskId, lane) {
    const container = document.getElementById('reviews-container');
    container.innerHTML = '<p class="loading">Loading review history...</p>';

    try {
        const response = await fetch(`/api/task/${featureId}/${lane}/${taskId}/reviews`);
        const reviews = await response.json();

        if (reviews.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>No reviews found for this task</p>
                    <p class="hint">Reviews will appear here when tasks are reviewed using <code>/spec-mix.review</code> or <code>/spec-mix.review-interactive</code></p>
                </div>
            `;
            return;
        }

        // Render review timeline
        let html = '<div class="review-timeline">';

        reviews.forEach((review, index) => {
            const isApproved = review.decision === 'APPROVED';
            const decisionClass = isApproved ? 'approved' : 'changes-requested';
            const decisionIcon = isApproved ? '✅' : '🔄';
            const decisionText = isApproved ? 'APPROVED' : 'CHANGES REQUESTED';

            html += `
                <div class="review-entry ${decisionClass}">
                    <div class="review-header">
                        <span class="review-decision-icon">${decisionIcon}</span>
                        <div class="review-meta">
                            <span class="review-decision">${decisionText}</span>
                            <span class="review-reviewer">by ${escapeHtml(review.reviewer)}</span>
                            <span class="review-date">${new Date(review.timestamp).toLocaleString()}</span>
                        </div>
                    </div>
                    <div class="review-body">
            `;

            // Show issues if present
            if (review.issues && review.issues.length > 0) {
                html += '<div class="review-issues">';
                html += '<h4>❌ Issues Found</h4>';
                html += '<ul>';
                review.issues.forEach(issue => {
                    html += `<li>${escapeHtml(issue)}</li>`;
                });
                html += '</ul>';
                html += '</div>';
            }

            // Show positives if present
            if (review.positives && review.positives.length > 0) {
                html += '<div class="review-positives">';
                html += '<h4>✅ Strengths</h4>';
                html += '<ul>';
                review.positives.forEach(positive => {
                    html += `<li>${escapeHtml(positive)}</li>`;
                });
                html += '</ul>';
                html += '</div>';
            }

            // Show notes if present
            if (review.notes && review.notes.length > 0) {
                html += '<div class="review-notes">';
                html += '<h4>📝 Notes</h4>';
                html += '<ul>';
                review.notes.forEach(note => {
                    html += `<li>${escapeHtml(note)}</li>`;
                });
                html += '</ul>';
                html += '</div>';
            }

            html += `
                    </div>
                </div>
            `;
        });

        html += '</div>';
        container.innerHTML = html;

    } catch (error) {
        console.error('Failed to load reviews:', error);
        container.innerHTML = '<p class="error">Failed to load review history</p>';
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

// Update untracked badge count
async function updateUntrackedBadge() {
    try {
        const response = await fetch('/api/untracked-commits');
        const commits = await response.json();
        const badge = document.getElementById('untracked-badge');

        if (commits.length === 0) {
            badge.style.display = 'none';
        } else {
            badge.textContent = commits.length;
            badge.style.display = 'inline-block';
        }
    } catch (error) {
        console.error('Failed to update untracked badge:', error);
    }
}

// Load untracked commits
async function loadUntrackedCommits() {
    const container = document.getElementById('untracked-list');
    const badge = document.getElementById('untracked-badge');
    container.innerHTML = '<p class="loading">Loading untracked commits...</p>';

    try {
        const response = await fetch('/api/untracked-commits');
        const commits = await response.json();

        if (commits.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>✅ All commits are tracked with Work Package IDs!</p>
                    <p class="hint">Commits without WP IDs will appear here for migration.</p>
                </div>
            `;
            badge.style.display = 'none';
            return;
        }

        // Update badge count
        badge.textContent = commits.length;
        badge.style.display = 'inline-block';

        // Render commit list
        let html = '<div class="commits-grid">';

        commits.forEach(commit => {
            const date = new Date(commit.date).toLocaleString();
            const shortSha = commit.sha.substring(0, 7);
            const stats = commit.stats;

            html += `
                <div class="commit-card">
                    <div class="commit-header">
                        <span class="commit-sha">${shortSha}</span>
                        <span class="commit-date">${date}</span>
                    </div>
                    <div class="commit-message">${escapeHtml(commit.message)}</div>
                    <div class="commit-author">👤 ${escapeHtml(commit.author)}</div>
                    <div class="commit-stats">
                        <span class="stat-item">📁 ${stats.files_changed} files</span>
                        <span class="stat-item stat-add">+${stats.insertions}</span>
                        <span class="stat-item stat-del">-${stats.deletions}</span>
                    </div>
                    <div class="commit-files">
                        ${commit.files.slice(0, 3).map(f => `<span class="file-name">${escapeHtml(f)}</span>`).join('')}
                        ${commit.files.length > 3 ? `<span class="file-more">+${commit.files.length - 3} more</span>` : ''}
                    </div>
                    <div class="commit-actions">
                        <button class="btn btn-primary" onclick="generateSpecFromCommit('${commit.sha}')">
                            📦 Migrate
                        </button>
                        <button class="btn btn-secondary" onclick="viewCommitDiff('${commit.sha}')">
                            View Diff
                        </button>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        container.innerHTML = html;

    } catch (error) {
        console.error('Failed to load untracked commits:', error);
        container.innerHTML = '<p class="error">Failed to load untracked commits</p>';
        badge.style.display = 'none';
    }
}

// Open migrate modal for a commit
async function generateSpecFromCommit(sha) {
    const modal = document.getElementById('migrate-modal');
    modal.classList.add('show');

    // Reset diff section
    document.getElementById('migrate-diff').innerHTML = '<p class="loading">Loading diff...</p>';
    document.querySelector('.migrate-diff-section').removeAttribute('open');

    // Find commit data from untracked list
    try {
        const response = await fetch('/api/untracked-commits');
        const commits = await response.json();
        const commit = commits.find(c => c.sha === sha);

        if (commit) {
            // Populate modal with commit info
            document.getElementById('migrate-sha').textContent = sha.substring(0, 7);
            document.getElementById('migrate-date').textContent = new Date(commit.date).toLocaleString();
            document.getElementById('migrate-message').textContent = commit.message;
            document.getElementById('migrate-author').textContent = `👤 ${commit.author}`;
            document.getElementById('migrate-stats').innerHTML = `
                <span class="stat-item">📁 ${commit.stats.files_changed} files</span>
                <span class="stat-item stat-add">+${commit.stats.insertions}</span>
                <span class="stat-item stat-del">-${commit.stats.deletions}</span>
            `;
        } else {
            // Fallback for commits not in the untracked list
            document.getElementById('migrate-sha').textContent = sha.substring(0, 7);
            document.getElementById('migrate-date').textContent = '';
            document.getElementById('migrate-message').textContent = 'Loading...';
            document.getElementById('migrate-author').textContent = '';
            document.getElementById('migrate-stats').innerHTML = '';
        }

        // Set command
        document.getElementById('migrate-command').textContent = `/spec-mix.migrate ${sha.substring(0, 7)}`;

        // Store full SHA for diff loading
        modal.dataset.commitSha = sha;

    } catch (error) {
        console.error('Failed to load commit info:', error);
    }
}

// Load diff when diff section is opened
document.addEventListener('DOMContentLoaded', () => {
    const diffSection = document.querySelector('.migrate-diff-section');
    if (diffSection) {
        diffSection.addEventListener('toggle', async (e) => {
            if (diffSection.open) {
                const modal = document.getElementById('migrate-modal');
                const sha = modal.dataset.commitSha;
                if (sha) {
                    await loadMigrateDiff(sha);
                }
            }
        });
    }
});

// Load diff for migrate modal
async function loadMigrateDiff(sha) {
    const container = document.getElementById('migrate-diff');

    try {
        const response = await fetch(`/api/diff/${sha}`);

        if (!response.ok) {
            throw new Error('Failed to load diff');
        }

        const diffText = await response.text();

        if (!diffText || diffText.trim() === '') {
            container.innerHTML = '<p class="empty-state">No diff available</p>';
            return;
        }

        // Parse and highlight diff
        const fileDiffs = parseDiffByFile(diffText);

        if (fileDiffs.length === 0) {
            container.innerHTML = '<p class="empty-state">No diff available</p>';
            return;
        }

        const html = fileDiffs.map(({fileName, diffContent}) => {
            const highlightedDiff = highlightDiff(diffContent);
            return `
                <details class="file-diff-section" open>
                    <summary class="file-diff-header">
                        <span class="file-diff-icon">📄</span>
                        <span class="file-diff-name">${escapeHtml(fileName)}</span>
                    </summary>
                    <pre class="diff-code">${highlightedDiff}</pre>
                </details>
            `;
        }).join('');

        container.innerHTML = html;

    } catch (error) {
        console.error('Failed to load diff:', error);
        container.innerHTML = '<p class="error">Failed to load diff</p>';
    }
}

// Close migrate modal
function closeMigrateModal() {
    const modal = document.getElementById('migrate-modal');
    modal.classList.remove('show');
}

// Copy migrate command to clipboard
async function copyMigrateCommand() {
    const command = document.getElementById('migrate-command').textContent;

    try {
        await navigator.clipboard.writeText(command);

        // Show toast
        const toast = document.getElementById('copy-toast');
        toast.classList.add('show');

        // Hide toast after 2 seconds
        setTimeout(() => {
            toast.classList.remove('show');
        }, 2000);

    } catch (error) {
        console.error('Failed to copy:', error);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = command;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);

        // Show toast anyway
        const toast = document.getElementById('copy-toast');
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 2000);
    }
}

// Close migrate modal when clicking outside
document.addEventListener('click', (e) => {
    const modal = document.getElementById('migrate-modal');
    if (e.target === modal) {
        closeMigrateModal();
    }
});

// Close migrate modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeMigrateModal();
    }
});

// View commit diff
function viewCommitDiff(sha) {
    window.open(`https://github.com/YOUR_ORG/YOUR_REPO/commit/${sha}`, '_blank');
}

// Cleanup on unload
window.addEventListener('beforeunload', () => {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});
