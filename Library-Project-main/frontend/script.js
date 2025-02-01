// Check login status when page loads
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token) {
        showMainSection();
        getGames();
    }
});

// Login function
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

//    try {
//        const response = await axios.post('http://127.0.0.1:5000/login', {
//            username: username,
//            password: password
//        });
//
//        if (response.data.token) {
//    localStorage.setItem('token', response.data.token);
    showMainSection();
    getGames();
//        }
//    } catch (error) {
//        console.error('Login failed:', error);
//        alert('Login failed. Please check your credentials.');
//    }
}

// Logout function
function logout() {
//    localStorage.removeItem('token');
    hideMainSection();
}

// Show main section and hide auth section
function showMainSection() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('main-section').style.display = 'block';
}

// Hide main section and show auth section
function hideMainSection() {
    document.getElementById('auth-section').style.display = 'block';
    document.getElementById('main-section').style.display = 'none';
    // Clear form fields
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
}

// Function to get all games from the API
async function getGames() {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/games', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Clear existing list

        response.data.games.forEach(game => {
            gamesList.innerHTML += `
                <div class="game-card">
                    <h3>${game.name}</h3>
                    <p>Price: $${game.price}</p>
                    <p>Quantity: ${game.quantity}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        if (error.response && error.response.status === 401) {
            // If unauthorized, show login
            hideMainSection();
        } else {
            alert('Failed to load games');
        }
    }
}

// Function to add a new game to the database
async function addGame() {
    const name = document.getElementById('game-name').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    try {
        const token = localStorage.getItem('token');
        await axios.post('http://127.0.0.1:5000/games',
            {
                name: name,
                price: price,
                quantity: quantity
            },
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );

        // Clear form fields
        document.getElementById('game-name').value = '';
        document.getElementById('game-price').value = '';
        document.getElementById('game-quantity').value = '';

        // Refresh the games list
        getGames();
        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        if (error.response && error.response.status === 401) {
            // If unauthorized, show login
            hideMainSection();
        } else {
            alert('Failed to add game');
        }
    }
}