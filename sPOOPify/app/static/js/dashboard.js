document.addEventListener('DOMContentLoaded', () => {
    const genreButtons = document.querySelectorAll('.genre-button');
    const songsContainer = document.getElementById('songs-list');

    genreButtons.forEach(button => {
        button.addEventListener('click', () => {
            const genre = button.dataset.genre;

            fetch(`/filter_songs?genre=${genre}`)
                .then(response => response.json())
                .then(data => {
                    songsContainer.innerHTML = '';

                    // Add filtered songs
                    data.songs.forEach(song => {
                        const songItem = document.createElement('li');
                        songItem.classList.add('song-item');
                        songItem.innerHTML = `
                            <span class="song-title">${song.title} - ${song.genre}</span>
                            <div class="audio-container">
                                <div class="custom-player" data-song="/static/music/${song.file_path}">
                                    <button class="play-pause">▶️</button>
                                    <div class="progress-bar">
                                        <div class="progress"></div>
                                    </div>
                                    <span class="time">0:00</span>
                                    <input type="range" class="volume-slider" min="0" max="1" step="0.1" value="1">
                                </div>
                            </div>
                        `;
                        songsContainer.appendChild(songItem);
                    });

                    // Reinitialize custom players for the newly added songs
                    InitCustomPlayer();
                })
                .catch(error => console.error('Error:', error));
        });
    });

    // Initialize custom players for songs loaded initially
    InitCustomPlayer();
});

// Custom player initialization function

