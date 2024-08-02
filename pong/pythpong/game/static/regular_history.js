document.addEventListener('DOMContentLoaded', function() {
    const playerName = JSON.parse(document.getElementById('player_name').textContent);
    const gameHistoryContainer = document.getElementById('regular-game-history');

    fetch(`/pong/api/games/${playerName}/`)
        .then(response => response.json())
        .then(data => {
            data.forEach(game => {
                const listItem = document.createElement('li');
                
                const date = new Date(game.start_time * 1000);
                const formattedTime = date.toLocaleString();
                
                const formattedGame = `Time: ${formattedTime}, ${game.player_names[0]} ${game.points[0]} - ${game.points[1]} ${game.player_names[1]}`;
                
                listItem.textContent = formattedGame;
                gameHistoryContainer.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching game history:', error));
});
