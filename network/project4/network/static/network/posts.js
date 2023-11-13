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
        else if (element.id === 'follow-button') {
            follow(element);
        }
    });
});


/**
 * Provides a mechanism for users to edit the text content of their own posts. Content
 * is updated but metadata such as the timestamp of the original post is maintained.
 * @param {HTMLElement} editButton - The button the user clicked to edit the post
 */
function edit(editButton) {
    const post = editButton.parentElement
    const content = post.getElementsByClassName('post-content')[0];
    const likeButton = post.getElementsByClassName('like')[0];

    // Create a text area and "Save" button
    const textarea = document.createElement('textarea');
    const saveButton = document.createElement('button');
    saveButton.className = 'btn btn-primary';   // Apply Bootstrap class
    saveButton.innerHTML = 'Save changes';

    // Set the text area value to the current content
    textarea.value = content.innerHTML;

    // Replace the post content with the text area and save button
    post.replaceChild(textarea, content);
    post.appendChild(saveButton);

    // Hide like and edit buttons
    editButton.style.display = 'none';
    likeButton.style.display = 'none';

    // Save changes when the user clicks the save button
    saveButton.addEventListener('click', () => {
        // Update the post content with the text area value
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
                // Remove the text area and save button
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


/**
 * Allows users to like or unlike a post by clicking a button
 * @param {HTMLElement} likeButton - The button that triggered the Like action
 */
function like(likeButton) {
    const post = likeButton.parentElement;
    const likeCount = post.getElementsByClassName('like-count')[0];

    // Make a PUT request to update the post likes server-side
    fetch(`/posts/${post.id}`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(data => {
        // Update count on the page
        likeCount.textContent = data;
    })
    .catch(error => {
        console.log('Error:', error);
    });
}


/**
 * Handles the follow/unfollow action.
 * @param {HTMLElement} followButton - The button triggering the follow action.
 */
function follow(followButton) {
    fetch(window.location.href, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // If the user just unfollowed the profile, set button text to 'Follow'. Else, set to 'Unfollow'.
        followButton.innerHTML = data.unfollow ? 'Follow' : 'Unfollow' ;
        // Update follower count displayed
        document.querySelector('#number-of-followers').innerHTML = 'Followers: ' + parseInt(data.follower_count);
    })
    .catch(error => {
        console.log('Error:', error);
    });
}