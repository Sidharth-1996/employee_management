// Professional Sidebar Navigation System

/**
 * Toggle sidebar visibility on mobile
 */
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    if (!sidebar) return;

    const isOpen = sidebar.classList.contains('open');
    
    if (isOpen) {
        sidebar.classList.remove('open');
        if (overlay) overlay.classList.add('hidden');
        document.body.style.overflow = '';
    } else {
        sidebar.classList.add('open');
        if (overlay) {
            overlay.classList.remove('hidden');
        } else {
            // Create overlay if it doesn't exist
            const newOverlay = document.createElement('div');
            newOverlay.id = 'sidebarOverlay';
            newOverlay.className = 'fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden';
            newOverlay.onclick = toggleSidebar;
            document.body.appendChild(newOverlay);
        }
        document.body.style.overflow = 'hidden';
    }
}

/**
 * Close sidebar on mobile
 */
function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    if (sidebar) sidebar.classList.remove('open');
    if (overlay) overlay.classList.add('hidden');
    document.body.style.overflow = '';
}

/**
 * Set active navigation item
 * @param {string} currentPath - Current page path
 */
function setActiveNavItem(currentPath) {
    const navLinks = document.querySelectorAll('.sidebar-link, .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href.split('?')[0])) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Close sidebar when clicking outside on mobile
document.addEventListener('DOMContentLoaded', function() {
    // Set active nav item based on current URL
    setActiveNavItem(window.location.pathname);

    // Close sidebar on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeSidebar();
        }
    });

    // Close sidebar when window is resized to desktop
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth >= 1024) {
                closeSidebar();
            }
        }, 250);
    });
});

