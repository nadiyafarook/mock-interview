document.addEventListener('DOMContentLoaded', function () {
    console.log("Interview session loaded!");

    // Example of interaction: alert after 15 minutes
    setTimeout(function () {
        alert("Your interview session is over. Please check your feedback.");
    }, 15 * 60 * 1000); // 15 minutes in milliseconds
});
