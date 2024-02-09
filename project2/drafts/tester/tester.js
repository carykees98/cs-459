/**
 * @type {[[Number]]}
 */
const TEST_COLORS = [
    [255,0,0],
    [127,96,0],
    [56,87,35],
    [255,255,0],
    [0,47,142],
    [112, 48, 160]
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
    colors;
    selections;

    /**
     * @param {[[Number]]} colors 
     * @param {[Number]} selections 
     */
    constructor(colors, selections) {
        this.colors = colors;
        this.selections = selections;
    }
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
    colors = getSwatch(TEST_COLORS[CURRENT_COLOR], TEST_HUE_SHIFT);
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
    if(CURRENT_COLOR >= TEST_COLORS.length) {
        CURRENT_COLOR = 0;
    }
    setColorRange(TEST_COLORS[CURRENT_COLOR], TEST_HUE_SHIFT);
    resetSelected();
}

function handleReset() {
    SAVED_TRIALS.length = 0;
    JSON_DISPLAY.innerHTML = JSON.stringify(SAVED_TRIALS);
}

function main() {
    CURRENT_COLOR = 0;
    setColorRange(TEST_COLORS[CURRENT_COLOR], TEST_HUE_SHIFT);
}

/* ===== On page load ===== */

main();