////////////////////
// Wait DOM load //
//////////////////


document.addEventListener('DOMContentLoaded', function() {

  // By default, load the inbox //
  load_mailbox('inbox');

  //////////////////////
  // Event Listeners //
  ////////////////////
  
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').onsubmit = () => {
    const recipients = document.querySelector('#compose-recipients').value
    const subject = document.querySelector('#compose-subject').value
    const body = document.querySelector('#compose-body').value

    fetch('/emails', {method: 'POST', body: JSON.stringify({recipients:recipients, subject:subject, body:body})})
    .then(response => response.json())
    .then(result => {alert(result.message)});

    return false
  };


  document.querySelector('#archive-email').onclick = () => {
    const data = document.querySelector('#delete-email').dataset
    if (data.archived === 'true') {
      unarchive_email(data.email_id)
    } else if (data.archived === 'false') {
      archive_email(data.email_id)
    }
  }

  document.querySelector('#delete-email').onclick = () => {
    delete_email(document.querySelector('#delete-email').dataset.email_id)
  }

  document.querySelector('#reply-email').onclick = () => {
    const data = document.querySelector('#reply-email').dataset
    load_reply(data.sender, data.subject, data.body)
  }
});


////////////////
// Functions //
//////////////
  
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#mailbox-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-recipients').disabled = false;
  document.querySelector('#compose-subject').disabled = false;
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#mailbox-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#mailbox-view-title').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    document.querySelectorAll(".email").forEach((item) => {
      item.remove()
    })
    
    emails.forEach((email) => {
      const div = document.createElement('div')
      const email_id = `id${email.id}`
      div.className = "grid email"
      div.id = email_id
      div.style.marginLeft = "-5px"
      div.onclick = function() {load_email(email.id)}
      document.querySelector("#mailbox-view").append(div)

      const list = ['sender', 'subject', 'timestamp']
      list.forEach((column) => {
        const element = document.createElement('span')
        element.innerHTML = email[column]
        element.className = "grid-item"
        element.style.paddingLeft = "5px"
        document.querySelector(`#${email_id}`).append(element)
      })

      if ( email.read == false ) {
        const png = document.createElement('img')
        png.src = "/static/mail/unread.png"
        png.alt = "error"
        const span = document.createElement('span')
        span.className = "grid-item"
        span.append(png)
        document.querySelector(`#${email_id}`).append(span)
      } else if ( email.read == true ) {
        const png = document.createElement('img')
        png.src = "/static/mail/read.png"
        png.alt = "error"
        const span = document.createElement('span')
        span.className = "grid-item"
        span.append(png)
        document.querySelector(`#${email_id}`).append(span)
      }
    })
  });
}


function load_email(id) {
  document.querySelector('#mailbox-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  fetch(`/emails/${id}`, { method: 'PUT', body: JSON.stringify({ read: true })})
  // fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#from').innerHTML = `<span style='font-weight: bold;'>From: </span> ${email.sender}`
    document.querySelector('#to').innerHTML = `<span style='font-weight: bold;'>To: </span> ${email.recipients}`
    document.querySelector('#subject').innerHTML = `<span style='font-weight: bold;'>Subject: </span> ${email.subject}`
    document.querySelector('#timestamp').innerHTML = `<span style='font-weight: bold;'>Timestamp: </span> ${email.timestamp}`

    const temp = email.body
    const body = temp.replace(/\n/g, '<br>')
    document.querySelector('#email-body').innerHTML = body

    document.querySelector('#delete-email').dataset.email_id = email.id
    document.querySelector('#delete-email').dataset.archived = email.archived
    document.querySelector('#reply-email').dataset.sender = email.sender
    document.querySelector('#reply-email').dataset.subject = email.subject
    document.querySelector('#reply-email').dataset.body = email.body

    if (email.archived === true) {
      document.querySelector('#archive-email').innerHTML = "Unarchive"
    } else if (email.archived === false) {
      document.querySelector('#archive-email').innerHTML = "Archive"
    }
  })
}

function load_reply(sender, subject, body) {
  document.querySelector('#mailbox-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  console.log([sender, subject, body])
  document.querySelector('#compose-recipients').value = sender;
  document.querySelector('#compose-subject').value = `Re: ${subject}`;
  document.querySelector('#compose-body').value = `\n------------------------------ \n ${body}`;

  document.querySelector('#compose-recipients').disabled = true;
  document.querySelector('#compose-subject').disabled = true;
}

function delete_email(id) {
  fetch(`/delete/${id}`)
  return load_mailbox('inbox')
}

function archive_email(id) {
  fetch(`/emails/${id}`, { method: 'PUT', body: JSON.stringify({ archived: true })})
  return load_mailbox('inbox')
}

function unarchive_email(id) {
  fetch(`/emails/${id}`, { method: 'PUT', body: JSON.stringify({ archived: false })})
  return load_mailbox('archived')

}

