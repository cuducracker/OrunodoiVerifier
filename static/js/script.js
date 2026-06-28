const progress=document.getElementById("progressBar");

const text=document.getElementById("progressText");

let value=0;

document.querySelector(".startBtn").onclick=function(){

value=0;

const timer=setInterval(()=>{

value++;

progress.style.width=value+"%";

text.innerHTML="Verification Running : "+value+"%";

if(value>=100){

clearInterval(timer);

text.innerHTML="Verification Completed";

}

},40);

}