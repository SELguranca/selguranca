const img = document.getElementById("camera");
const fps_display = document.getElementById("fps");

// FPS Counter
let fps = 0;
img.addEventListener("load", (_) => fps++);

setInterval(() => {
    fps_display.innerHTML = fps.toString();
    fps = 0;
}, 1000);

// Servo Command
const servo = {
    key: "",
    request: async () => {
        const res = await fetch(`/controls/request`);
        const key = await res.text();

        if (key == "-1") {
            console.error("Failed to get servo access");
            return;
        }
        console.log("Aquired Servo Access!!");
        servo.key = key;
        console.log(servo.key);
    },
    release: async () => {
        const res = await fetch(`/controls/release/`, {
            headers: { "Api-Key": servo.key },
        });
        const t = await res.text();
        const ok = Number(t);
        if (ok < 0) {
            console.error("Failed, can't release what wasn't aquired");
            return;
        }
        console.log("Servo Access Released!!");
    },
    send: async (cmd) => {
        const res = await fetch(`/servo/${cmd}`, {
            headers: { "Api-Key": servo.key },
            body: JSON.stringify({ cmd }),
        });
        const content = await res.text();
        console.log(`Servo command: '${cmd}'.\nResponse: `, content);
    },
};

// Stream lifecycle
let stream_id = "";
window.addEventListener("load", async (ev) => {
    const res = await fetch(`/camera_feed/0`);
    const id = await res.text();
    if (id) {
        img.setAttribute("src", `/camera_feed/${id}`);
        stream_id = id;
    }
});

window.addEventListener("beforeunload", async (ev) => {
    await fetch(`/camera_ctrl/${stream_id}/stop`);
});
