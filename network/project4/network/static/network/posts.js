document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', event => {
        // Find what was clicked on
        const element = event.target;

        // Check if the user clicked on a hide button
        if (element.className === 'btn btn-link edit-button') {
            edit(element);
        }
        else if (element.className === 'like') {
            like(element);
        }
    });
});


function edit(editButton) {
    const post = editButton.parentElement
    const content = post.getElementsByClassName('post-content')[0];
    // Create a text area and "Save" button
    const textarea = document.createElement('textarea');
    const saveButton = document.createElement('button');
    saveButton.className = 'btn btn-primary';   // Apply Bootstrap class
    // Set the text area value to the current content
    textarea.value = content.innerHTML;

    // Configure the "Save" button
    saveButton.innerHTML = 'Save changes';

    // Replace the paragraph with the text area and "Save" button
    post.replaceChild(textarea, content);
    post.appendChild(saveButton);

    // Hide like and edit buttons
    editButton.style.display = 'none';
    const likeButton = post.getElementsByClassName('like')[0];
    likeButton.style.display = 'none';

    saveButton.addEventListener('click', () => {
        // Update the content with the text area value
        content.innerHTML = textarea.value;

        // Update the content server-side
        fetch(`/posts/${post.id}`, {
            method: 'POST',
            body: JSON.stringify({
                content: textarea.value
            })
        })
        .then(response => {
            if (response.ok) {
                // Remove the text area and "Save" button
                post.replaceChild(content, textarea);
                post.removeChild(saveButton);

                // Show like and edit buttons
                editButton.style.display = 'block';
                likeButton.style.display = 'block';
            } else {
                // Handle the case where the POST request fails
                alert('Failed to edit post.');
            }
        })
    });
}


function like(likeButton) {
    const post = likeButton.parentElement;
    const likeCount = post.getElementsByClassName('like-count')[0]

    // GET the post to get the current number of likes it has
    fetch(`/posts/${post.id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data.likes.value);

        const likes = parseInt(data.likes_count) + 1;
        console.log(likes);
        likeCount.textContent = likes.toString();
    })
    .catch(error => {
    console.log('Error:', error);
    });

    // Make a PUT request to update the post likes server-side
    fetch(`/posts/${post.id}`, {
        method: 'PUT'
    })
}
