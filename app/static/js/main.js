const dropdowns = document.querySelectorAll('.dropdown')
dropdowns.forEach((d)=> {
    d.addEventListener('click', (e) => {
        e.stopPropagation()
        e.target.classList.toggle('open')

        console.log('sdg')
    })

    let items = d.children[1].children


    for ( let i = 0; i<items.length; i++) {
        items[i].addEventListener('click', ()=> {
            d.querySelector('.dropdown-value').value = items[i].dataset['code']
            d.classList.remove('open')
        })
    }
})

window.addEventListener('click', (e)=> {
    if (e.target.matches('.dropdown') === false) {
        dropdowns.forEach((d) => {
            d.classList.remove('open')
        })
    }
})


function showDetail(flight, ticketClass) {
    var currentURL = window.location.href;

    var updatedURL = window.location.href;

    if (currentURL.includes('flight=')) {
        updatedURL = currentURL.replace(/(\?|&)flight=[^&]*/, '$1flight='+flight);
    } else {
        updatedURL = currentURL + (currentURL.includes('?') ? '&' : '?') + 'flight='+flight;
    }

    if (currentURL.includes('ticket-class=')) {
        updatedURL = updatedURL.replace(/(\?|&)ticket-class=[^&]*/, '$1ticket-class='+ticketClass);
    } else {
        updatedURL = updatedURL + (currentURL.includes('?') ? '&' : '?') + 'ticket-class='+ticketClass;
    }

    window.location.href = updatedURL
}

