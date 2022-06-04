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
