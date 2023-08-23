
const showTaskAddFormLink = document.getElementById('addTaskFormModal');
const addTaskFormModal = new bootstrap.Modal(document.getElementById('addTaskModal'));

showTaskAddFormLink.addEventListener('click', () => {
    addTaskFormModal.show();
});