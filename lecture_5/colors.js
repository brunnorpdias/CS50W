document.addEventListener('DOMContentLoaded', function() {

    heading = document.querySelector('#main_header');

    document.querySelector('#red').onclick = function() {
        heading.style.color = 'darkred';
    }
    document.querySelector('#blue').onclick = function() {
        heading.style.color = 'darkblue';
    }
    document.querySelector('#green').onclick = function() {
        heading.style.color = 'darkgreen';
    }

});