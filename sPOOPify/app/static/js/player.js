function InitCustomPlayer() {
    document.querySelectorAll('.custom-player').forEach(player => {
        const audio = new Audio(player.getAttribute('data-song'));
        const playButton = player.querySelector('.play-pause');
        const progressBar = player.querySelector('.progress-bar');
        const progress = player.querySelector('.progress');
        const time = player.querySelector('.time');
        const volumeSlider = player.querySelector('.volume-slider');

        // Play and pause functionality
        playButton.addEventListener('click', () => {
            if (audio.paused) {
                audio.play();
                playButton.textContent = '⏸';
            } else {
                audio.pause();
                playButton.textContent = '▶️';
            }
        });

        // Update progress and time display
        audio.addEventListener('timeupdate', () => {
            const percent = (audio.currentTime / audio.duration) * 100;
            progress.style.width = `${percent}%`;
            time.textContent = formatTime(audio.currentTime);
        });

        // Seek functionality
        progressBar.addEventListener('click', (event) => {
            const width = progressBar.offsetWidth;
            const clickX = event.offsetX;
            const duration = audio.duration;
            audio.currentTime = (clickX / width) * duration;
        });

        // Volume control
        volumeSlider.addEventListener('input', () => {
            audio.volume = volumeSlider.value;
        });

        // Format time display
        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        }
    });
}