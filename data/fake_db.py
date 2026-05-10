# In-memory database (replaces a real DB for now)
users_db = [
    {
        "id": 1,
        "name": "Rafik",
        "email": "mdrafik.naregal@gmail.com",
        "age": 28,
        "password": "Rafik@123",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane@example.com",
        "age": 32,
        "password": "jane123",
    },
    {
        "id": 3,
        "name": "Bob Johnson",
        "email": "bob@example.com",
        "age": 25,
        "password": "bob123",
    },
]

# Auto-increment counter (like a DB sequence)
next_id = [4]  # wrapped in list so controllers can mutate it
