// Professional Table Sorting and Filtering System

/**
 * Initialize table sorting and filtering
 * @param {string} tableId - The ID of the table
 * @param {Array} sortableColumns - Array of column indices that should be sortable
 */
function initTableSort(tableId, sortableColumns = []) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const thead = table.querySelector('thead');
    const tbody = table.querySelector('tbody');
    if (!thead || !tbody) return;

    const headers = thead.querySelectorAll('th');
    let sortDirection = {};

    // Add click handlers to sortable columns
    sortableColumns.forEach(colIndex => {
        const header = headers[colIndex];
        if (!header) return;

        header.style.cursor = 'pointer';
        header.classList.add('sortable');
        
        // Add sort indicator
        const indicator = document.createElement('span');
        indicator.className = 'sort-indicator ml-2';
        indicator.innerHTML = '↕';
        indicator.style.opacity = '0.3';
        header.appendChild(indicator);

        header.addEventListener('click', () => {
            const isAscending = sortDirection[colIndex] !== 'asc';
            sortTable(tableId, colIndex, isAscending);
            sortDirection[colIndex] = isAscending ? 'asc' : 'desc';

            // Update indicators
            headers.forEach((h, i) => {
                const ind = h.querySelector('.sort-indicator');
                if (ind) {
                    if (i === colIndex) {
                        ind.innerHTML = isAscending ? '↑' : '↓';
                        ind.style.opacity = '1';
                        h.classList.add('sorted');
                    } else {
                        ind.innerHTML = '↕';
                        ind.style.opacity = '0.3';
                        h.classList.remove('sorted');
                    }
                }
            });
        });
    });
}

/**
 * Sort table by column
 * @param {string} tableId - The ID of the table
 * @param {number} columnIndex - The column index to sort by
 * @param {boolean} ascending - Sort direction
 */
function sortTable(tableId, columnIndex, ascending = true) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const aText = getCellText(a.cells[columnIndex]);
        const bText = getCellText(b.cells[columnIndex]);

        // Try to parse as numbers
        const aNum = parseFloat(aText.replace(/[^0-9.-]/g, ''));
        const bNum = parseFloat(bText.replace(/[^0-9.-]/g, ''));

        if (!isNaN(aNum) && !isNaN(bNum)) {
            return ascending ? aNum - bNum : bNum - aNum;
        }

        // Compare as strings
        if (ascending) {
            return aText.localeCompare(bText);
        } else {
            return bText.localeCompare(aText);
        }
    });

    // Clear tbody
    tbody.innerHTML = '';

    // Append sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

/**
 * Get text content from a table cell
 * @param {HTMLElement} cell - The table cell element
 * @returns {string} - The text content
 */
function getCellText(cell) {
    if (!cell) return '';
    // Get text content, excluding icons and buttons
    const clone = cell.cloneNode(true);
    clone.querySelectorAll('svg, button, .sort-indicator').forEach(el => el.remove());
    return clone.textContent.trim();
}

/**
 * Add table filtering
 * @param {string} inputId - The ID of the filter input
 * @param {string} tableId - The ID of the table
 */
function initTableFilter(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;

    input.addEventListener('input', function() {
        const filter = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        let visibleCount = 0;

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(filter)) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });

        // Show/hide "no results" message
        let noResults = table.parentElement.querySelector('.no-results');
        if (visibleCount === 0 && filter) {
            if (!noResults) {
                noResults = document.createElement('div');
                noResults.className = 'no-results text-center py-8 text-gray-500';
                noResults.textContent = 'No matching records found';
                table.parentElement.appendChild(noResults);
            }
            noResults.style.display = 'block';
        } else if (noResults) {
            noResults.style.display = 'none';
        }
    });
}

// Auto-initialize common patterns on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize employee list table if present
    const employeeTable = document.getElementById('employeeTable');
    if (employeeTable) {
        initTableSort('employeeTable', [0, 1]); // Sortable by name and department
    }

    // Initialize attendance table if present
    const attendanceTable = document.getElementById('attendanceTable');
    if (attendanceTable) {
        initTableSort('attendanceTable', [0, 1]); // Sortable by employee name and department
    }
});

