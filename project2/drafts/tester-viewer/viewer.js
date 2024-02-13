/**
 * @type {String}
 */
const TEST_DATA = `[{"target_color":[255,0,0],"colors":[[255,0,230],[255,0,153],[255,0,76],[255,77,0],[255,153,0],[255,230,0]],"selections":[[255,77,0],[255,153,0]]},{"target_color":[127,96,0],"colors":[[127,0,18],[127,20,0],[127,58,0],[120,127,0],[82,127,0],[44,127,0]],"selections":[[120,127,0],[82,127,0],[44,127,0]]},{"target_color":[56,87,35],"colors":[[87,71,35],[87,87,35],[72,87,35],[40,87,35],[35,87,45],[35,87,61]],"selections":[[87,71,35],[87,87,35],[72,87,35],[40,87,35],[35,87,45],[35,87,61]]},{"target_color":[255,255,0],"colors":[[255,25,0],[255,102,0],[255,179,0],[178,255,0],[102,255,0],[26,255,0]],"selections":[[255,179,0],[178,255,0],[102,255,0],[26,255,0]]},{"target_color":[0,47,142],"colors":[[0,142,109],[0,132,142],[0,90,142],[0,4,142],[38,0,142],[81,0,142]],"selections":[[0,90,142],[0,4,142],[38,0,142],[81,0,142]]},{"target_color":[112,48,160],"colors":[[48,85,160],[48,51,160],[78,48,160],[146,48,160],[160,48,141],[160,48,107]],"selections":[[48,85,160],[48,51,160],[78,48,160],[146,48,160],[160,48,141]]},{"target_color":[155,0,0],"colors":[[155,0,140],[155,0,93],[155,0,46],[155,47,0],[155,93,0],[155,140,0]],"selections":[[155,0,46],[155,47,0],[155,93,0]]},{"target_color":[125,69,0],"colors":[[125,0,43],[125,0,6],[125,31,0],[125,106,0],[106,125,0],[69,125,0]],"selections":[[125,0,43],[125,0,6],[125,31,0],[125,106,0],[106,125,0],[69,125,0]]},{"target_color":[0,158,115],"colors":[[27,158,0],[0,158,20],[0,158,68],[0,154,158],[0,106,158],[0,59,158]],"selections":[[0,158,68]]},{"target_color":[255,255,0],"colors":[[255,25,0],[255,102,0],[255,179,0],[178,255,0],[102,255,0],[26,255,0]],"selections":[[178,255,0],[102,255,0],[26,255,0]]},{"target_color":[0,114,178],"colors":[[0,178,82],[0,178,135],[0,167,178],[0,61,178],[0,7,178],[46,0,178]],"selections":[[0,167,178]]},{"target_color":[204,121,167],"colors":[[166,121,204],[191,121,204],[204,121,192],[204,121,142],[204,125,121],[204,150,121]],"selections":[[166,121,204],[191,121,204],[204,121,192],[204,121,142]]},{"target_color":[255,0,0],"colors":[[255,0,230],[255,0,153],[255,0,76],[255,77,0],[255,153,0],[255,230,0]],"selections":[[255,77,0]]},{"target_color":[127,96,0],"colors":[[127,0,18],[127,20,0],[127,58,0],[120,127,0],[82,127,0],[44,127,0]],"selections":[[120,127,0],[82,127,0],[44,127,0]]},{"target_color":[56,87,35],"colors":[[87,71,35],[87,87,35],[72,87,35],[40,87,35],[35,87,45],[35,87,61]],"selections":[[87,71,35],[87,87,35],[72,87,35],[40,87,35],[35,87,45],[35,87,61]]},{"target_color":[255,255,0],"colors":[[255,25,0],[255,102,0],[255,179,0],[178,255,0],[102,255,0],[26,255,0]],"selections":[[178,255,0],[102,255,0],[26,255,0]]},{"target_color":[0,47,142],"colors":[[0,142,109],[0,132,142],[0,90,142],[0,4,142],[38,0,142],[81,0,142]],"selections":[[0,4,142],[38,0,142],[81,0,142]]},{"target_color":[112,48,160],"colors":[[48,85,160],[48,51,160],[78,48,160],[146,48,160],[160,48,141],[160,48,107]],"selections":[[48,85,160],[48,51,160],[78,48,160],[146,48,160],[160,48,141]]},{"target_color":[155,0,0],"colors":[[155,0,140],[155,0,93],[155,0,46],[155,47,0],[155,93,0],[155,140,0]],"selections":[[155,0,46],[155,47,0],[155,93,0]]},{"target_color":[125,69,0],"colors":[[125,0,43],[125,0,6],[125,31,0],[125,106,0],[106,125,0],[69,125,0]],"selections":[[125,106,0],[106,125,0],[69,125,0]]},{"target_color":[0,158,115],"colors":[[27,158,0],[0,158,20],[0,158,68],[0,154,158],[0,106,158],[0,59,158]],"selections":[[0,158,68]]},{"target_color":[255,255,0],"colors":[[255,25,0],[255,102,0],[255,179,0],[178,255,0],[102,255,0],[26,255,0]],"selections":[[178,255,0],[102,255,0],[26,255,0]]},{"target_color":[0,114,178],"colors":[[0,178,82],[0,178,135],[0,167,178],[0,61,178],[0,7,178],[46,0,178]],"selections":[[0,167,178]]},{"target_color":[204,121,167],"colors":[[166,121,204],[191,121,204],[204,121,192],[204,121,142],[204,125,121],[204,150,121]],"selections":[[204,121,142]]},{"target_color":[255,0,0],"colors":[[255,0,230],[255,0,153],[255,0,76],[255,77,0],[255,153,0],[255,230,0]],"selections":[[255,77,0]]}]`

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
    //CURRENT_COLOR = 0;
    //setColorRange(TEST_COLORS[CURRENT_COLOR], TEST_HUE_SHIFT);
    td = JSON.parse(TEST_DATA);
    elements_html = ""
    console.log(td);
    trial_id = 0
    for(i in td) {
        for(j = 0; j < 6; j++) {
            elements_html += `<div class="color_box" id="CB_${trial_id}_" onclick="handleClick(0)"></div> `;
        }
        elements_html += `<br><br>`
        trial_id++;
    }
    document.getElementById("COLOR_BOXES").innerHTML = elements_html;
    for(i in td) {
        
    }
}

/* ===== On page load ===== */

main();