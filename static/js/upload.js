$(document).ready(function(){
    $('input[type="file"]').change(function(e){
        var fileName = e.target.files[0].name;
        $('.up-label').text('The file "' + fileName +  '" has been selected.');
    });
});

document.getElementById('upload-bid').addEventListener('click', 
function(){
    document.querySelector('html').style.overflow = 'hidden';
    document.querySelector('.bg-modal').style.display = 'flex';
});

document.querySelector('.close').addEventListener('click',
function(){
    document.querySelector('html').style.overflow = 'scroll';
    document.querySelector('html').style.overflowX = 'hidden';
    document.querySelector('.bg-modal').style.display = 'none';
});
