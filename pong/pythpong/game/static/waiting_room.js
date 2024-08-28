const playerName = JSON.parse(document.getElementById('player_name').textContent);
const playerId = JSON.parse(document.getElementById('player_id').textContent);

console.log(player_name);

let player_names = []

var ws = new WebSocket(
    'wss://' + window.location.host + '/ws/waiting_room/' + playerName + '/' + playerId + '/' 
);

ws.onopen = function (e) {
    console.log("Waiting room WebSocket connection opened.");
};

ws.onmessage = function (event) {
    const data = JSON.parse(event.data)
    console.log("Received message: ", data);
    if (data.players)
        player_names = data.players
    if (data.type == 'redirect') {
        if (playerName == data.player_name) {
            window.location.href = data.url;
        }
    }
};

function getPlayerList() {
    let ul = document.getElementById("players-list");
    ul.innerHTML = "";
    player_names.forEach(function(player) {
        let li = document.createElement("li");
        li.textContent = player;
        ul.appendChild(li);
    });
}

setInterval(getPlayerList, 1000);

document.addEventListener("DOMContentLoaded", function() {
    getPlayerList();
}); 