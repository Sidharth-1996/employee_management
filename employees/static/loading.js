// Professional Loading States System

/**
 * Show loading state for a form
 * @param {string} formId - The ID of the form
 * @param {boolean} show - Show or hide loading state
 */
function setFormLoading(formId, show = true) {
    const form = document.getElementById(formId);
    if (!form) return;

    const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
    if (!submitButton) return;

    if (show) {
        submitButton.disabled = true;
        submitButton.dataset.originalText = submitButton.textContent || submitButton.value;
        
        const spinner = document.createElement('span');
        spinner.className = 'spinner inline-block ml-2';
        spinner.style.width = '16px';
        spinner.style.height = '16px';
        spinner.style.borderWidth = '2px';
        
        submitButton.appendChild(spinner);
        submitButton.style.opacity = '0.7';
        submitButton.style.cursor = 'not-allowed';
    } else {
        submitButton.disabled = false;
        submitButton.textContent = submitButton.dataset.originalText || submitButton.textContent;
        submitButton.value = submitButton.dataset.originalText || submitButton.value;
        const spinner = submitButton.querySelector('.spinner');
        if (spinner) spinner.remove();
        submitButton.style.opacity = '1';
        submitButton.style.cursor = 'pointer';
    }
}

/**
 * Show page loading overlay
 */
function showPageLoading() {
    const overlay = document.createElement('div');
    overlay.id = 'pageLoadingOverlay';
    overlay.className = 'fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-50 flex items-center justify-center';
    overlay.innerHTML = `
        <div class="bg-white rounded-2xl p-8 shadow-2xl flex flex-col items-center">
            <div class="spinner" style="width: 48px; height: 48px; border-width: 4px;"></div>
            <p class="mt-4 text-gray-700 font-semibold">Loading...</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

/**
 * Hide page loading overlay
 */
function hidePageLoading() {
    const overlay = document.getElementById('pageLoadingOverlay');
    if (overlay) {
        overlay.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => overlay.remove(), 300);
    }
}

/**
 * Show loading state for a card/section
 * @param {string} elementId - The ID of the element
 * @param {boolean} show - Show or hide loading state
 */
function setCardLoading(elementId, show = true) {
    const element = document.getElementById(elementId);
    if (!element) return;

    if (show) {
        element.classList.add('loading');
        element.style.opacity = '0.6';
        element.style.pointerEvents = 'none';
    } else {
        element.classList.remove('loading');
        element.style.opacity = '1';
        element.style.pointerEvents = 'auto';
    }
}

/**
 * Show loading skeleton for content
 * @param {string} containerId - The ID of the container
 * @param {number} count - Number of skeleton items to show
 */
function showSkeletonLoader(containerId, count = 3) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '';
    for (let i = 0; i < count; i++) {
        const skeleton = document.createElement('div');
        skeleton.className = 'skeleton-loader card p-6 mb-4';
        skeleton.innerHTML = `
            <div class="h-4 bg-gray-200 rounded w-3/4 mb-4 animate-pulse"></div>
            <div class="h-4 bg-gray-200 rounded w-1/2 mb-2 animate-pulse"></div>
            <div class="h-4 bg-gray-200 rounded w-5/6 animate-pulse"></div>
        `;
        container.appendChild(skeleton);
    }
}

// Add fadeOut animation if not present
if (!document.getElementById('loadingAnimations')) {
    const style = document.createElement('style');
    style.id = 'loadingAnimations';
    style.textContent = `
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        .skeleton-loader {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    `;
    document.head.appendChild(style);
}

// Auto-enable form loading states
document.addEventListener('DOMContentLoaded', function() {
    // Add loading state to all forms on submit
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            // Only add loading if form has validation
            if (form.checkValidity()) {
                setFormLoading(form.id || form.className, true);
            }
        });
    });
});

