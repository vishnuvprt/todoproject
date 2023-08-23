const showAddFormLink = document.getElementById('showAddFormLink');
const addFormModal = new bootstrap.Modal(document.getElementById('addFormModal'));
const editFormModal = new bootstrap.Modal(document.getElementById('editFormModal'));

showAddFormLink.addEventListener('click', () => {
    addFormModal.show();
});

const editBtns = document.querySelectorAll('.edit-btn');
editBtns.forEach(btn => {
    btn.addEventListener('click', (event) => {
        const projectId = btn.getAttribute('data-project-id');
        // Fetch project details using AJAX and populate the edit form fields

        // Show the edit form modal
        editFormModal.show();
    });
});



//  duration calculator  

document.addEventListener("DOMContentLoaded", function() {
const startDateInput = document.getElementById("floatingSdate");
const endDateInput = document.getElementById("floatingEdate");
const durationInput = document.getElementById("floatingDuration");

startDateInput.addEventListener("change", calculateDuration);   
endDateInput.addEventListener("change", calculateDuration);

function calculateDuration() {
const startDate = new Date(startDateInput.value);
const endDate = new Date(endDateInput.value);

if (!isNaN(startDate) && !isNaN(endDate)) {
    const timeDifference = Math.abs(endDate - startDate);
    const daysDifference = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));
    const diff=daysDifference +' '+'Days'
    durationInput.value = diff;
}
}
});


const showTaskAddFormLink = document.getElementById('addTaskFormModal');
const addTaskFormModal = new bootstrap.Modal(document.getElementById('addTaskModal'));


showTaskAddFormLink.addEventListener('click', () => {
    addTaskFormModal.show();
});




