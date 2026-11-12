document.addEventListener('DOMContentLoaded', function() {
    const djangoNotifications = document.querySelectorAll('.custom-notification');
    
    djangoNotifications.forEach(notification => {
        const closeBtn = notification.querySelector('.custom-close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                notification.classList.add('custom-fade-out');
            });
        }
        document.addEventListener('DOMContentLoaded', function() {
            const djangoNotifications = document.querySelectorAll('.custom-notification');
            
            djangoNotifications.forEach(notification => {
                const closeBtn = notification.querySelector('.custom-close-btn');
                if (closeBtn) {
                    closeBtn.addEventListener('click', function() {
                        notification.classList.add('custom-fade-out');
                    });
                }
        
                setTimeout(() => {
                    notification.classList.add('custom-fade-out');
                }, 5000);
            });
        });
        setTimeout(() => {
            notification.classList.add('custom-fade-out');
        }, 5000);
    });
});