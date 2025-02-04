// Check login status when page loads
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token) {
        showMainSection();
        getGames();
        getCustomers(); // Load customers when the page loads
    }
});

// Login function
async function login() {
    const phone_num = document.getElementById('phone').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
            phone_num: phone_num,
            password: password
        });

        if (response.data.token) {
            localStorage.setItem('token', response.data.token);
            showMainSection();
            getGames();
        }
    } catch (error) {
        console.error('Login failed:', error);
        alert('Login failed. Please check your credentials.');
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
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
    document.getElementById('phone').value = '';
    document.getElementById('password').value = '';
}

async function addCustomer() {
    const name = document.getElementById('customer-name').value.trim();
    const phone_number = document.getElementById('customer-phone').value.trim();
    const email = document.getElementById('customer-email').value.trim();

    if (!name || !phone_number || !email) {
        alert('Please fill in all fields before adding a customer.');
        return;
    }

    try {
        const response = await axios.post('http://127.0.0.1:5000/customers', {
            name: name,
            phone_number: phone_number,
            email: email
        });

        alert(response.data.message);
        getCustomers(); // Refresh customer list

        // Clear input fields
        document.getElementById('customer-name').value = '';
        document.getElementById('customer-phone').value = '';
        document.getElementById('customer-email').value = '';
    } catch (error) {
        console.error('Error adding customer:', error);
        alert(error.response?.data?.error || 'Failed to add customer');
    }
}

// Function to fetch and display all customers
async function getCustomers() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/customers');

        const customersList = document.getElementById('customers-list');
        customersList.innerHTML = '';

        response.data.customers.forEach(customer => {
            customersList.innerHTML += `
                <div class="customer-card">
                    <h3>${customer.name}</h3>
                    <p>Phone: ${customer.phone}</p>
                    <p>Email: ${customer.email}</p>
                    <button onclick="deleteCustomer(${customer.id})">Delete</button>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching customers:', error);
        alert('Failed to load customers');
    }
}

// Function to delete a customer
async function deleteCustomer(customerId) {
    if (!confirm('Are you sure you want to delete this customer?')) {
        return;
    }

    try {
        await axios.delete(`http://127.0.0.1:5000/customers/${customerId}`);
        alert('Customer deleted successfully!');
        getCustomers(); // Refresh the customer list
    } catch (error) {
        console.error('Error deleting customer:', error);
        alert('Failed to delete customer');
    }
}

// Existing getGames function with modifications
async function getGames() {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/games', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Clear existing list

        response.data.games.forEach(game => {
            let loanButtonText = game.is_loaned ? "Loaned" : "Loan";
            let loanButtonDisabled = game.is_loaned ? "disabled" : "";

            // New loan details rendering
            let loanDetailsHTML = game.is_loaned && game.loan_details ? `
                <div class="loan-details">
                    <p>Loaned to: ${game.loan_details.customer_name}</p>
                    <p>Phone: ${game.loan_details.customer_phone}</p>
                    <p>Return Date: ${game.loan_details.return_date}</p>
                    <button onclick="returnGame(${game.id})">Return Game</button>
                </div>
            ` : '';

            gamesList.innerHTML += `
                <div class="game-card" id="game-${game.id}">
                    <h3>${game.name}</h3>
                    <p>Price: $${game.price}</p>
                    <p>Quantity: ${game.quantity}</p>
                    <button id="loan-btn-${game.id}" ${loanButtonDisabled} onclick="toggleLoanForm(${game.id})">${loanButtonText}</button>
                    <button onclick="deleteGame(${game.id})">Delete</button>
                    <div id="loan-form-${game.id}" class="loan-form hidden"></div>
                    ${loanDetailsHTML}
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}

// New function to return a game
async function returnGame(gameId) {
    try {
        const response = await axios.delete(`http://127.0.0.1:5000/return_game/${gameId}`);
        alert(response.data.message);
        getGames(); // Refresh games list
    } catch (error) {
        console.error('Error returning game:', error);
        alert(error.response?.data?.error || 'Failed to return game');
    }
}


async function toggleLoanForm(gameId) {
    const loanFormContainer = document.getElementById(`loan-form-${gameId}`);
    const loanButton = document.getElementById(`loan-btn-${gameId}`);

    // Toggle logic: if form is visible, hide it; otherwise, show it
    if (!loanFormContainer.classList.contains("hidden")) {
        loanFormContainer.innerHTML = ""; // Clear form
        loanFormContainer.classList.add("hidden");
        loanButton.textContent = "Loan"; // Switch back to "Loan"
        return;
    }

    const customers = await fetchCustomers();

    let customerOptions = customers.map(
        customer => `<option value="${customer.id}">${customer.name} (${customer.phone_number})</option>`
    ).join("");

    loanFormContainer.innerHTML = `
        <label for="customer-${gameId}">Select Customer:</label>
        <select id="customer-${gameId}">
            <option value="">-- Choose Customer --</option>
            ${customerOptions}
        </select>
        <label for="return-date-${gameId}">Return Date:</label>
        <input type="date" id="return-date-${gameId}" />
        <button onclick="confirmLoan(${gameId})">Confirm Loan</button>
    `;
    loanFormContainer.classList.remove("hidden");
    loanButton.textContent = "Cancel"; // Switch to "Cancel"
}



function closeLoanModal() {
    document.getElementById("loan-modal").style.display = "none";
}

async function loadCustomers() {
    try {
        const response = await axios.get("http://127.0.0.1:5000/customers");
        const customerList = document.getElementById("customer-list");
        customerList.innerHTML = "";

        response.data.customers.forEach(customer => {
            const div = document.createElement("div");
            div.classList.add("customer-item");
            div.textContent = `${customer.name} (${customer.phone})`;
            div.onclick = () => selectCustomer(customer.id);
            customerList.appendChild(div);
        });
    } catch (error) {
        console.error("Error fetching customers:", error);
        alert("Failed to load customers");
    }
}

let selectedCustomerId = null;

function selectCustomer(customerId) {
    selectedCustomerId = customerId;
    document.querySelectorAll(".customer-item").forEach(item => item.classList.remove("selected"));
    event.target.classList.add("selected");
}

async function confirmLoan(gameId) {
    const customerId = document.getElementById(`customer-${gameId}`).value;
    const returnDate = document.getElementById(`return-date-${gameId}`).value;

    if (!customerId || !returnDate) {
        alert("Please select a customer and return date.");
        return;
    }

    try {
        const response = await axios.post("http://127.0.0.1:5000/loan", {
            customer_id: customerId,
            game_id: gameId,
            return_date: returnDate
        });

        alert(response.data.message);
        getGames(); // Refresh games list
    } catch (error) {
        console.error("Error loaning game:", error);
        alert("Failed to loan game.");
    }
}

// Fetch customers from backend
async function fetchCustomers() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/customers/search');
        return response.data.customers;
    } catch (error) {
        console.error('Error fetching customers:', error);
        return [];
    }
}



// Function to add a new game to the database
async function addGame() {
    const name = document.getElementById('game-name').value.trim();
    const price = document.getElementById('game-price').value.trim();
    const quantity = document.getElementById('game-quantity').value.trim();

    // Validate that all fields are filled
    if (!name || !price || !quantity) {
        alert('Please fill in all fields before adding a game.');
        return;
    }

    try {
        const token = localStorage.getItem('token');
        await axios.post('http://127.0.0.1:5000/games',
            {
                name: name,
                price: parseFloat(price), // Ensure price is a valid number
                quantity: parseInt(quantity) // Ensure quantity is a valid integer
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

// Function to delete a game by ID
async function deleteGame(gameId) {
    if (!confirm('Are you sure you want to delete this game?')) {
        return;
    }

    try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://127.0.0.1:5000/games/${gameId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        alert('Game deleted successfully!');
        getGames(); // Refresh the games list
    } catch (error) {
        console.error('Error deleting game:', error);
        alert('Failed to delete game');
    }
}

