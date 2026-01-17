/**
 * Professional Date Range Picker - Senior Developer Quality
 * Handles smooth date range selection with proper state management
 */

class DateRangePicker {
    constructor(options = {}) {
        this.startDate = options.startDate || null;
        this.endDate = options.endDate || null;
        this.today = options.today || new Date().toISOString().split('T')[0];
        this.selectionMode = 'start'; // 'start' | 'end'
        this.onChange = options.onChange || null;
        this.onApply = options.onApply || null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.updateVisualState();
    }
    
    setupEventListeners() {
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });
        
        // Click outside to close
        const modal = document.getElementById('calendarModal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        }
    }
    
    /**
     * Select a date for range selection
     * First click sets start date, second click sets end date
     */
    selectDate(dateStr, event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }
        
        const selectedDate = new Date(dateStr + 'T00:00:00');
        const today = new Date(this.today + 'T00:00:00');
        
        // Prevent future dates
        if (selectedDate > today) {
            this.showFeedback('Cannot select future dates', 'warning');
            return;
        }
        
        // If no start date selected, or if clicking before start date, set as start
        if (!this.startDate || selectedDate < new Date(this.startDate + 'T00:00:00')) {
            this.startDate = dateStr;
            this.endDate = null;
            this.selectionMode = 'end';
            this.showFeedback(`Start date selected: ${this.formatDisplayDate(dateStr)}. Select end date.`, 'info');
        } else {
            // Set as end date
            this.endDate = dateStr;
            this.selectionMode = 'start';
            this.showFeedback(`Date range selected: ${this.formatDisplayDate(this.startDate)} - ${this.formatDisplayDate(dateStr)}`, 'success');
        }
        
        this.updateVisualState();
        this.syncInputs();
    }
    
    /**
     * Apply preset range (Today, Last 7 Days, etc.)
     */
    applyPresetRange(presetType, event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }
        
        const today = new Date(this.today);
        let start, end;
        
        switch(presetType) {
            case 'today':
                start = end = new Date(today);
                break;
            case 'yesterday':
                start = end = new Date(today);
                start.setDate(today.getDate() - 1);
                break;
            case 'last7days':
                end = new Date(today);
                start = new Date(today);
                start.setDate(today.getDate() - 6);
                break;
            case 'last30days':
                end = new Date(today);
                start = new Date(today);
                start.setDate(today.getDate() - 29);
                break;
            case 'last90days':
                end = new Date(today);
                start = new Date(today);
                start.setDate(today.getDate() - 89);
                break;
            case 'thisweek':
                start = new Date(today);
                start.setDate(today.getDate() - today.getDay() + 1); // Monday
                end = new Date(today);
                break;
            case 'lastweek':
                end = new Date(today);
                end.setDate(today.getDate() - today.getDay()); // Sunday of last week
                start = new Date(end);
                start.setDate(end.getDate() - 6); // Monday of last week
                break;
            case 'thismonth':
                start = new Date(today.getFullYear(), today.getMonth(), 1);
                end = new Date(today);
                break;
            case 'lastmonth':
                start = new Date(today.getFullYear(), today.getMonth() - 1, 1);
                end = new Date(today.getFullYear(), today.getMonth(), 0);
                break;
            case 'thisyear':
                start = new Date(today.getFullYear(), 0, 1);
                end = new Date(today);
                break;
            case 'lastyear':
                start = new Date(today.getFullYear() - 1, 0, 1);
                end = new Date(today.getFullYear() - 1, 11, 31);
                break;
            default:
                return;
        }
        
        this.startDate = this.formatDateForInput(start);
        this.endDate = this.formatDateForInput(end);
        this.selectionMode = 'start';
        
        this.updateVisualState();
        this.syncInputs();
        this.showFeedback(`Applied preset: ${presetType}`, 'success');
    }
    
    /**
     * Apply custom date range from inputs
     */
    applyCustomRange(event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }
        
        const startInput = document.getElementById('customStartDate');
        const endInput = document.getElementById('customEndDate');
        
        if (!startInput || !endInput || !startInput.value || !endInput.value) {
            this.showFeedback('Please select both start and end dates', 'error');
            return;
        }
        
        const startDate = new Date(startInput.value + 'T00:00:00');
        const endDate = new Date(endInput.value + 'T00:00:00');
        const today = new Date(this.today + 'T00:00:00');
        
        // Validation
        if (startDate > endDate) {
            this.showFeedback('Start date cannot be after end date', 'error');
            return;
        }
        
        if (endDate > today) {
            this.showFeedback('End date cannot be in the future', 'error');
            return;
        }
        
        this.startDate = startInput.value;
        this.endDate = endInput.value;
        this.selectionMode = 'start';
        
        this.updateVisualState();
        this.showFeedback('Custom range applied', 'success');
    }
    
    /**
     * Update visual highlights on calendar
     */
    updateVisualState() {
        const calendarDays = document.querySelectorAll('.calendar-day[data-date]');
        
        calendarDays.forEach(day => {
            const dayDate = day.getAttribute('data-date');
            const dayDateObj = new Date(dayDate + 'T00:00:00');
            const todayObj = new Date(this.today + 'T00:00:00');
            
            // Reset classes
            day.classList.remove(
                'bg-blue-500', 'bg-blue-600', 'bg-purple-600',
                'text-white', 'ring-2', 'ring-blue-300', 'scale-110',
                'border-2', 'border-blue-400'
            );
            
            // Future dates - disabled
            if (dayDateObj > todayObj) {
                day.classList.add('opacity-50', 'cursor-not-allowed', 'bg-gray-100');
                day.disabled = true;
                return;
            }
            
            day.classList.remove('opacity-50', 'cursor-not-allowed', 'bg-gray-100');
            day.disabled = false;
            
            // Today indicator
            if (dayDate === this.today) {
                day.classList.add('border-2', 'border-yellow-400');
            }
            
            // Selected range highlighting
            if (this.startDate && this.endDate) {
                if (dayDate >= this.startDate && dayDate <= this.endDate) {
                    if (dayDate === this.startDate) {
                        day.classList.add('bg-gradient-to-br', 'from-blue-600', 'to-purple-600', 'text-white', 'ring-2', 'ring-blue-300', 'scale-110', 'font-bold');
                    } else if (dayDate === this.endDate) {
                        day.classList.add('bg-gradient-to-br', 'from-blue-600', 'to-purple-600', 'text-white', 'ring-2', 'ring-blue-300', 'scale-110', 'font-bold');
                    } else {
                        day.classList.add('bg-blue-500', 'text-white');
                    }
                }
            } else if (this.startDate && dayDate === this.startDate) {
                // Only start date selected
                day.classList.add('bg-gradient-to-br', 'from-blue-600', 'to-purple-600', 'text-white', 'ring-2', 'ring-blue-300', 'scale-110', 'font-bold');
            }
            
            // Default hover state
            if (!day.classList.contains('bg-blue-500') && !day.classList.contains('bg-blue-600') && !day.classList.contains('bg-purple-600')) {
                day.classList.add('hover:bg-blue-100');
            }
        });
        
        // Update preset button states
        this.updatePresetButtons();
        
        // Update display
        this.updateRangeDisplay();
    }
    
    /**
     * Update preset button active states
     */
    updatePresetButtons() {
        const presetButtons = document.querySelectorAll('[data-preset]');
        presetButtons.forEach(btn => {
            const presetValue = btn.getAttribute('data-preset');
            btn.classList.remove('bg-gradient-to-r', 'from-blue-600', 'to-purple-600', 'text-white', 'shadow-lg', 'ring-2', 'ring-blue-400');
            btn.classList.add('bg-white/80', 'text-gray-700', 'border', 'border-gray-200/50');
        });
    }
    
    /**
     * Update the range display text
     */
    updateRangeDisplay() {
        const displayElement = document.getElementById('selectedRangeDisplay');
        if (displayElement && this.startDate) {
            if (this.endDate) {
                const days = this.calculateDays();
                displayElement.innerHTML = `
                    <span class="text-blue-600 font-extrabold">${this.formatDisplayDate(this.startDate)}</span>
                    <span class="mx-2 text-gray-600">→</span>
                    <span class="text-purple-600 font-extrabold">${this.formatDisplayDate(this.endDate)}</span>
                    <span class="ml-3 text-sm text-gray-500">(${days} ${days === 1 ? 'day' : 'days'})</span>
                `;
            } else {
                displayElement.innerHTML = `
                    <span class="text-blue-600 font-extrabold">${this.formatDisplayDate(this.startDate)}</span>
                    <span class="ml-3 text-sm text-gray-500">Select end date...</span>
                `;
            }
        }
    }
    
    /**
     * Calculate days between dates
     */
    calculateDays() {
        if (!this.startDate || !this.endDate) return 0;
        const start = new Date(this.startDate + 'T00:00:00');
        const end = new Date(this.endDate + 'T00:00:00');
        const diffTime = Math.abs(end - start);
        return Math.floor(diffTime / (1000 * 60 * 60 * 24)) + 1;
    }
    
    /**
     * Sync custom input fields with selected dates
     */
    syncInputs() {
        const startInput = document.getElementById('customStartDate');
        const endInput = document.getElementById('customEndDate');
        
        if (startInput && this.startDate) {
            startInput.value = this.startDate;
        }
        if (endInput && this.endDate) {
            endInput.value = this.endDate;
        }
    }
    
    /**
     * Apply the selected date range (navigate to URL)
     */
    applyRange(event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }
        
        if (!this.startDate || !this.endDate) {
            this.showFeedback('Please select a complete date range', 'error');
            return;
        }
        
        // Validate
        const start = new Date(this.startDate + 'T00:00:00');
        const end = new Date(this.endDate + 'T00:00:00');
        const today = new Date(this.today + 'T00:00:00');
        
        if (start > end) {
            this.showFeedback('Start date cannot be after end date', 'error');
            return;
        }
        
        if (end > today) {
            this.showFeedback('End date cannot be in the future', 'error');
            return;
        }
        
        // Navigate to URL with date parameters
        const url = new URL(window.location);
        url.searchParams.set('start_date', this.startDate);
        url.searchParams.set('end_date', this.endDate);
        url.searchParams.delete('calendar_month');
        url.searchParams.delete('calendar_year');
        
        // Show loading state
        this.showFeedback('Loading attendance records...', 'info');
        
        // Navigate
        window.location.href = url.toString();
    }
    
    /**
     * Toggle calendar modal
     */
    toggleModal(event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }
        
        const modal = document.getElementById('calendarModal');
        const modalContent = document.getElementById('calendarModalContent');
        
        if (!modal) return;
        
        const isHidden = modal.classList.contains('hidden');
        
        if (isHidden) {
            // Opening
            modal.classList.remove('hidden');
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            
            // Reset selection to current range
            this.startDate = window.tempStartDate || this.startDate;
            this.endDate = window.tempEndDate || this.endDate;
            
            // Trigger animation
            setTimeout(() => {
                if (modalContent) {
                    modalContent.style.animation = 'none';
                    requestAnimationFrame(() => {
                        modalContent.style.animation = 'modalFadeIn 0.3s ease-out forwards';
                    });
                }
            }, 10);
            
            this.updateVisualState();
            this.syncInputs();
        } else {
            // Closing
            this.closeModal();
        }
    }
    
    /**
     * Close calendar modal
     */
    closeModal() {
        const modal = document.getElementById('calendarModal');
        if (modal) {
            modal.classList.add('hidden');
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }
    }
    
    /**
     * Navigate calendar months
     */
    navigateMonth(year, month, direction) {
        const currentDate = new Date(year, month - 1, 1);
        currentDate.setMonth(currentDate.getMonth() + direction);
        
        const url = new URL(window.location);
        url.searchParams.set('calendar_month', currentDate.getMonth() + 1);
        url.searchParams.set('calendar_year', currentDate.getFullYear());
        
        if (this.startDate) url.searchParams.set('start_date', this.startDate);
        if (this.endDate) url.searchParams.set('end_date', this.endDate);
        
        window.location.href = url.toString();
    }
    
    /**
     * Show user feedback
     */
    showFeedback(message, type = 'info') {
        if (window.showToast) {
            window.showToast(message, type, 2000);
        }
    }
    
    /**
     * Format date for display
     */
    formatDisplayDate(dateStr) {
        const date = new Date(dateStr + 'T00:00:00');
        return date.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric', 
            year: 'numeric' 
        });
    }
    
    /**
     * Format date for input (YYYY-MM-DD)
     */
    formatDateForInput(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
}

// Global instance
let dateRangePicker = null;

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    const startDate = '{{ start_date|date:"Y-m-d" }}';
    const endDate = '{{ end_date|date:"Y-m-d" }}';
    const today = '{{ today|date:"Y-m-d" }}';
    
    dateRangePicker = new DateRangePicker({
        startDate: startDate,
        endDate: endDate,
        today: today
    });
    
    // Store in window for easy access
    window.tempStartDate = startDate;
    window.tempEndDate = endDate;
    window.dateRangePicker = dateRangePicker;
});

// Global functions for backward compatibility and template usage
function toggleCalendar(event) {
    if (window.dateRangePicker) {
        window.dateRangePicker.toggleModal(event);
    }
}

function selectDateRange(dateStr, event) {
    if (window.dateRangePicker) {
        window.dateRangePicker.selectDate(dateStr, event);
        window.tempStartDate = window.dateRangePicker.startDate;
        window.tempEndDate = window.dateRangePicker.endDate;
    }
}

function applyPresetRange(presetType, event) {
    if (window.dateRangePicker) {
        window.dateRangePicker.applyPresetRange(presetType, event);
        window.tempStartDate = window.dateRangePicker.startDate;
        window.tempEndDate = window.dateRangePicker.endDate;
    }
}

function applyCustomRange(event) {
    if (window.dateRangePicker) {
        window.dateRangePicker.applyCustomRange(event);
        window.tempStartDate = window.dateRangePicker.startDate;
        window.tempEndDate = window.dateRangePicker.endDate;
    }
}

function applyDateRange(event) {
    if (window.dateRangePicker) {
        window.dateRangePicker.applyRange(event);
    }
}

function navigateMonth(event, year, month, direction) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    if (window.dateRangePicker) {
        window.dateRangePicker.navigateMonth(year, month, direction);
    }
}

