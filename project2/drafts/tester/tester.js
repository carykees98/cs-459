/**
 * @type {[[Number]]}
 */
const TEST_COLORS = [
    // Original colors
    [255,0,0],      // Red
    [127,96,0],     // Brown
    [56,87,35],     // Green
    [255,255,0],    // Yellow
    [0,47,142],     // Blue
    [112, 48, 160], // Purple
    // New colors (Try 1)
    [155,0,0],
    [125,69,0],
    [0,158,115],
    [255,255,0],
    [0,114,178],
    [204, 121, 167],
    // ...
]

/**
 * @type {Number}
 */
const TEST_HUE_SHIFT = 0.05;


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

class Trial {
    target_color;
    colors;
    selections;

    /**
     * @param {[Number]} target_color
     * @param {[[Number]]} colors 
     * @param {[[Number]]} selections 
     */
    constructor(target_color, colors, selections) {
        this.target_color = target_color;
        this.colors = colors;
        this.selections = selections;
    }
}

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

function setColorRange(color, hue_shift) {
    setColorBoxes(getSwatch(color, hue_shift));
    setTargetBox(color);
}

function getSwatch(color, hue_shift) {
    shifted_colors = []
    for(var i = -3; i <= 3; i++) {
        if(i != 0) {
            shifted_colors.push(shiftHue(color, i * hue_shift));
        }
    }
    return shifted_colors;
}

function handleClick(box_id) {
    if(COLOR_BOXES[box_id].classList.contains("box_selected")) {
        COLOR_BOXES[box_id].classList.remove("box_selected");
    } else {
        COLOR_BOXES[box_id].classList.add("box_selected");
    }
    
}

function resetSelected() {
    for(var i = 0; i < 6; i++) {
        if(COLOR_BOXES[i].classList.contains("box_selected")) {
            COLOR_BOXES[i].classList.remove("box_selected");
        }
    }
}

function handleNext() {
    // save data from this trial
    target_color = TEST_COLORS[CURRENT_COLOR];
    colors = getSwatch(TEST_COLORS[CURRENT_COLOR], TEST_HUE_SHIFT);
    selections = [];
    for(var i = 0; i < 6; i++) {
        if(COLOR_BOXES[i].classList.contains("box_selected")) {
            selections.push(colors[i]);
        }
    }
    SAVED_TRIALS.push(new Trial(target_color, colors, selections));
    JSON_DISPLAY.innerHTML = JSON.stringify(SAVED_TRIALS);

    // advance to next trial
    CURRENT_COLOR++;
    if(CURRENT_COLOR >= TEST_COLORS.length) {
        CURRENT_COLOR = 0;
    }
    setColorRange(TEST_COLORS[CURRENT_COLOR], TEST_HUE_SHIFT);
    bumpTargetBox();
    resetSelected();
}

function handleReset() {
    if(window.confirm("THIS WILL RESET ALL COLLECTED DATA! Continue?")) {
        SAVED_TRIALS.length = 0;
        CURRENT_COLOR = 0;
        setColorRange(TEST_COLORS[CURRENT_COLOR], TEST_HUE_SHIFT);
        bumpTargetBox();
        resetSelected();
        JSON_DISPLAY.innerHTML = JSON.stringify(SAVED_TRIALS);
    }
}

function main() {
    CURRENT_COLOR = 0;
    setColorRange(TEST_COLORS[CURRENT_COLOR], TEST_HUE_SHIFT);
}

/* ===== On page load ===== */

main();