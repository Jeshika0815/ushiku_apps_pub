//focus.js

const start = document.getElementById('wstart');
console.log(start);
if(start){
    start.addEventListener('click', function () {
        const header = document.querySelector('header');
        const hcontent1 = document.querySelector('.hm');
        const hcontent2 = document.querySelector('.hsu');
        const hcontent3 = document.querySelector('.menus');
        const ribon = document.querySelector('.subhead');
        const footers = document.querySelector('.f_el');

        const end = document.querySelector('.fullsc2');
        const clock = document.querySelector('.fullsc1');
    
        const element = document.documentElement;
        // Start fullscreen
        if (!document.fullscreenElement) {
            if(element.requestFullscreen){
            element.requestFullscreen(document.body).then(() => {
                console.log('Fullscreen started');
                document.body.classList.add('fullscreen');
                hcontent1.style.display = 'none';
                hcontent2.style.display = 'none';
                header.style.display = 'none';
                hcontent3.style.display = 'none';
                footers.style.display = 'none';
                ribon.style.display = 'none';

                if (element.requestFullscreen) {
                    element.requestFullscreen();
                  } else if (element.mozRequestFullScreen) {
                    element.mozRequestFullScreen();
                  } else if (element.webkitRequestFullscreen) {
                    element.webkitRequestFullscreen();
                  } else if (element.msRequestFullscreen) {
                    element.msRequestFullscreen();
                }

                end.style.display = 'block';
                clock.style.display = 'block';
                
            }).catch(err => {
                console.error('Failed to enter fullscreen mode:', err);
            });
        }
    }
    });
}

//clock
function clock(){
    let date = new Date();
    let year = date.getFullYear();
    let mon = date.getMonth()+1;
    let day = date.getDate();
    let sdy = date.getDay();
    let hou = date.getHours();
    let min = date.getMinutes();
    let sec = date.getSeconds();


    if(sdy===1){sdy='月';}if(sdy===2){sdy='火';}if(sdy===3){sdy='水';}if(sdy===4){sdy='木';}if(sdy===5){sdy='金';}if(sdy===6){sdy='土';}if(sdy===0){sdy='日';}
    if(hou<10){hou = "0" + hou;}if(min<10){min = "0" + min;}if(sec<10){sec = "0" + sec;}

    let info_d = year+"年"+mon+"月"+day+"日"+sdy+"曜日"+hou+":"+min+":"+sec;
   
    let clo = document.getElementById('timespace');
    clo.innerHTML=info_d;
}
setInterval('clock()',1000);