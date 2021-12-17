console.log("file is connected")
function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId}),
    }).then((_res) => {
        window.location.href = "/"; //reload the homepage
});

// takes noteId we passed and send a post request to the deletnote endpoint
// once it gets a response, it will reload the window