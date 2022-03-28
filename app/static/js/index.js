link_btn = document.querySelector('#search .more-opt');
link_btn_text = document.querySelector('#search .more-opt p');
hidden = document.querySelector('#search .hidden-search');

link_btn.addEventListener('click', (e) => {
    if (hidden.style.display === 'none'){

        hidden.style.display = 'block'; 
        hidden.style.height = 'auto';
        link_btn.style.marginTop = '20px';
        link_btn_text.textContent = 'Less options'

    } else{
        
        hidden.style.display = 'none'; 
        hidden.style.height = 0;
        link_btn_text.textContent = 'More options'
    }
});