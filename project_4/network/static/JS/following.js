addEventListener('DOMContentLoaded', () => {

    document.querySelector('#submit').onclick = () => {
        const text = document.querySelector('#text').value;
        const username = document.querySelector('#username').innerHTML;
        const csrftoken = Cookies.get('csrftoken');
        
        const request = new Request(
            '/API/post',
            {headers: {'X-CSRFToken': csrftoken}}
        );

        fetch(request, {method:'POST', body:JSON.stringify({text:text, username:username})})
        .then(response => response.json())
        .then(data => {
            console.log(data)
            document.querySelector('#text').value = ''
            document.location.reload()
        })    
    }

    if (document.querySelector('#back_page') || document.querySelector('#next_page')) {
        document.querySelector('#back_page').onclick = () => {
            let username = document.querySelector('#username').innerHTML.replace(/\s/g, '')
            let page = parseInt(document.querySelector('#paginator').value)
            if (page > 1) {
                window.location = `/user/${username}/following/${page - 1}`
            }
        }

        document.querySelector('#next_page').onclick = () => {
            let username = document.querySelector('#username').innerHTML.replace(/\s/g, '')
            let page = parseInt(document.querySelector('#paginator').value)
            let max_page = parseInt(document.querySelector('#max_page').value)
            if (page < max_page) {
                window.location = `/user/${username}/following/${page + 1}`
            }
        }
    }
})


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


