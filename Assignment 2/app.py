import sqlite3

def init_db():
    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()

    # Create the "kind" table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS kind (
        id INTEGER PRIMARY KEY,
        kind_name TEXT NOT NULL
    )
    ''')

    # Create the "pet" table with a foreign key to the "kind" table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pet (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        kind_id INTEGER,
        FOREIGN KEY(kind_id) REFERENCES kind(id)
    )
    ''')

    conn.commit()
    conn.close()

# Call this function to initialize the database tables
init_db()

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is running!"

if __name__ == '__main__':
    app.run(debug=True)

# Initialize the database
def init_db():
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS kind (
        id INTEGER PRIMARY KEY,
        kind_name TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pet (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        kind_id INTEGER,
        FOREIGN KEY(kind_id) REFERENCES kind(id)
    )
    ''')
    conn.commit()
    conn.close()

# Route to display all pets
@app.route('/')
def index():
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT pet.id, pet.name, kind.kind_name
    FROM pet
    JOIN kind ON pet.kind_id = kind.id
    ''')
    pets = cursor.fetchall()
    conn.close()
    return render_template('index.html', pets=pets)

# Route to add a pet
@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        kind_id = request.form['kind_id']
        cursor.execute('INSERT INTO pet (name, kind_id) VALUES (?, ?)', (name, kind_id))
        conn.commit()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM kind')
    kinds = cursor.fetchall()
    conn.close()
    return render_template('add_pet.html', kinds=kinds)

# Route to update a pet
@app.route('/update/<int:pet_id>', methods=['GET', 'POST'])
def update_pet(pet_id):
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        kind_id = request.form['kind_id']
        cursor.execute('UPDATE pet SET name = ?, kind_id = ? WHERE id = ?', (name, kind_id, pet_id))
        conn.commit()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM pet WHERE id = ?', (pet_id,))
    pet = cursor.fetchone()

    cursor.execute('SELECT * FROM kind')
    kinds = cursor.fetchall()
    conn.close()
    return render_template('update_pet.html', pet=pet, kinds=kinds)

# Route to delete a pet
@app.route('/delete/<int:pet_id>')
def delete_pet(pet_id):
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pet WHERE id = ?', (pet_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize the database on app start
    app.run(debug=True)


