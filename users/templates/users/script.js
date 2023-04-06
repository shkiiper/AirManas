let dropIcon = document.querySelector('.header_profile__img');
let dropDown = document.querySelector('.dropdown');
console.log(dropDown)
dropIcon.addEventListener('click', function(e){
    dropDown.classList.toggle('active')
})

let select = document.querySelector('.select');
let sort = document.querySelector('.sort');

select.addEventListener('click', function(){
    sort.classList.toggle('sort_active')
})
