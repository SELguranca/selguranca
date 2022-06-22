const img = document.getElementById("camera");
const fps_display = document.getElementById("fps");
let fps = 0;

img.addEventListener("load", (ev) => {
    fps++;
    console.log(ev) 
});

setInterval(() => {
    fps_display.innerHTML = fps.toString();
    fps = 0;
}, 1000);

// document.getElementById("cmd_form").addEventListener("submit", (ev) => {
// });

async function send(cmd) {
    // console.log("Enviando requisição")
    // let text = document.getElementById("cmd");
    // let cmd = text.value;
    let res = await fetch(`/servo/${cmd}`);
    }


