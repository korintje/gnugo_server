// Load HTML elements
const user_input = document.getElementById("user_move");
const message = document.getElementById("message");
const cpu_ouutput = document.getElementById("cpu_move");
const send_button = document.getElementById("send_move");
const board = document.getElementById("board");
const reset_button = document.getElementById("reset");


// Register function for send_button click
send_button.addEventListener("click", () => {

    // User move
    let user_move = user_input.value;
    let usermove_res = get_response(`black ${user_move}`);
    console.log(usermove_res);
    message.value = usermove_res;

    if (usermove_res.startsWith('=')) {
        // CPU move
        let cpumove_res = get_response("genmove_white");
        cpu_ouutput.value = cpumove_res;
    }

    // Goban update
    let current_board = get_response("showboard");
    console.log(current_board);
    board.value = current_board;

});


// Register function for send_button click
reset_button.addEventListener("click", () => {

    // Reset Goban
    let reset_res = get_response("clear_board");
    console.log(reset_res);
    message.value = reset_res;

    // Goban update
    let current_board = get_response("showboard");
    console.log(current_board);
    board.value = current_board;

});


// Function to send GNU Go GTP command to server
// and get response from server
function get_response(command) {

    let request = new XMLHttpRequest();
    request.open('POST', 'http://127.0.0.1:8085', false); 
    request.setRequestHeader('Content-Type', 'application/json');
    request.send(JSON.stringify({"command": command}));

    if (request.status === 200) {
        resData = JSON.parse(request.responseText);
        return resData["output"]
    }

}