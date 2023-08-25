$(document).ready(function() {
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
                '<th scope="row"><a href="#">'+response.slno+'</a></th>' +
                '<td><a href="#" class="text-primary">' + response.projectname + '</a></td>' +
                '<td>' + response.description + '</td>' +
                '<td>' + response.startdate + ' to ' + response.enddate + '<br>' + response.duration + '</td>' +
                '<td><span class="badge bg-info"><i class="bi bi-check-circle me-1"></i>'+response.status+'</span></td>' +
                '<td><a href="#" class="btn btn-primary edit-btn" data-bs-toggle="modal" data-bs-target="#editFormModal" data-project-id="' + response.id + '"> <i class="bi bi-pencil"></i></a></td>' +
                '<td><a href="#" class="btn btn-danger delete-button" id="delete" yy="' + response.id + '"> <i class="bi bi-trash"></i></a></td>' +
                '</tr>';

                $('#projects-table tbody').append(newRow);
                rowIndex++;
                $('#addFormModal').modal('hide');


                
            },
            error: function(xhr, status, error) {
                if (xhr.status === 400) {
                    var errors = JSON.parse(xhr.responseText).errors;
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
            projectIdr=projectId
            $.ajax({
            url: '/myapp/projects/' + projectId + '/edit/', 
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

   
    $('#editFormSubmit').off('click').on('click', function(event) {
        event.preventDefault();
        var count=0;
        $.ajax({
            
            url: '/myapp/projects/' + projectIdr + '/edit/', 
            method: 'POST',
            data: $('#editForm').serialize(),
            dataType: 'json',
            success: function(response) {
                
                alert("Project updated");
                count++;
                console.log("Updated project"+count);
                var editedRow = $('#projects-table').find('tr[data-project-id="' + projectIdr + '"]');
                editedRow.find('td:eq(0)').html(response.projectname);
                editedRow.find('td:eq(1)').html(response.description);
                editedRow.find('td:eq(2)').html(response.startdate + ' to ' + response.enddate + '<br>' + response.duration);
                if(response.status=='Completed'){
                    editedRow.find('td:eq(3)').html('<span class="badge bg-success"><i class="bi bi-check-circle me-1"></i>'+response.status+'</span>');
                }
                else if(response.status=='Ongoing'){
                    editedRow.find('td:eq(3)').html('<span class="badge bg-primary"><i class="bi bi-check-circle me-1"></i>'+response.status+'</span>');

                }
                else if(response.status=='Cancel'){
                    editedRow.find('td:eq(3)').html('<span class="badge bg-danger"><i class="bi bi-check-circle me-1"></i>'+response.status+'</span>');

                }
                else if(response.status=='Onhold'){
                    editedRow.find('td:eq(3)').html('<span class="badge bg-secondary"><i class="bi bi-check-circle me-1"></i>'+response.status+'</span>');

                }
                else{

                   editedRow.find('td:eq(3)').html('<span class="badge bg-info"><i class="bi bi-check-circle me-1"></i>'+response.status+'</span>');
                }




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
    
    var delete_id = $(this).attr('yy'); 
    
    var confirmDelete = confirm('Are you sure you want to delete this project?');
    if (!confirmDelete) {
        return; 
    }
    
    $.ajax({
        type: 'GET',
        url: `/myapp/deleteitem/${delete_id}/delete/`,  
        success: function(response) {
            if (response.success) {

                var editedRow = $('#projects-table').find('tr[data-project-id="' + delete_id + '"]');
                editedRow.remove();
                alert('Item successfully deleted.');

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


filterForm.on('submit', function(event) {
    event.preventDefault();
    var c=1;
    var status;
    $.ajax({
        type: 'GET',
        url: filterForm.attr('action'),
        data: filterForm.serialize(),
        success: function(response) {
            console.log(response); 

            projectsTable.empty();

            alert('hlooooooo')

            response.project.forEach(function(project) {


                if(project.status=='Completed'){
                    status='<span class="badge bg-success"><i class="bi bi-check-circle me-1"></i>'+project.status+'</span>'
                }
                else if(project.status=='Ongoing'){
                    status='<span class="badge bg-primary"><i class="bi bi-check-circle me-1"></i>'+project.status+'</span>'
                }
                else if(project.status=='Cancel'){
                    status='<span class="badge bg-danger"><i class="bi bi-check-circle me-1"></i>'+project.status+'</span>'
                }
                else if(project.status=='Onhold'){

                    status='<span class="badge bg-secondary"><i class="bi bi-check-circle me-1"></i>'+project.status+'</span>'

                }
                else{

                    status='<span class="badge bg-info"><i class="bi bi-check-circle me-1"></i>'+project.status+'</span>'

                }

                const newRow = `
                    <tr>
                        <td><a href="#">`+c+`</a></td>
                        <td><a href="/myapp/projectteam/${project.id}">${project.projectname}</a></td>
                        <td>${project.description}</td>
                        <td>${project.startdate} to ${project.enddate}<br>${project.duration}</td>
                        <td>${status}</td>
                        <td><a href="#" class="btn btn-primary edit-btn" data-bs-toggle="modal" data-bs-target="#editFormModal" data-project-id="${ project.id }"> <i class="bi bi-pencil"></i></a></td>
                        <td><a href="#" class="btn btn-danger delete-button" id="delete" yy="${ project.id }"> <i class="bi bi-trash"></i></a></td>
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
    projectId = $(this).data('project-id');  
    $('#project-id-input').val(projectId);
    $('#addTaskModal').modal('show');
});


$('#TaskFormBtn').off('click').on('click', function(event) {
    event.preventDefault();

    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  

    $.ajax({
        url: '/myapp/userassignedprojects/'+projectId+'/add/',
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken }, 
        data:$('#TaskForm').serialize(),
        dataType: 'json',
        success: function(data) {
            console.log(data); 
            alert(data.message);
            setTimeout(function() {
                $('#addTaskModal').modal('hide');
            }, 500);
            
           

        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
});




const tasktable = $('#task-table');

$('#AddTask').off('click').on('click', function(event) {
    event.preventDefault();

    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  
    const formData = new FormData($('#AddTaskForm')[0]);  // Convert the form to FormData

    var c=1;
    $.ajax({
        url: '/myapp/usertasks/',
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken }, 
        data:formData,
        dataType: 'json',
        processData: false,  // Prevent jQuery from processing the data
        contentType: false,  // Prevent jQuery from setting contentType
        success: function(data) {
            console.log(data); 
            alert(data.message);
            setTimeout(function() {
                $('#addTaskModal').modal('hide');
            }, 500);
    
            const newRow = `
            <tr data-task-id="${data.id}">
                <td><a href="#">${data.id}</a></td>
                <td>${data.title}</td>
                <td>${data.description}</td>
                <td>${data.duedate}</td>
                <td><span class="badge bg-danger">High </span></td>
                <td><a href="#" class="btn btn-primary edit-task-btn" data-task-id="${data.id}"><i class="bi-pencil"></i></a></td>
                <td><a href="#" class="btn btn-danger" data-task-id="${data.id}"><i class="bi-trash"></i></a></td>
                <td><a href="/myapp/subtask/${data.id}" class="btn btn-primary">Subtask <i class="bi-list-task"></i></a></td>
            </tr>`;
                tasktable.append(newRow);
                c++;
        
        },
        error: function(error) {
            console.error('Error:', error);
            console.log(error);

        }
    });
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
            var priority = response.priority;
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



$('#EditTaskSubmit').off('click').on('click', function(event) {
    event.preventDefault();
    $.ajax({
        url: '/myapp/userviewtasks/' + taskidr + '/edit/', 
        method: 'POST',
        data: $('#EditTaskForm').serialize(),
        dataType: 'json',
        success: function(response) {
            
            alert("Task updated");
            
            var editedRow = $('#task-table').find('tr[data-task-id="' + taskidr + '"]');
            editedRow.find('td:eq(0)').html(response.title);
            editedRow.find('td:eq(1)').html(response.description);
            editedRow.find('td:eq(2)').html(response.duedate);
            editedRow.find('td:eq(3)').html('<a href="#" id="edit-task-btn" class="btn btn-primary edit-task-btn" data-task-id="'+response.taskid+'" ><i class="bi-pencil"></i></a>');
            editedRow.find('td:eq(4)').html('<a href="#" id="deletetask" class="btn btn-danger" data-task-id="'+response.taskid+'" > <i class="bi-trash"></i></a>');
            editedRow.find('td:eq(5)').html('<a href="#" id="showAddFormLink" class="btn btn-primary">Subtask <i class="bi-list-task"></i></a>');
            console.log("Updatfinish");
           
            setTimeout(function() {
                $('#EditTaskFormModal').modal('hide');
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
        headers: { 'X-CSRFToken': csrfToken }, 
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
            '<td><a href="#" id="showEditsubtaskFormLink" class="btn btn-primary edit-subtask-btn" data-subtask-id="'+data.id+'" > <i class="bi-pencil"></i></a></td>' +
            '<td><a href="#" id="delete" class="btn btn-danger"> <i class="bi-trash"></i></a></td>' +
            '</tr>';

            $('#subtasktable').append(newRow);
           

        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
});





const editSubTaskBtns = document.querySelectorAll('.edit-subtask-btn');
var subtaskidr;
editSubTaskBtns.forEach(btn => {
    btn.addEventListener('click', (event) => {
        const taskidId = btn.getAttribute('data-subtask-id');
        subtaskidr=taskidId;
        $.ajax({
        url: '/myapp/subtask/'+taskidId+'/edit/', 
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            
            $('#editSubtaskFormModal #floatingName').val(response.title);


            var status = response.status;

            var selectElement = $('#editSubtaskFormModal #floatingSelect2');
            selectElement.find('option').each(function () {
                if ($(this).val() === status) {
                    $(this).prop('selected', true);
                } else {
                    $(this).prop('selected', false);
                }
            });


            $('#editSubtaskFormModal').modal('show'); 


        },
        error: function(xhr, status, error) {
            console.error('Error fetching project data:', error);
        }
    });
});






$('#EditSubTaskSubmit').off('click').on('click', function(event) {
    event.preventDefault();
    $.ajax({
        url: '/myapp/subtask/' + subtaskidr + '/edit/', 
        method: 'POST',
        data: $('#editSubtaskForm').serialize(),
        dataType: 'json',
        success: function(response) {
            
            alert("Subtask updated");
            
            var editedRow = $('#subtasktable').find('tr[data-subtask-id="' + subtaskidr + '"]');
            editedRow.find('td:eq(0)').html(response.title);
            editedRow.find('td:eq(1)').html(response.status);
            editedRow.find('td:eq(2)').html('<a href="#" id="showEditsubtaskFormLink" class="btn btn-primary edit-subtask-btn" data-subtask-id="'+response.taskid+'" > <i class="bi-pencil"></i></a>');
            editedRow.find('td:eq(3)').html('<a href="#" id="delete" class="btn btn-danger"> <i class="bi-trash"></i></a>');
            console.log("Updatfinish");
           
            setTimeout(function() {
                $('#editSubtaskFormModal').modal('hide');
            }, 500);
        },
        error: function(xhr, status, error) {
            console.error('Error editing task data:', error);
        }
    });
});



});


$('#deletesubtask').off('click').on('click', function(event)  {
    event.preventDefault();
    const taskidId = $(this).data('subtask-id');
    var confirmDelete = confirm('Are you sure you want to delete this subtask?');
    if (!confirmDelete) {
        return; 
    }
    $.ajax({
        url: '/myapp/subtask/'+taskidId+'/delete/', 
        method: 'GET',
        dataType: 'json',
        success: function(response) {

            var editedRow = $('#subtasktable').find('tr[data-subtask-id="' + taskidId + '"]');
            editedRow.remove();
            alert('Subtask Deleted.');

        },
        error: function(xhr, status, error) {
            console.error('Error subtask:', error);
        }
    });



    
});



$('#deletetask').off('click').on('click', function(event)  {
    event.preventDefault();
    const taskidId = $(this).data('task-id');
    var confirmDelete = confirm('Are you sure you want to delete this task?');
    if (!confirmDelete) {
        return; 
    }
    $.ajax({
        url: '/myapp/userviewtasks/'+taskidId+'/delete/', 
        method: 'GET',
        dataType: 'json',
        success: function(response) {

            var editedRow = $('#task-table').find('tr[data-task-id="' + taskidId + '"]');
            editedRow.remove();
            alert('Task Deleted.');

        },
        error: function(xhr, status, error) {
            console.error('Error Task:', error);
        }
    });



    
});










$('#showAddFormLink').on('click', function() {
    $('#addFormModal').modal('show');
});




function ViewProfileInfo() {
    $.ajax({
    type: "GET",
    url: "/myapp/userprofiledata/",
    success: function (data) {
        console.log(data);
        
        $("#fullName").val(data.name);
        $("#Job").val(data.job);
        $("#Phone").val(data.phone);
        $("#Email").val(data.email);

        if(data.photo == 'None'){

            $("#profileimg").attr("src",data.photo);
        }
        else{

            $("#profileimg").attr("src", data.photo);

        }



    },
    });
}




ViewProfileInfo();


updateProfileImage();

$('#uploadImage').on('click', function(event) {
    event.preventDefault();
    $('#profileImageInput').click();
});

$('#profileImageInput').on('change', function() {
    uploadProfileImage();
});




function updateProfileImage() {

    $.ajax({
        type: 'GET',
        url: '/myapp/get-profile-photo/',
        success: function(data) {
            $('#profileimg').attr('src', data.photo);
            $('#dpimg').attr('src', data.photo);
        },
    });
}

function uploadProfileImage() {
    var formData = new FormData();
    formData.append('profile_image', $('#profileImageInput')[0].files[0]);
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  

    $.ajax({
        type: 'POST',
        url: '/myapp/upload-profile-photo/',
        data: formData,
        processData: false,
        contentType: false,
        headers: { 'X-CSRFToken': csrfToken }, 
        success: function(data) {
            if (data.success) {
                updateProfileImage();
            }
        },
    });



}





$('#removeImage').click(function(e) {
    e.preventDefault();
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  

    $.ajax({
      type: 'POST',
      url: '/myapp/remove-profile-photo/',
      headers: { 'X-CSRFToken': csrfToken }, 
      success: function (data) {
        $('#profileimg').attr('src', '/static/assets/img/20230814095643.jpg');
        $('#dpimg').attr('src', '/static/assets/img/20230814095643.jpg');
      },
      error: function (xhr, errmsg, err) {
      }
    });
  });




  $('#saveChange').off('click').on('click', function(event) {
    event.preventDefault();


    
    $.ajax({
        url: '/myapp/edit-profile/', 
        method: 'POST',
        data: $('#editprofileform').serialize(),
        dataType: 'json',
        success: function(response) {

            $('#fullName').val(response.name);
            $('#Job').val(response.job);
            $('#Phone').val(response.phone);
            $('#fname').text(response.name);
            $('#jobb').text(response.job);
            $('#ovfname').text(response.name);
            $('#ovjob').text(response.job);
            $('#ovphone').text(response.phone);

        
        },
        error: function(xhr, status, error) {
            console.error('Error editing task data:', error);
        }
    });
});





const filterFormuser = $('#filter-form-user');
const projectsTableUser = $('#projects-table-user tbody');
const paginationLinksUser = $('#pagination-links');

filterFormuser.on('submit', function(event) {
    event.preventDefault();

    $.ajax({
        type: 'GET',
        url: filterFormuser.attr('action'),
        data: filterFormuser.serialize(),
        dataType: 'json', 
        success: function(response) {
            console.log(response); 

            projectsTableUser.empty();
            var c = 1;

            response.project.forEach(function(project) {
                const newRow = `
                    <tr>
                        <td><a href="#">${c}</a></td>
                        <td><a href="{% url 'projectteam' ${project.id} %}">${project.projectname}</a></td>
                        <td>${project.description}</td>
                        <td>${project.startdate} to ${project.enddate}<br>${project.duration}</td>
                        <td><a href="#" class="btn btn-primary add-task-button" data-bs-toggle="modal" data-bs-target="#addTaskModal" data-project-id="${ project.id }" >Add Task <i class="bi bi-plus"></i></a></td>
                        <td><a href="{% url 'userviewtasks' ${ project.id } %}" class="btn btn-danger">Tasks <i class="bi bi-list-task"></i></a></td>
                    </tr>`;
                    projectsTableUser.append(newRow);
                c++;
            });

            paginationLinksUser.html(response.pagination_links);
        },
        error: function(xhr, status, error) {
            console.error('Error filtering projects:', error);
        }
    });
});






const taskfilterFormuser = $('#task-filter-form');
const taskTableUser = $('#task-table tbody');
const taskpaginationLinksUser = $('#task-pagination-links');

taskfilterFormuser.on('submit', function(event) {
    event.preventDefault();
   var pp="";
    $.ajax({
        type: 'GET',
        url: taskfilterFormuser.attr('action'),
        data: taskfilterFormuser.serialize(),
        dataType: 'json', 
        success: function(response) {
            console.log(response); 

            taskTableUser.empty();
            var c = 1;
            console.log(response.tasks);
            response.tasks.forEach(function(i) {
                
                if(i.priority == 'High'){
                    pp='<span class="badge bg-danger">High </span>'
                }
                else if(i.priority=='Medium'){
                    pp='<span class="badge bg-primary">Medium </span>'
                }
                else{
                    pp='<span class="badge bg-success">Low </span>'
                }

                const newRow = `
                    <tr>
                        <td><a href="#">${c}</a></td>
                        <td>${i.title}</a></td>
                        <td>${i.description}</td>
                        <td>${i.duedate}</td>
                        <td>${pp}</td>
                        <td><a href="#" id="edit-task-btn" class="btn btn-primary edit-task-btn" data-task-id="${ i.id }" > <i class="bi-pencil"></i></a></td>
                        <td><a href="#" id="deletetask" class="btn btn-danger" data-task-id="${ i.id }" > <i class="bi-trash"></i></a></td>
                        <td><a href="/myapp/subtask/${ i.id }" id="showAddFormLink" class="btn btn-primary">Subtask <i class="bi-list-task"></i></a></td>
                    </tr>`;
                    taskTableUser.append(newRow);
                c++;



            });
            const sortOption = $('#sort-option').val();
            const newURL = new URL(response.pagination_links);
            newURL.searchParams.set('sort_by', sortOption);
            response.pagination_links = newURL.toString();
            taskpaginationLinksUser.html(response.pagination_links);

        },
        error: function(xhr, status, error) {
            console.error('Error filtering task:', error);
        }
    });
});



const searchForm = $('#filter-staff');
const personList = $('#staff-table');
        searchForm.on('submit', function(event) {
            event.preventDefault();

            $.ajax({
                type: 'GET',
                url: searchForm.attr('action'),
                data: searchForm.serialize(),
                dataType: 'json',
                success: function(response) {
                    personList.empty();
                    var c = 1;
                    var photo=""
                    const newRow = `
                    <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">User</th>
                        <th scope="col">Email</th>
                        <th scope="col">Phone</th>
                    </tr>
                    </thead>`;
                    personList.append(newRow);
                    response.persons.forEach(function(person) {
                        if(person.photo == '/media/None'){
                            photo="/static/assets/img/20230814095643.jpg";
                        }
                        else{
                            photo=person.photo
                        }
                        const newRow = `
                        <tr>
                            <td><a href="#">${c}</a></td>
                            <td><img src='${photo}' height="50px" width="50px" alt="Profile" class="rounded-circle"><br>${person.name}</a></td>
                            <td>${person.email}</td>
                            <td>${person.phone}</td>
                           
                        </tr>`;
                        personList.append(newRow);
                        c++
                    });
                },
                error: function(xhr, status, error) {
                    console.error('Error searching persons:', error);
                }
          });
 });



 const newPasswordInput = document.getElementById('yourPassword');
    const confirmPasswordInput = document.getElementById('yourCPassword');
    const saveButton = document.getElementById('saveButton');
    const pmis = document.getElementById('pmis');
   
    function updateSaveButtonState() {
        const newPassword = newPasswordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (newPassword !== confirmPassword) {
            pmis.style.display = 'block';
            saveButton.disabled = true;
        } else {
            pmis.style.display = 'none';
            saveButton.disabled = false;
        }
    }

    newPasswordInput.addEventListener('input', updateSaveButtonState);
    confirmPasswordInput.addEventListener('input', updateSaveButtonState);

    $('form[id="cpform"]').validate({
        rules: {
            oldpassword: {
                required: true,
            },
            newpassword: {
                required: true,
                minlength: 8,
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$/,
            },
            confirmpassword: {
                equalTo: '#id_newpassword',
            },
        },
        messages: {
            newpassword: {
                minlength: 'Password must be at least 8 characters long',
                pattern: 'Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character (@$!%*?&)',
            },
            confirmpassword: {
                equalTo: 'Passwords do not match',
            },
        },
        submitHandler: function(form) {
            form.submit();
        }
    });


















});


