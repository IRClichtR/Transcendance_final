/* purpose :
1) get csrf token from cookies
2) get player_id from user/men
3) inject in html */

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

const csrftoken = getCookie('csrftoken');
console.log('CSRF Token:', csrftoken);

fetch('/user/me', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken 
    },
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json(); 
})
.then(data => {
    console.log('data received:', data);  
    
    const playerId = data.id;
    console.log('ID :', playerId);
    document.getElementById('playerIdLocalStart').value = playerId;
    document.getElementById('playerIdNameStart').value = playerId;
    document.getElementById('playerIdTournament').value = playerId;
})
.catch(error => {
    alert('You have to be login to continue.');
	window.location.href = '/login';
    console.error('Error:', error);
});

document.addEventListener('DOMContentLoaded', function() {
    const localForm = document.getElementById('localForm');
    localForm.addEventListener('submit', function(event) {
    });
});