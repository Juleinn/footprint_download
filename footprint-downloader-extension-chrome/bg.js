chrome.downloads.onChanged.addListener((download_delta) => {
    console.log({download_delta});
    if(download_delta.filename !== undefined && download_delta !== null){
        current_filename = download_delta.filename.current;
        // analyse only zip archives 
        if (current_filename.includes(".zip") === false) {
            return;
        }

        chrome.tabs.getSelected(null,function(tab) {

            console.log({tab});
            if(tab.url === null && tab.url === undefined) {
                alert('footprintdownload : Failed to retrieve hostname from download tab');
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
            })
                .then((response)=>{
                    console.log({response});
                    response.text().then((text)=>{
                        if( response.status === 200 ){
                            chrome.tabs.sendMessage(tab.id, 'footprintdownload : Success. Reload eeschema/symbol library to access new symbol and footprint');
                        } else {
                            chrome.tabs.sendMessage(tab.id, `footprintdownload : Failed: ${text}`);
                        }
                    })
                }) 
                .catch((err)=>{
                    console.log({err})
                    chrome.tabs.sendMessage(tab.id, 'footprintdownload : Error while sending filename to server. Is server started ?');
                })
        });

    }
})

