function fetchData() {
    $.get('/data', function(data) {
        $('#data-body').empty();  // Clear existing data
        data.forEach(function(row) {
            $('#data-body').append(
                `<tr>
                    <td>${row[0]}</td>
                    <td>${row[1]}</td>
                    <td>${row[2]}</td>
                </tr>`
            );
        });
    });
}

$(document).ready(function() {
    fetchData();  // Fetch data on page load

    $('#sync-data').click(function() {
        $.post('/sync-data', function() {
            alert('Data synchronized between Google Sheets and MySQL');
            fetchData();  // Refresh data after sync
        });
    });

    $('#add-data-form').submit(function(event) {
        event.preventDefault();
        const id = $('#id').val();
        const name = $('#name').val();
        const age = $('#age').val();
        $.ajax({
            url: '/add-data',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ id: id, name: name, age: age }),
            success: function(response) {
                alert('Data added successfully');
                fetchData();  // Refresh data after addition
                $('#add-data-form')[0].reset();  // Reset form fields
            },
            error: function(xhr, status, error) {
                alert('Error adding data');
            }
        });
    });

    $('#update-data-form').submit(function(event) {
        event.preventDefault();
        const id = $('#update-id').val();
        const name = $('#update-name').val();
        const age = $('#update-age').val();
        $.ajax({
            url: '/update-data',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ id: id, name: name, age: age }),
            success: function(response) {
                alert('Data updated successfully');
                fetchData();  // Refresh data after update
                $('#update-data-form')[0].reset();  // Reset form fields
            },
            error: function(xhr, status, error) {
                alert('Error updating data');
            }
        });
    });

    $('#delete-data-form').submit(function(event) {
        event.preventDefault();
        const id = $('#delete-id').val();
        $.ajax({
            url: '/delete-data',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ id: id }),
            success: function(response) {
                alert('Data deleted successfully');
                fetchData();  // Refresh data after deletion
                $('#delete-data-form')[0].reset();  // Reset form fields
            },
            error: function(xhr, status, error) {
                alert('Error deleting data');
            }
        });
    });
});
