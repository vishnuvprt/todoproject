
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





