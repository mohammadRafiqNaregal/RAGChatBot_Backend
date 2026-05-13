# In-memory database (replaces a real DB for now)
users_db = [
    {
        "id": 1,
        "username": "Rafik",
        "role": "Admin",
        "email": "mdrafik.naregal@gmail.com",
        "age": 28,
        "password": "Rafik@123",
    },
    {
        "id": 2,
        "username": "Jane Smith",
        "role": "HR User",
        "email": "jane@example.com",
        "age": 32,
        "password": "jane123",
    },
    {
        "id": 3,
        "username": "Bob Johnson",
        "role": "Employee",
        "email": "bob@example.com",
        "age": 25,
        "password": "bob123",
    },
]

# Auto-increment counter (like a DB sequence)
next_id = [4]  # wrapped in list so controllers can mutate it
