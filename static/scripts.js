document.addEventListener('DOMContentLoaded', () => {
    // Handle Add Data form submission
    document.getElementById('add-data-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('id').value;
        const name = document.getElementById('name').value;
        const age = document.getElementById('age').value;

        const response = await fetch('/add-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id, name, age }),
        });

        const result = await response.json();
        document.getElementById('response-message').textContent = result.status;
        if (response.ok) {
            document.getElementById('add-data-form').reset();
        }
    });

    // Handle Update Data form submission
    document.getElementById('update-data-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('update-id').value;
        const name = document.getElementById('update-name').value;
        const age = document.getElementById('update-age').value;

        const response = await fetch('/update-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id, name, age }),
        });

        const result = await response.json();
        document.getElementById('response-message').textContent = result.status;
        if (response.ok) {
            document.getElementById('update-data-form').reset();
        }
    });

    // Handle Delete Data form submission
    document.getElementById('delete-data-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('delete-id').value;

        const response = await fetch('/delete-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id }),
        });

        const result = await response.json();
        document.getElementById('response-message').textContent = result.status;
        if (response.ok) {
            document.getElementById('delete-data-form').reset();
        }
    });

    // Fetch and display data on View Data page
    if (window.location.pathname === '/view-data') {
        fetchData();
    }

    async function fetchData() {
        const response = await fetch('/data');
        const data = await response.json();
        const tableBody = document.querySelector('#data-table tbody');
        tableBody.innerHTML = '';  // Clear existing rows

        data.forEach(row => {
            const tr = document.createElement('tr');
            row.forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell;
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });
    }
});
