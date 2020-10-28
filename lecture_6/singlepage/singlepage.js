document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#pages').onchange = () => {
        document.querySelectorAll('div').forEach(element => {
            document.querySelector(`#${element.id}`).style.display = 'none'
        })
        selected = document.querySelector('#pages').value
        document.querySelector(`#${selected}`).style.display = 'block'

    }
})