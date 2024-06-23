document.addEventListener('DOMContentLoaded',()=>{
    let profile_pic = document.querySelector('#profile-pic');
    let close_btn = document.querySelector('.close-button');
    let input = document.querySelector('.input-container');
    let file = document.querySelector('#file');
    let apply_btn = document.querySelector('.apply');
    let username = document.querySelector('.username');
    let phone_num = document.querySelector('.phone_num');
    profile_pic.addEventListener('click',()=>{
        input.style.display='block';
    })
    close_btn.addEventListener('click',()=>{
        input.style.display='none';
    })
    //enable apply button after choosing pic or changing user informations
    function apply_btn_status_change(){
        apply_btn.style.pointerEvents="auto";
        apply_btn.style.color="#000";
    }
    username.addEventListener('keyup',apply_btn_status_change);
    phone_num.addEventListener('keyup',apply_btn_status_change);
    file.addEventListener('change',(e)=>{
        if (e.target.files[0]){
            input.style.display='none';
            apply_btn.style.pointerEvents="auto";
            apply_btn.style.color="#000";
        }
    })

    apply_btn.addEventListener('mouseenter',()=>{
      
        apply_btn.style.color="#fff";
    })
    apply_btn.addEventListener('mouseleave',()=>{
        apply_btn.style.color="#000";
    })
    
})