const playerName = JSON.parse(
	document.getElementById('player_name').textContent
);
const tournament_history = JSON.parse(
	document.getElementById('tournament_history').textContent
);
console.log('tournament_history:', tournament_history);
const gameHistory = document.getElementById('game-history');

tournament_history.data.forEach((game) => {
	if (
		game[3] === playerName ||
		game[4] === playerName ||
		game[5] === playerName ||
		game[6] === playerName
	) {
		const gameElement = document.createElement('div');
		gameElement.innerHTML = `
        <h3>Date: ${new Date(game[0] * 1000).toLocaleString()}</h3>
        <p>semi-final: ${game[3]} ${game[9]} - ${game[10]} ${game[4]}</p>
        <p>semi-final: ${game[5]} ${game[11]} - ${game[12]} ${game[6]}</p>
        <p>final: ${game[7]} ${game[13]} - ${game[14]} ${game[8]}</p>
      `;
		gameHistory.appendChild(gameElement);
	}
});
