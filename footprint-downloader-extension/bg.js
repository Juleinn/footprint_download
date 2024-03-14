chrome.downloads.onChanged.addListener((download_delta) => {
    console.log({download_delta});
    if(download_delta.filename !== undefined && download_delta !== null){
        current_filename = download_delta.filename.current;
        console.log({current_filename});


        chrome.tabs.getSelected(null,function(tab) {
            console.log({tab});
            if(tab.url === null && tab.url === undefined) {
                alert('Failed to retrieve hostname from download tab');
                return;
            }

            let body =  JSON.stringify({
                filename: current_filename,
                tab_url: tab.url,
            })
            fetch("http://localhost:2222", {
                method: "POST",
                body: body,
                headers: {
                    "Content-Length": body.length,
                }
            }).catch((err)=>{
                    console.log({err})
                })
        });

    }
})

