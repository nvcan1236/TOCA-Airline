
const dropdowns = document.querySelectorAll('.dropdown')

dropdowns.forEach((d)=> {
    d.addEventListener('click', (e) => {
        e.stopPropagation()
        e.target.classList.toggle('open')
    })



    let items = d.children[1].children

    for ( let i = 0; i<items.length; i++) {
        items[i].addEventListener('click', ()=> {
            d.querySelector('.dropdown-value').innerText = items[i].innerHTML
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

