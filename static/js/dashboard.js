/**
 * Dashboard JavaScript - Handles all frontend interactions
 */

// Global variables
let allInventoryData = [];
let filteredData = [];

/**
 * Load inventory data from the API
 */
function loadInventory() {
    fetch('/api/inventory')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load inventory');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                allInventoryData = data.data;
                filteredData = [...allInventoryData];
                displayInventory(filteredData);
                updateLastUpdated(data.timestamp);
            } else {
                showError('Failed to load inventory: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Error loading inventory: ' + error.message);
        });
}

/**
 * Display inventory data in the table
 */
function displayInventory(items) {
    const tbody = document.getElementById('inventoryBody');
    const itemCount = document.getElementById('itemCount');
    
    if (!items || items.length === 0) {
        tbody.innerHTML = '<tr class="loading-row"><td colspan="5" class="text-center">No items found</td></tr>';
        itemCount.textContent = '0 items';
        return;
    }
    
    let html = '';
    items.forEach((item, index) => {
        const status = getItemStatus(item.Quantity);
        const statusClass = getStatusClass(item.Quantity);
        
        html += `
            <tr class="inventory-row">
                <td class="item-id">${index + 1}</td>
                <td class="item-name">${escapeHtml(item.Item || 'N/A')}</td>
                <td class="item-sku">${escapeHtml(item.SKU || 'N/A')}</td>
                <td class="item-quantity">${item.Quantity}</td>
                <td class="item-status">
                    <span class="status-badge ${statusClass}">${status}</span>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
    itemCount.textContent = `${items.length} items`;
}

/**
 * Load and display statistics
 */
function loadStats() {
    fetch('/api/inventory/stats')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                displayStats(data.data);
            }
        })
        .catch(error => console.error('Error loading stats:', error));
}

/**
 * Display statistics cards
 */
function displayStats(stats) {
    const statsContainer = document.getElementById('statsContainer');
    
    if (!stats || Object.keys(stats).length === 0) {
        return;
    }
    
    let html = `
        <div class="stat-card">
            <div class="stat-label">Total Items</div>
            <div class="stat-value">${stats.total_items || 0}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Total Quantity</div>
            <div class="stat-value">${stats.total_quantity || 0}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Average Stock</div>
            <div class="stat-value">${stats.average_quantity || 0}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Out of Stock</div>
            <div class="stat-value" style="color: #f44336;">${stats.out_of_stock_count || 0}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Low Stock</div>
            <div class="stat-value" style="color: #ff9800;">${stats.low_stock_count || 0}</div>
        </div>
    `;
    
    statsContainer.innerHTML = html;
}

/**
 * Search inventory by item name or SKU
 */
function searchInventory() {
    const searchInput = document.getElementById('searchInput').value.trim();
    
    if (!searchInput) {
        filteredData = [...allInventoryData];
        displayInventory(filteredData);
        return;
    }
    
    fetch(`/api/inventory/search?q=${encodeURIComponent(searchInput)}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                filteredData = data.data;
                displayInventory(filteredData);
            }
        })
        .catch(error => console.error('Error searching inventory:', error));
}

/**
 * Manually refresh inventory
 */
function refreshInventory() {
    const btn = event.target.closest('.btn-refresh');
    const originalText = btn.textContent;
    btn.textContent = '⏳ Refreshing...';
    btn.disabled = true;
    
    fetch('/api/inventory/refresh', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                loadInventory();
                loadStats();
                showSuccess('Inventory refreshed successfully!');
            } else {
                showError('Failed to refresh inventory: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Error refreshing inventory: ' + error.message);
        })
        .finally(() => {
            btn.textContent = originalText;
            btn.disabled = false;
        });
}

/**
 * Get item status based on quantity
 */
function getItemStatus(quantity) {
    if (quantity === 0) {
        return 'Out of Stock';
    } else if (quantity < 50) {
        return 'Low Stock';
    } else if (quantity < 100) {
        return 'Medium Stock';
    } else {
        return 'Good Stock';
    }
}

/**
 * Get status CSS class
 */
function getStatusClass(quantity) {
    if (quantity === 0) {
        return 'status-critical';
    } else if (quantity < 50) {
        return 'status-warning';
    } else if (quantity < 100) {
        return 'status-medium';
    } else {
        return 'status-good';
    }
}

/**
 * Update last updated timestamp
 */
function updateLastUpdated(timestamp) {
    const lastUpdatedEl = document.getElementById('last-updated');
    if (lastUpdatedEl && timestamp) {
        const date = new Date(timestamp);
        lastUpdatedEl.textContent = date.toLocaleString();
    }
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Show error message
 */
function showError(message) {
    console.error(message);
    // Could implement a toast notification here
}

/**
 * Show success message
 */
function showSuccess(message) {
    console.log(message);
    // Could implement a toast notification here
}
