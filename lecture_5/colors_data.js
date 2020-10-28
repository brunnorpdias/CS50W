document.addEventListener('DOMContentLoaded', function() {

    heading = document.querySelector('#main_header');

    document.querySelector('select').onchange = function() {
        document.querySelector('#main_header').style.color = this.value;
    }
});