document.addEventListener('DOMContentLoaded', () => {
    const logo = document.getElementById('logo') ;
    let ClickCount = 0 ;
    logo.addEventListener('click', (event) => {
        event.preventDefault() ;
        ClickCount ++ ;
        if (ClickCount === 5){
            const image = document.createElement('img') ;
            const image2 = document.createElement('img') ;
            image2.src = '/static/ThisBetter.png' ;
            image.src = '/static/bu_ispugalsa.png' ;
            image.style.top = '50%' ;
            image2.style.top = '4.4%' ;
            image.style.left = '50%' ;
            image2.style.left = '71.63%' ;
            image.style.position = 'fixed' ;
            image2.style.position = 'fixed' ;
            image.style.zIndex = '1000' ;
            image2.style.zIndex = '1000' ;
            image.style.transform = 'translate(-50%, -50%)'
            image.style.width = '500px'
            image.style.height = '500px'
            image2.style.width = '100px'
            image2.style.height = '50px'
            document.body.appendChild(image) ;
            document.body.appendChild(image2) ;
            setTimeout(() => {
                document.body.removeChild(image) ;
                document.body.removeChild(image2) ;
                ClickCount = 0 ;
            }, 2999) ;
        }
    }) ;
}) ;