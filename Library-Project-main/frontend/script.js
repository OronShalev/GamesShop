// function to get all books from the API
async function getBooks() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/books');
        const booksList = document.getElementById('books-list');
        booksList.innerHTML = ''; // Clear existing list

        response.data.books.forEach(book => {
            booksList.innerHTML += `
                <div class="book-card">
                    <h3>${book.title}</h3>
                    <p>Author: ${book.author}</p>
                    <p>Year: ${book.year_published}</p>
                    <p>Type: ${book.types}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching books:', error);
        alert('Failed to load books');
    }
}

// function to add a new book to the database
async function addBook() {
    const title = document.getElementById('book-title').value;
    const author = document.getElementById('book-author').value;
    const year_published = document.getElementById('book-year-published').value;
    const types = document.getElementById('book-type').value;

    try {
        await axios.post('http://127.0.0.1:5000/books', {
            title: title,
            author: author,
            year_published: year_published,
            types: types
        });
        
        // Clear form fields
        document.getElementById('book-title').value = '';
        document.getElementById('book-author').value = '';
        document.getElementById('book-year-published').value = '';
        document.getElementById('book-type').value = '';

        // Refresh the books list
        getBooks();
        
        alert('Book added successfully!');
    } catch (error) {
        console.error('Error adding book:', error);
        alert('Failed to add book');
    }
}

// Load all books when page loads
document.addEventListener('DOMContentLoaded', getBooks);