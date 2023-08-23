$(document).ready(function() {
    var rowIndex = 1;
    $('#addform').submit(function(event) {
        event.preventDefault();
        
        $.ajax({
            url: '/myapp/projects/',
            type: 'POST',
            data: $(this).serialize(),
            dataType: 'json', 
            success: function(response) {


                alert('New Project Added!');
                

            

                var newRow = '<tr>' +
                '<th scope="row"><a href="#">'+rowIndex+'</a></th>' +
                '<td>' + response.projectname + '</td>' +
                '<td><a href="#" class="text-primary">' + response.description + '</a></td>' +
                '<td>' + response.startdate + ' to ' + response.enddate + '<br>' + response.duration + '</td>' +
                '<td><a href="#" class="btn btn-primary edit-btn" data-bs-toggle="modal" data-bs-target="#editFormModal" data-project-id="' + response.id + '"> <i class="bi bi-pencil"></i></a></td>' +
                '<td><a href="#" class="btn btn-danger delete-button" id="delete" yy="' + response.id + '"> <i class="bi bi-trash"></i></a></td>' +
                '</tr>';

                $('#projects-table tbody').append(newRow);
                rowIndex++;
                // Close the modal after adding the project
                $('#addFormModal').modal('hide');


                
            },
            error: function(xhr, status, error) {
                if (xhr.status === 400) {
                    var errors = JSON.parse(xhr.responseText).errors;
                    // Display validation errors to the user
                } else {
                  alert('Something Went wrong');                    }
            }
        });
    });





    const editBtns = document.querySelectorAll('.edit-btn');
    var projectIdr;
    editBtns.forEach(btn => {
        btn.addEventListener('click', (event) => {
            const projectId = btn.getAttribute('data-project-id');
            // Now you can use projectId in your AJAX request
            $.ajax({
            url: '/myapp/projects/' + projectId + '/edit/', // URL to your editing view
            method: 'GET',
            dataType: 'json',
            success: function(response) {

                $('#editFormModal #floatingName').val(response.projectname);
                $('#editFormModal #floatingTextarea').val(response.description);
                $('#editFormModal #floatingSdate').val(response.startdate);
                $('#editFormModal #floatingEdate').val(response.enddate);
                $('#editFormModal #floatingDuration').val(response.duration);
                var projectType = response.project_type;
                projectIdr = response.project_id;

                var selectElement = $('#editFormModal #floatingSelect');
                selectElement.find('option').each(function () {
                    if ($(this).val() === projectType) {
                        $(this).prop('selected', true);
                    } else {
                        $(this).prop('selected', false);
                    }
                });

                var projectType = response.project_type;

                var selectElement = $('#editFormModal #floatingSelect');
                selectElement.find('option').each(function () {
                    if ($(this).val() === projectType) {
                        $(this).prop('selected', true);
                    } else {
                        $(this).prop('selected', false);
                    }
                });

                $('#userField option').prop('selected', false);
    
                for (var i = 0; i < response.userlist.length; i++) {
                    var userId = response.userlist[i].user;
                    $('#userField option[value="' + userId + '"]').prop('selected', true);
                }






                $('#editFormModal').modal('show'); 


            },
            error: function(xhr, status, error) {
                console.error('Error fetching project data:', error);
            }
        });
    });

    // Event listener for the "Submit" button in the edit form
   
    $('#editFormSubmit').off('click').on('click', function(event) {
        event.preventDefault();
        var count=0;
        $.ajax({
            url: '/myapp/projects/' + projectIdr + '/edit/', // URL to your editing view
            method: 'POST',
            data: $('#editForm').serialize(),
            dataType: 'json',
            success: function(response) {
                
                alert("Project updated");
                count++;
                console.log("Updated project"+count);
                // Update the corresponding row with edited data
                var editedRow = $('#projects-table').find('tr[data-project-id="' + projectIdr + '"]');
                editedRow.find('td:eq(1)').html(response.projectname);
                editedRow.find('td:eq(2)').html(response.description);
                editedRow.find('td:eq(3)').html(response.startdate + ' to ' + response.enddate + '<br>' + response.duration);
                editedRow.find('td:eq(4)').html('<a href="#" class="btn btn-primary edit-btn" data-bs-toggle="modal" data-bs-target="#editFormModal" data-project-id="'+response.project_id+'"> <i class="bi bi-pencil"></i></a>');
                editedRow.find('td:eq(5)').html('<a href="#" class="btn btn-danger delete-button" id="delete" yy="'+response.project_id+'"> <i class="bi bi-trash"></i></a>');
                console.log("Updatfinish");
                setTimeout(function() {

                    $('#editFormModal').modal('hide');
                }, 500);
            },
            error: function(xhr, status, error) {
                console.error('Error editing project data:', error);
            }
        });
    });




});




$(document).on('click', '.delete-button', function (event) {
    event.preventDefault();
    
    var delete_id = $(this).attr('yy'); // Use the correct attribute name here
    
    var confirmDelete = confirm('Are you sure you want to delete this project?');
    if (!confirmDelete) {
        return; 
    }
    
    $.ajax({
        type: 'GET',
        url: `/myapp/deleteitem/${delete_id}/delete/`,  
        success: function(response) {
            if (response.success) {
                // Remove the deleted row from the table
                $(`.item-${delete_id}`).remove();
                alert('Item successfully deleted.');
                // window.location="/myapp/projects/"

            } else {
                alert('Error deleting item: ' + response.error);
            }
        },
        error: function() {
            alert('An error occurred while deleting the item.');
        }
    });
});
 



const filterForm = $('#filter-form');
const projectsTable = $('#projects-table tbody');
const paginationLinks = $('#pagination-links');


// Attach event listener to the form's submit button
filterForm.on('submit', function(event) {
    event.preventDefault();
    var c=1;
    // Serialize the form data and send an AJAX request
    $.ajax({
        type: 'GET',
        url: filterForm.attr('action'),
        data: filterForm.serialize(),
        success: function(response) {
            // Clear the current table content
            projectsTable.empty();

            // Loop through the filtered projects and update the table
            response.forEach(function(project) {
                const newRow = `
                    <tr>
                        <td><a href="#">`+c+`</a></td>
                        <td><a href="{% url 'projectteam' ${project.id} %}">${project.projectname}</a></td>
                        <td>${project.description}</td>
                        <td>${project.startdate} to ${project.enddate}<br>${project.duration}</td>
                        <td>${project.status}</td>
                    </tr>`;
                projectsTable.append(newRow);
                c++;
            });

            paginationLinks.html(response.pagination_links);
        },
        error: function(xhr, status, error) {
            console.error('Error filtering projects:', error);
        }
    });
});






let projectId; 


$('.add-task-button').on('click', function() {
    projectId = $(this).data('project-id');  // Assign value to projectId
    $('#project-id-input').val(projectId);
    $('#addTaskModal').modal('show');
});


$('#TaskFormBtn').off('click').on('click', function(event) {
    event.preventDefault();

    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  

    $.ajax({
        url: '/myapp/userassignedprojects/'+projectId+'/add/',
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },  // Include CSRF token in headers
        data:$('#TaskForm').serialize(),
        dataType: 'json',
        success: function(data) {
            console.log(data); 
            alert('Task Added');
            setTimeout(function() {
                $('#addTaskModal').modal('hide');
            }, 500);
           

        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
});










let taskid;

$('.edit-task-btn').on('click', function() {
    taskid = $(this).data('task-id'); 
    $('#task-id-input').val(taskid);
    $('#EditTaskFormModal').modal('show');
});



const editTaskBtns = document.querySelectorAll('.edit-task-btn');
var taskidr;
editTaskBtns.forEach(btn => {
    btn.addEventListener('click', (event) => {
        const taskidId = btn.getAttribute('data-task-id');
        
        $.ajax({
        url: '/myapp/userviewtasks/' + taskidId + '/edit/', 
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            
            $('#EditTaskFormModal #floatingName').val(response.title);
            $('#EditTaskFormModal #floatingTextarea').val(response.description);
            $('#EditTaskFormModal #floatingSdate').val(response.duedate);
            var priority = response.project_type;
            taskidr=taskidId;

            var selectElement = $('#EditTaskFormModal #floatingSelect');
            selectElement.find('option').each(function () {
                if ($(this).val() === priority) {
                    $(this).prop('selected', true);
                } else {
                    $(this).prop('selected', false);
                }
            });

            var status = response.status;

            var selectElement = $('#EditTaskFormModal #floatingSelect2');
            selectElement.find('option').each(function () {
                if ($(this).val() === status) {
                    $(this).prop('selected', true);
                } else {
                    $(this).prop('selected', false);
                }
            });


            $('#EditTaskFormModal').modal('show'); 


        },
        error: function(xhr, status, error) {
            console.error('Error fetching project data:', error);
        }
    });
});

// Event listener for the "Submit" button in the edit form

$('#edit-task-btn').off('click').on('click', function(event) {
    event.preventDefault();
    var count=0;
    $.ajax({
        url: '/myapp/userviewtasks/' + taskidr + '/edit/', 
        method: 'POST',
        data: $('#EditTaskForm').serialize(),
        dataType: 'json',
        success: function(response) {
            
            alert("Task updated");
            count++;
            console.log("Task Updated"+count);
            // Update the corresponding row with edited data
            var editedRow = $('#task-table').find('tr[data-project-id="' + taskidr + '"]');
            editedRow.find('td:eq(1)').html(response.title);
            editedRow.find('td:eq(2)').html(response.description);
            editedRow.find('td:eq(3)').html(response.duedate);
            editedRow.find('td:eq(4)').html('<a href="#" id="showAddFormLink" class="btn btn-primary edit-task-btn" data-task-id="'+response.taskidr+'" >Update <i class="bi-pencil"></i></a>');
            editedRow.find('td:eq(5)').html('<a href="#" id="showAddFormLink" class="btn btn-primary">Subtask <i class="bi-list-task"></i></a>');
            console.log("Updatfinish");
            setTimeout(function() {

                $('#EditTaskForm').modal('hide');
            }, 500);
        },
        error: function(xhr, status, error) {
            console.error('Error editing task data:', error);
        }
    });
});




});






$('#showSubTaskAddFormLink').on('click', function() {
    $('#addSubTaskFormModal').modal('show');
});


$('#addSubTaskSubmit').off('click').on('click', function(event) {
    event.preventDefault();

    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  

    $.ajax({
        url: '/myapp/addsubtask/',
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },  // Include CSRF token in headers
        data:$('#addSubTaskForm').serialize(),
        dataType: 'json',
        success: function(data) {
            console.log(data); 
            alert('Sub Task Added');
            setTimeout(function() {
                $('#addSubTaskFormModal').modal('hide');

            }, 500);

            var newRow = '<tr>' +
            '<th scope="row"><a href="#">...</a></th>' +
            '<td>' + data.title + '</td>' +
            '<td>' + data.status + '</td>' +
            '<td><a href="#" id="showEditFormLink" class="btn btn-primary">Update <i class="bi-pencil"></i></a></td>' +
            '<td><a href="#" id="delete" class="btn btn-danger">Delete <i class="bi-trash"></i></a></td>' +
            '</tr>';

            $('#subtasktable').append(newRow);
           

        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
});




















});


