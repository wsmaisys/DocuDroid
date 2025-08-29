// Temporary fix for modal
const modal = document.getElementById('welcomeModal');
const closeButton = document.querySelector('.modal-close');

// Update modal styles
if (modal) {
    modal.style.transition = 'opacity 0.3s ease-in-out';
}

function showWelcomeModal() {
    if (modal) {
        modal.style.opacity = '0';
        modal.style.display = 'flex';
        requestAnimationFrame(() => {
            modal.style.opacity = '1';
        });
        localStorage.setItem('welcomeShown', 'true');
    }
}

function closeWelcomeModal() {
    if (modal) {
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    }
}

// Add click event listener for close button
if (closeButton) {
    closeButton.addEventListener('click', closeWelcomeModal);
}

// Initialize welcome modal state
window.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('welcomeShown')) {
        showWelcomeModal();
    } else {
        if (modal) {
            modal.style.display = 'none';
        }
    }
});