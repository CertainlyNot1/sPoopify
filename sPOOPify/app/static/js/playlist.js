document.addEventListener('DOMContentLoaded', function() {
    const createPlaylistButton = document.getElementById('createPlaylistButton');
    const playlistModal = document.getElementById('playlist-modal')
    const closeModalButton = document.getElementById('close-modal')
    const savePlayListButton = document.getElementById('save-playlist')
    const playlistNameInput = document.getElementById('playlist-name')

    createPlaylistButton.addEventListener('click', function() {
        playlistModal.classList.remove('hidden');

    });

    closeModalButton.addEventListener('click', function() {
        playlistModal.classList.add('hidden');
    })

    savePlayListButton.addEventListener('click', function() {
        const playlistName = playlistNameInput.ariaValueMax.trim();
    

        if (playlistName) {
            fetch('/playlists/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'name=${playlistName}'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Created playlist successfully!');
                    playlistModal.classList.add('hiddenn');
                    location.reload();
                } else {
                    alert('A problem occured while creating a playlist =(')
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('A problem occured while creating a playlist =(');
            });
        } else {
            alert('Please type in the name of the playlist.')
        }
    });
});