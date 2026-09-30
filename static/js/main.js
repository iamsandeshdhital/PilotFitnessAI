// Pilot Fitness Assessment AI - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // Animate score bars on page load
    const scoreFills = document.querySelectorAll('.score-fill');
    scoreFills.forEach(function(fill) {
        const width = fill.style.width;
        fill.style.width = '0';
        setTimeout(function() {
            fill.style.width = width;
        }, 100);
    });

    // Animate bars in charts
    const bars = document.querySelectorAll('.bar');
    bars.forEach(function(bar) {
        const height = bar.style.height;
        bar.style.height = '0';
        setTimeout(function() {
            bar.style.height = height;
        }, 100);
    });

    // Confirm before running assessment
    const assessForms = document.querySelectorAll('form[action*="assess"]');
    assessForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to run this comprehensive assessment? This will analyze all available data across 15 modules.')) {
                e.preventDefault();
            }
        });
    });

    // Table row click navigation
    const clickableRows = document.querySelectorAll('tr[data-href]');
    clickableRows.forEach(function(row) {
        row.addEventListener('click', function() {
            window.location.href = this.dataset.href;
        });
        row.style.cursor = 'pointer';
    });

    // Search/filter functionality
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const table = this.closest('.section').querySelector('.data-table');
            if (table) {
                const rows = table.querySelectorAll('tbody tr');
                rows.forEach(function(row) {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchTerm) ? '' : 'none';
                });
            }
        });
    });

    // Print report functionality
    const printBtns = document.querySelectorAll('.print-report');
    printBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            window.print();
        });
    });

    // Export to CSV functionality
    const exportBtns = document.querySelectorAll('.export-csv');
    exportBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const table = this.closest('.section').querySelector('.data-table');
            if (table) {
                exportTableToCSV(table, 'pilot_fitness_report.csv');
            }
        });
    });
});

// Export table to CSV
function exportTableToCSV(table, filename) {
    const rows = table.querySelectorAll('tr');
    let csv = [];
    
    rows.forEach(function(row) {
        const cols = row.querySelectorAll('th, td');
        const rowData = [];
        cols.forEach(function(col) {
            let data = col.textContent.replace(/(\r\n|\n|\r)/gm, '').replace(/"/g, '""');
            rowData.push('"' + data + '"');
        });
        csv.push(rowData.join(','));
    });
    
    const csvContent = '\uFEFF' + csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}

// Toggle module details
function toggleModuleDetails(moduleId) {
    const details = document.getElementById(moduleId + '-details');
    if (details) {
        details.classList.toggle('collapsed');
    }
}

// Filter assessments by status
function filterByStatus(status) {
    const rows = document.querySelectorAll('.data-table tbody tr');
    rows.forEach(function(row) {
        const badge = row.querySelector('.badge');
        if (badge) {
            const rowStatus = badge.textContent.toLowerCase();
            row.style.display = (status === 'all' || rowStatus.includes(status)) ? '' : 'none';
        }
    });
}

// Calculate and display risk score color
function getRiskColor(score) {
    if (score >= 80) return '#28a745';
    if (score >= 60) return '#ffc107';
    if (score >= 40) return '#fd7e14';
    return '#dc3545';
}

// Print styles
window.addEventListener('beforeprint', function() {
    document.body.classList.add('printing');
});

window.addEventListener('afterprint', function() {
    document.body.classList.remove('printing');
});
