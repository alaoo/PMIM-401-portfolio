const btn = document.getElementById('menu-btn')
const nav = document.getElementById('menu')
const hook = document.getElementById('hook')

btn.addEventListener('click', () => {
    btn.classList.toggle('open')
    nav.classList.toggle('flex')
    nav.classList.toggle('hidden')
    hook.classList.toggle('hidden')
})
