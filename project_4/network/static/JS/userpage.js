addEventListener('DOMContentLoaded', () => {
    const csrftoken = Cookies.get('csrftoken');
    const username = document.querySelector('#username').innerHTML;
    const page_username = document.querySelector('#page_username').innerHTML;

    if (document.querySelector('#follow') || document.querySelector('#unfollow')) {
        document.querySelector('#follow').onclick = () => {
            const request = new Request(
                '/API/follow',
                {headers: {'X-CSRFToken': csrftoken}}
            );
            fetch(request, {method:'POST', body:JSON.stringify({username:username, page_username:page_username})})
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.response == 'OK') {
                    document.location.reload()
                }
            })
        }
        document.querySelector('#unfollow').onclick = () => {        
            const request = new Request(
                '/API/unfollow',
                {headers: {'X-CSRFToken': csrftoken}}
            );
            fetch(request, {method:'POST', body:JSON.stringify({username:username, page_username:page_username})})
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.response == 'OK') {
                    document.location.reload()
                }
            })
        }
    }

    if (document.querySelector('#back_page') || document.querySelector('#next_page')) {
        document.querySelector('#back_page').onclick = () => {
            let page = parseInt(document.querySelector('#paginator').value)
            if (page > 1) {
                let username = document.querySelector('#page_username').innerHTML.replace(/\s/g, '')
                window.location = `/user/${username}/${page - 1}`
            }
        }

        document.querySelector('#next_page').onclick = () => {
            let page = parseInt(document.querySelector('#paginator').value)
            let max_page = parseInt(document.querySelector('#max_page').value)
            if (page < max_page) {
                let username = document.querySelector('#page_username').innerHTML.replace(/\s/g, '')
                window.location = `/user/${username}/${page + 1}`
            }
        }
    }
})

function delete_post(id) {
    fetch(`/API/delete/${id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        window.location.reload()
    })
}

function edit_post(id) {
    document.querySelector(`#text_${id}`).disabled = false;
    document.querySelector(`#text_${id}`).style.border = '0.5px solid gray'
    document.querySelector(`#edit_${id}`).style.display = 'none'
    document.querySelector(`#save_${id}`).style.display = 'block'
}

function save_post(id) {
    const text = document.querySelector(`#text_${id}`).value
    const csrftoken = Cookies.get('csrftoken');

    const request = new Request(
        '/API/save',
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request, {method:'POST', body:JSON.stringify({id:id, text:text})})
    .then(response => response.json())
    .then(data => {
        if (data.response == 'OK') {
            document.querySelector(`#text_${id}`).disabled = true;
            document.querySelector(`#text_${id}`).style.border = 'none'
            document.querySelector(`#edit_${id}`).style.display = 'block'
            document.querySelector(`#save_${id}`).style.display = 'none'    
        }
    })
}


function like(id) {
    const username = document.querySelector('#username').innerHTML;
    document.querySelector(`#like_${id}`).style.display = 'none'
    document.querySelector(`#unlike_${id}`).style.display = 'block'
    document.querySelector(`#n_likes_${id}`).innerHTML = parseInt(document.querySelector(`#n_likes_${id}`).innerHTML) + 1

    const csrftoken = Cookies.get('csrftoken');
    const request = new Request(
        '/API/like',
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request, {method:'POST', body:JSON.stringify({id:id, username:username})})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        // window.location.reload()
    })
}

function unlike(id) {
    const username = document.querySelector('#username').innerHTML;
    document.querySelector(`#unlike_${id}`).style.display = 'none'
    document.querySelector(`#like_${id}`).style.display = 'block'
    document.querySelector(`#n_likes_${id}`).innerHTML = parseInt(document.querySelector(`#n_likes_${id}`).innerHTML) - 1

    const csrftoken = Cookies.get('csrftoken');
    const request = new Request(
        '/API/unlike',
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request, {method:'POST', body:JSON.stringify({id:id, username:username})})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        // window.location.reload()
    })
}
