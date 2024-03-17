browser.downloads.onChanged.addListener((download_delta) => {
    state = download_delta.state || null;
    exists = download_delta.exists || false;
    if(state && exists && exists.current === true && state.current === "complete") {
        browser.tabs.query({active: true, windowId: browser.windows.WINDOW_ID_CURRENT})
            .then(tabs => browser.tabs.get(tabs[0].id))
            .then(tab => {
                browser.downloads.search({limit: 1, orderBy: ["-startTime"]})
                    .then((items)=>{
                        let file = items[0]; //there should be only one
                        current_filename = file.filename;
                        if (current_filename.includes(".zip") === false) {
                            return;
                        }

                        let body =  JSON.stringify({
                            filename: current_filename,
                        })

                        fetch("http://localhost:2222", {
                            method: "POST",
                            body: body,
                            headers: {
                                "Content-Length": body.length,
                            }
                        })
                            .then((response)=>{
                                response.text().then((text)=>{
                                    console.log({response});
                                    if( response.status === 200 ){
                                        browser.tabs.sendMessage(tab.id, 'footprintdownload : Success. Reload eeschema/symbol library to access new symbol and footprint');
                                    } else {
                                        browser.tabs.sendMessage(tab.id, `footprintdownload : Failed: ${text}`);
                                    }
                                })
                            }, (err)=>{
                                    browser.tabs.sendMessage(tab.id, "footprintdownload : Is server running ?" + err );
                                }) 
                            .catch((err)=>{
                                browser.tabs.sendMessage(tab.id, "footprintdownload : Is server running ?" + err );
                            })
                    });
            });
    }
});
