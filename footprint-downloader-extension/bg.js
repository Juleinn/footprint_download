chrome.downloads.onChanged.addListener((download_delta) => {
    if(download_delta.filename !== undefined && download_delta !== null){
        current_filename = download_delta.filename.current;
        console.log({current_filename});

        let body =  JSON.stringify({
            filename: current_filename,
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
    }
})
