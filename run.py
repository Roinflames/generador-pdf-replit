from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Base de datos creada")
    
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("✅ Base de datos creada")

@app.cli.command("create-user")
def create_user():
    username = input("Usuario: ")
    password = input("Contraseña: ")
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print("✅ Usuario creado")

if __name__ == '__main__':
    app.run(debug=True)
