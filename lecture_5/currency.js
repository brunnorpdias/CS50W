document.addEventListener('DOMContentLoaded', () => {
    fetch('https://api.exchangeratesapi.io/latest?base=USD')
    .then(response => response.json())
    .then(data => {
        Object.keys(data.rates).forEach( (currency) => {
            const options = document.createElement('option')
            options.innerHTML = currency
            document.querySelector('#currency').append(options)
        })

        document.querySelector('#submit').onclick = () => {
            document.querySelector('#result').innerHTML = ''
            const currency = document.querySelector('#currency').value
            text = document.createElement('span')
    
            const exchange = data.rates[currency]
            
            text.innerHTML = `The exchange currency between USD and ${currency} is ${exchange.toFixed(3)}`
            document.querySelector('#result').append(text)
            return false
        }
    })  
});