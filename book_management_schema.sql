-- Create the genres table
CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Create the books table with new fields
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year INTEGER,
    isbn VARCHAR(13),
    description TEXT,
    total_copies INTEGER DEFAULT 1,
    available_copies INTEGER DEFAULT 1,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the books_genres junction table
CREATE TABLE books_genres (
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, genre_id)
);

-- Insert some common genres
INSERT INTO genres (name) VALUES 
    ('Fiction'), ('Non-Fiction'), ('Science Fiction'), ('Fantasy'),
    ('Mystery'), ('Biography'), ('History'), ('Romance'), ('Horror'),
    ('Adventure'), ('Science'), ('Technology'), ('Philosophy'), ('Poetry');
