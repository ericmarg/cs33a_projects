let currentEmail = null;

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());
  document.querySelector('#mark-archived-button').addEventListener('click', () => archive(currentEmail));
  document.querySelector('#reply-button').addEventListener('click', () => compose_email(currentEmail));

  // By default, load the inbox
  load_mailbox('inbox');
});

/**
 * Composes a new email if called without an argument. If an email argument is provided, compose_email
 * provides reply functionality and the new email is sent as a response to the original with pre-populated fields.
 * @param email defaults to null, indicating a new email thread
 */
function compose_email(email = null) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-content').style.display = 'none';
  document.querySelector('#email-view-buttons').style.display = 'none';

  if (email === null) {   // Composing a new email to start a thread
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  } else {  // Replying to an existing email
    // Pre-populate the email fields
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value =
            // Add 'Re: ' to the start of the subject if it isn't there already (to indicate a reply)
            email.subject.startsWith('Re: ') ? email.subject : `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
  }

  // Send email upon form submission
  document.querySelector('form').onsubmit = function() {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value,
      })
    })
    .then(response => {
      if (response.ok) {
        // If the POST request is successful, load the sent mailbox
        load_mailbox('sent');
      } else {
        // Handle the case where the POST request fails
        alert('Email sending failed');
      }
    })
    // Catch any errors and log them to the console
    .catch(error => {
      console.log('Error:', error);
    });
    // Prevent default submission
    return false;
  };
}

/**
 * Loads the requested mailbox: inbox, sent mail, or archived. Displays the following information from all
 * relevant emails within their own div: sender, subject, and timestamp.
 * @param mailbox inbox, sent, or archive.
 */
function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';
  document.querySelector('#email-view-buttons').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show the emails in the mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Iterate through the returned array of emails
    emails.forEach(email => {
      // Create a div HTML element for each object
      const element = document.createElement('div');

      // Assign the div to the appropriate class for color differentiation based on whether it has been read
      element.setAttribute('class', email.read ? 'preview read' : 'preview unread');

      // Display email sender, subject, and timestamp information
      element.innerHTML = `FROM: ${email.sender}  |  SUBJECT: ${email.subject}  |  SENT: ${email.timestamp}`;

      // Add an event listener to open and display the email on click
      element.addEventListener('click', function() {
        // Set the email's read attribute to true since it has been clicked on
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        });
        // Display the email
        view_email(email.id);
      });
    // Add the email to the display
    document.querySelector('#emails-view').append(element);
    });
  })
  // Catch any errors and log them to the console
  .catch(error => {
    console.log('Error:', error);
  });
}

/**
 * Fetches an email using the given ID and displays it to the user.
 * The following email fields are displayed: sender, recipients, subject, body, timestamp.
 * @param emailID The ID of the email the user clicked on.
 */
function view_email(emailID) {
  // Show the email content and functionality buttons and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'block';
  document.querySelector('#email-view-buttons').style.display = 'block';

  // Reset div HTML to blank so that only the current email is being displayed
  document.querySelector('#email-content').innerHTML = '';

  // Fetch the email
  fetch(`/emails/${emailID}`)
  .then(response => response.json())
  .then(email => {
    // Assign email to global variable for the reply and archive button event listeners
    currentEmail = email;

    // Set the archive button text to 'Unarchive' if the email is archived, else set it to 'Archive'
    document.querySelector('#mark-archived-button').innerHTML = email.archived ? 'Unarchive' : 'Archive';

    // List required email fields
    let displayFields = ['sender', 'recipients', 'subject', 'body', 'timestamp'];
    // Loop through all email fields
    for (const key in email) {
      // Display the field if it's in the list
      if (email.hasOwnProperty(key) && displayFields.includes(key)) {
        const element = document.createElement('p');
        element.innerHTML = `${key}: ${email[key]}`;
        document.querySelector('#email-content').append(element);
      }
    }
  })
  // Catch any errors and log them to the console
  .catch(error => {
    console.log('Error:', error);
  });
}

/**
 * Allows a user to archive or un-archive an email by clicking on the archive/un-archive button in the email view.
 * @param email The email that is being archived/un-archived
 */
function archive(email) {
  if (email === null) return;

  // Use a PUT request to archive or un-archive the email
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      // If email is archived, un-archive it. If it's not archived, archive it.
      archived: !email.archived
    })
  })
  .then(response => {
    if (response.ok) {
      load_mailbox('inbox');  // Return to inbox
    } else {
      console.log('Archive/unarchive failed');
    }
  })
  // Catch any errors and log them to the console
  .catch(error => {
    console.log('Error:', error);
  });
}
