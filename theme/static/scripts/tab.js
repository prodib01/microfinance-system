document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.filterBtn');
    const tabContents = document.querySelectorAll('.tabContent');

    tabs.forEach((tab) => {
        tab.addEventListener('click', function () {
            const tabId = tab.id;
            const contentId = tabId.replace('tab', 'content');

            tabContents.forEach((content) => {
                content.classList.add('hidden');
            });

            tabs.forEach((t) => {
                t.classList.remove('active');
            });

            tab.classList.add('active');

            const targetContent = document.getElementById(contentId);
            targetContent.classList.remove('hidden');
        });

        if (tab.classList.contains('active')) {
            const tabId = tab.id;
            const contentId = tabId.replace('tab', 'content');
            const targetContent = document.getElementById(contentId);
            targetContent.classList.remove('hidden');
        }
    });
});
