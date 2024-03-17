browser.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        alert(request);
    }
);

