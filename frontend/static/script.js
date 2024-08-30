async function fetchCuratedVideos() {
    const videoLength = document.getElementById('videoLength').value;
    const topic = document.getElementById('topic').value;

    if (!videoLength || videoLength <= 0) {
        alert("Please enter a valid video length.");
        return;
    }

    if (!topic) {
        alert("Please enter a topic or hashtag.");
        return;
    }

    const videoResultsDiv = document.getElementById('videoResults');
    videoResultsDiv.innerHTML = "Loading...";

    try {
        // Make sure the URL points to the correct backend URL and port
        const response = await fetch(`http://127.0.0.1:8080/curate_videos?n=${videoLength}&topic=${encodeURIComponent(topic)}`);
        const videos = await response.json();

        // Clear previous results and display videos
        videoResultsDiv.innerHTML = '';
        videos.forEach(video => {
            const videoItem = document.createElement('div');
            videoItem.classList.add('video-item');

            const videoTitle = document.createElement('div');
            videoTitle.classList.add('video-title');
            videoTitle.textContent = video.title;

            const videoLink = document.createElement('a');
            videoLink.href = video.url;
            videoLink.target = '_blank';
            videoLink.textContent = 'Watch on YouTube';

            videoItem.appendChild(videoTitle);
            videoItem.appendChild(videoLink);
            videoResultsDiv.appendChild(videoItem);
        });

        if (videos.length === 0) {
            videoResultsDiv.innerHTML = "No videos found for the given topic and length.";
        }

    } catch (error) {
        console.error("Error fetching videos:", error);
        videoResultsDiv.innerHTML = "An error occurred while fetching videos. Please try again.";
    }
}