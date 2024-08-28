const canvas = document.getElementById("pong");
const ctx = canvas.getContext("2d");

const windowWidth = JSON.parse(document.getElementById('window-width').textContent);
const windowHeight = JSON.parse(document.getElementById('window-height').textContent);
const ballDiameter = JSON.parse(document.getElementById('ball-diameter').textContent);
const batHeight = JSON.parse(document.getElementById('bat-height').textContent);
const batWidth = JSON.parse(document.getElementById('bat-width').textContent);
const gameId = JSON.parse(document.getElementById('game-id').textContent);
const playerPos = JSON.parse(document.getElementById('player-pos').textContent);
const batSpeed = JSON.parse(document.getElementById('bat-speed').textContent);
const startPosY = JSON.parse(document.getElementById('start-pos-y').textContent);
const player1_X = JSON.parse(document.getElementById('player1-x').textContent);
const player2_X = JSON.parse(document.getElementById('player2-x').textContent);
const playerName = JSON.parse(document.getElementById('player_name').textContent);


let initialized = false
let msg = 'Waiting for oponent...'
let start = false
let ball = {
    x: 0,
    y: 0,
    radius: 0,
    velocityX: 0,
    velocityY: 0,
    directionX: 'positive',
    directionY: 'positive',
    color: 'white'
};

let player1 = {
    name: 'default',
    x: 0,
    y: 0,
    width: 0,
    height: 0,
    color: 'white',
    score: 0
};

let player2 = {
    name: 'default',
    x: 0,
    y: 0,
    width: 0,
    height: 0,
    color: 'white',
    score: 0
};

const net = {
	x : windowWidth/2 - 1,
	y : 0,
	width : 2,
	height : 10,
	color : "WHITE",
}

var gameSocket = new WebSocket(
    'wss://' + window.location.host + '/ws/game/' + gameId + '/' + playerPos + '/'
);

gameSocket.onopen = function (e) {
    console.log("WebSocket connection opened.");
};

gameSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log("Received message: ", data);

    if (data.type === 'player_move') {
        const game = data.game;
        if (game.player_pos === 0) {
            player1.y = game.player_y[0];
        } else if (game.player_pos === 1) {
            player2.y = game.player_y[1];
        }
    } else if (data.type == 'game_timer') {
        msg = data.message;
    } else if (data.type == 'redirect') {
        if (playerName == data.player_name) {
            window.location.href = data.url;
        }
    }else {
        if (!initialized) {
            msg = data.msg;

            ball.x = data.ball_x;
            ball.y = data.ball_y;
            ball.radius = ballDiameter / 2;
            ball.velocityX = data.ball_velocity_x;
            ball.velocityY = data.ball_velocity_y;
            ball.directionX = data.ball_direction_x;
            ball.directionY = data.ball_direction_y;

            player1.x = player1_X;
            player1.y = startPosY;
            player1.name = data.player_names[0];
            player1.width = batWidth;
            player1.height = batHeight;

            player2.x = player2_X;
            player2.y = startPosY;
            player2.name = data.player_names[1];
            player2.width = batWidth;
            player2.height = batHeight;

            initialized = true;
        } else {
            msg = data.msg;
            ball.x = data.ball_x;
            ball.y = data.ball_y;
            ball.velocityX = data.ball_velocity_x;
            ball.velocityY = data.ball_velocity_y;
            ball.directionX = data.ball_direction_x;
            ball.directionY = data.ball_direction_y;
            player1.score = data.points[0];
            player2.score = data.points[1];
        } 
    }    
};

function drawRect(x, y, w, h, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, w, h);
}

function drawCircle(x, y, r, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2, false);
    ctx.closePath();
    ctx.fill();
}

function drawNet() {
	for(let i = 0; i <= windowHeight; i += 15) {
		drawRect(net.x, net.y + i, net.width, net.height, net.color)
	}
}		
function drawText(text, x, y, color) {
    ctx.fillStyle = color;
    ctx.font = "20px Arial";
    const textWidth = ctx.measureText(text).width;
    ctx.fillText(text, x - textWidth / 2, y);
}

function render() {
    drawRect(0, 0, windowWidth, windowHeight, "black"),
    drawText(`${player1.name}: ${player1.score}`, windowWidth / 4, windowHeight / 5, "WHITE");
    drawText(`${player2.name}: ${player2.score}`, 3 * windowWidth / 4, windowHeight / 5, "WHITE");
    drawText(msg, windowWidth / 2, windowHeight / 3, "WHITE");
    drawRect(player1.x, player1.y, player1.width, player1.height, player1.color);
    drawRect(player2.x, player2.y, player2.width, player2.height, player2.color);
    drawCircle(ball.x, ball.y, ball.radius, ball.color);
    drawNet();
}

function gameLoop() {
    render();
    requestAnimationFrame(gameLoop)
}

document.addEventListener('keydown', function (event) {
    if (event.key === 'W' || event.key === 'w' || event.key === 'S' || event.key === 's') {
        let direction = (event.key === 'W' || event.key === 'w') ? -1 : 1;
        if (playerPos === 0) {
            player1.y += direction * batSpeed;
            if (player1.y + batHeight > windowHeight) {
                player1.y = windowHeight - batHeight;
            }
            else if (player1.y < 0) {
                player1.y = 0;
            }
            gameSocket.send(JSON.stringify({
                'game': {
                    'game_id': gameId,
                    'player_pos': playerPos,
                    'player_y': [player1.y, player2.y]
                }
            }));
        } else if (playerPos === 1) {
            player2.y += direction * batSpeed;
            if (player2.y + batHeight > windowHeight) {
                player2.y = windowHeight - batHeight;
            }
            else if (player2.y < 0) {
                player2.y = 0;
            }
            gameSocket.send(JSON.stringify({
                'game': {
                    'game_id': gameId,
                    'player_pos': playerPos,
                    'player_y': [player1.y, player2.y]
                }
            }));
        }
    }
});

gameLoop();
//setInterval(gameLoop, 1000 / 40);