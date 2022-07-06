$(function () {
    // init feather icons
    feather.replace();

    // init tooltip & popovers
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="popover"]').popover();

    //page scroll
    $("a.page-scroll").bind("click", function (event) {
        var $anchor = $(this);
        $("html, body")
            .stop()
            .animate(
                {
                    scrollTop: $($anchor.attr("href")).offset().top - 50,
                },
                1000
            );
        event.preventDefault();
    });

    //toggle scroll menu
    $(window).scroll(function () {
        var scroll = $(window).scrollTop();
        //adjust menu background
        if (scroll >= 100) {
            $(".sticky-navigation").addClass("navbar-shadow");
        } else {
            $(".sticky-navigation").removeClass("navbar-shadow");
        }

        // adjust scroll to top
        if (scroll >= 600) {
            $(".scroll-top").addClass("active");
        } else {
            $(".scroll-top").removeClass("active");
        }
        return false;
    });

    // scroll top top
    $(".scroll-top").click(function () {
        $("html, body").stop().animate(
            {
                scrollTop: 0,
            },
            1000
        );
    });

    /**Theme switcher - DEMO PURPOSE ONLY */
    $(".switcher-trigger").click(function () {
        $(".switcher-wrap").toggleClass("active");
    });
    $(".color-switcher ul li").click(function () {
        var color = $(this).attr("data-color");
        $("#theme-color").attr("href", "css/" + color + ".css");
        $(".color-switcher ul li").removeClass("active");
        $(this).addClass("active");
    });
});

//--------------------------------- Teste ---------------------------------
// Commented HTML:
// <span class="dot"></span>

Number.prototype.map = function (in_min, in_max, out_min, out_max) {
    return (
        ((this - in_min) * (out_max - out_min)) / (in_max - in_min) + out_min
    );
};

const Valor1 = document.getElementById("value1");
const Valor2 = document.getElementById("value2");
const Sweeper1 = document.getElementById("Sweeper1");
const Sweeper2 = document.getElementById("Sweeper2");

(function loop() {
    var value1 = Math.random() * 100;
    var value2 = Math.random() * 100;

    value1 = Math.round(value1.map(0, 100, 50, 130));
    value2 = Math.round(value2.map(0, 100, 50, 130));

    Sweeper1.style.transform = "rotate(" + (90 - value1) + "deg)";
    Sweeper2.style.transform = "rotate(" + value2 + "deg)";

    Valor1.innerText = "θ = " + value1 + "°";
    Valor2.innerText = "φ = " + value2 + "°";

    window.setTimeout(loop, 2000);
})();

function init() {
    // easal stuff goes hur
    var xCenter = 150;
    var yCenter = 150;
    var stage = new createjs.Stage("joystick");

    var psp = new createjs.Shape();
    psp.graphics.beginFill("#333333").drawCircle(xCenter, yCenter, 50);

    psp.alpha = 0.25;

    var vertical = new createjs.Shape();
    var horizontal = new createjs.Shape();
    vertical.graphics.beginFill("#ff4d4d").drawRect(150, 0, 2, 300);
    horizontal.graphics.beginFill("#ff4d4d").drawRect(0, 150, 300, 2);

    stage.addChild(psp);
    stage.addChild(vertical);
    stage.addChild(horizontal);
    createjs.Ticker.framerate = 60;
    createjs.Ticker.addEventListener("tick", stage);
    stage.update();

    var myElement = $("#joystick")[0];

    // create a simple instance
    // by default, it only adds horizontal recognizers
    var mc = new Hammer(myElement);

    mc.on("panstart", function (ev) {
        var pos = $("#joystick").position();
        xCenter = psp.x;
        yCenter = psp.y;
        psp.alpha = 0.5;
        console.log("START", { pos });
        stage.update();
    });

    // listen to events...
    mc.on("panmove", function (ev) {
        var pos = $("#joystick").position();
        var x = ev.center.x - pos.left - 150;
        var y = ev.center.y - pos.top - 150;
        console.log("MOVE", { x, y, pos });
        $("#xVal").text("X: " + x);
        $("#yVal").text("Y: " + -1 * y);

        var coords = calculateCoords(ev.angle, ev.distance);

        psp.x = coords.x;
        psp.y = coords.y;

        psp.alpha = 0.5;

        stage.update();
    });

    mc.on("panend", function (ev) {
        psp.alpha = 0.25;
        var pos = $("#joystick").position();
        console.log("END", { pos });
        createjs.Tween.get(psp).to(
            { x: xCenter, y: yCenter },
            750,
            createjs.Ease.elasticOut
        );
    });
}

function calculateCoords(angle, distance) {
    var coords = {};
    distance = Math.min(distance, 100);
    var rads = (angle * Math.PI) / 180.0;

    coords.x = distance * Math.cos(rads);
    coords.y = distance * Math.sin(rads);

    return coords;
}

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
