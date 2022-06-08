const img = document.getElementById("camera");
const fps_display = document.getElementById("fps");
let fps = 0;

img.addEventListener("load", (ev) => {
    fps++;
});

setInterval(() => {
    fps_display.innerHTML = fps.toString();
    fps = 0;
}, 1000);

// document.getElementById("cmd_form").addEventListener("submit", (ev) => {
// });

async function send() {
    // ev.preventDefault();
    let f = document.getElementById("cmd_form");
    f.submit();
}
