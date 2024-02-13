/**
 * @type {[[Number]]}
 */
const BUS_COLORS = [
    [155,0,0],
    [125,69,0],
    [0,158,115],
    [255,255,0],
    [0,114,178],
    [204, 121, 167]
]

/**
 * @type {[HTMLElement]}
 */
const COLOR_BOXES = [];
COLOR_BOXES.push(document.getElementById("COLOR_BOX_0"));
COLOR_BOXES.push(document.getElementById("COLOR_BOX_1"));
COLOR_BOXES.push(document.getElementById("COLOR_BOX_2"));
COLOR_BOXES.push(document.getElementById("COLOR_BOX_3"));
COLOR_BOXES.push(document.getElementById("COLOR_BOX_4"));
COLOR_BOXES.push(document.getElementById("COLOR_BOX_5"));

/**
 * @type {HTMLElement}
 */
const TARGET_BOX = document.getElementById("TARGET_BOX");

/**
 * @type {HTMLElement}
 */
const JSON_DISPLAY = document.getElementById("JSON_DISPLAY");

/**
 * @type {Number}
 */
var CURRENT_COLOR;

/**
 * @type {[Trial]}
 */
var SAVED_TRIALS = [];

/**
 * @type {Number}
 */
var CLOCK = 0.0;

class Trial {
    /**
     * @type {Number}
     */
    time;

    /**
     * @type {String}
     */
    target_color;

    /**
     * @type {String}
     */
    selected_color;

    /**
     * @param {Number} time
     * @param {String} target_color
     * @param {String} selected_color
     */
    constructor(time, target_color, selected_color) {
        this.time = time;
        this.target_color = target_color;
        this.selected_color = selected_color;
    }
}

function tickClock() { CLOCK += 0.01; }

function rand(max) { return Math.floor(Math.random() * max); }

function bumpTargetBox() {
    TARGET_BOX.animate(
        [
            {transform: "rotate(0deg)"},
            {transform: "rotate(-8deg)"},
            {transform: "rotate(8deg)"},
            {transform: "rotate(0)"}
        ],
        {
            duration: 200,
            iterations: 1
        }
    );
}

/**
 * @param {[[Number]]} colors 
 */
function setColorBoxes(colors) {
    for(var i = 0; i < 6; i++) {
        let color = colors[i];
        COLOR_BOXES[i].style.backgroundColor = 
                `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
    }
}

/**
 * @param {[Number]} color
 */
function setTargetBox(color) {
    TARGET_BOX.style.backgroundColor = 
            `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
}

function handleClick(box_id) {
    target_color = TARGET_BOX.style.backgroundColor;
    selected_color = COLOR_BOXES[box_id].style.backgroundColor;
    console.log(`Time: ${CLOCK}`);
    console.log(`Target color: ${target_color}`)
    console.log(`Selected color: ${selected_color}`);
    SAVED_TRIALS.push(new Trial(CLOCK, target_color, selected_color));
    JSON_DISPLAY.innerHTML = JSON.stringify(SAVED_TRIALS);
    setTargetBox(BUS_COLORS[rand(6)]);
    bumpTargetBox();
    CLOCK = 0.0;
}

function handleNext() {
    // save data from this trial
    colors = getSwatch(BUS_COLORS[CURRENT_COLOR], TEST_HUE_SHIFT);
    selections = [];
    for(var i = 0; i < 6; i++) {
        if(COLOR_BOXES[i].classList.contains("box_selected")) {
            selections.push(colors[i]);
        }
    }
    SAVED_TRIALS.push(new Trial(colors, selections));
    JSON_DISPLAY.innerHTML = JSON.stringify(SAVED_TRIALS);

    // advance to next trial
    CURRENT_COLOR++;
    if(CURRENT_COLOR >= BUS_COLORS.length) {
        CURRENT_COLOR = 0;
    }
    setColorRange(BUS_COLORS[CURRENT_COLOR], TEST_HUE_SHIFT);
    resetSelected();
}

function handleReset() {
    if(window.confirm("THIS WILL RESET ALL COLLECTED DATA! Continue?")) {
        SAVED_TRIALS.length = 0;
        JSON_DISPLAY.innerHTML = JSON.stringify(SAVED_TRIALS);
    }
}

function main() {
    setColorBoxes(BUS_COLORS);
    setInterval(tickClock, 10);
    setTargetBox(BUS_COLORS[rand(6)]);
}

/* ===== On page load ===== */

main();