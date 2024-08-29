async function fetchCuratedVideos() {
    // Get the user input for video length
    const videoLength = document.getElementById('videoLength').value;

    // Validate the input
    if (!videoLength || videoLength <= 0) {
        alert("Please enter a valid video length.");
        return;
    }

    // Display loading message while fetching data
    const videoResultsDiv = document.getElementById('videoResults');
    videoResultsDiv.innerHTML = "Loading...";

    try {
        // Fetch the videos from the backend server
        const response = await fetch(`http://127.0.0.1:5000/curate_videos?n=${videoLength}`);

        // Check if the response status is OK (status code 200)
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.status} ${response.statusText}`);
        }

        // Parse the response as JSON
        const videos = await response.json();

        // Clear the loading message
        videoResultsDiv.innerHTML = '';

        // Check if there are any videos returned
        if (videos.length === 0) {
            videoResultsDiv.innerHTML = "No videos found for the given length.";
            return;
        }

        // Display the curated videos
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

    } catch (error) {
        console.error("Error fetching videos:", error);
        videoResultsDiv.innerHTML = "An error occurred while fetching videos. Please try again.";
    }
}

// Event listener for button click or form submission
document.getElementById('fetchButton').addEventListener('click', fetchCuratedVideos);
