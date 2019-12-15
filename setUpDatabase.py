from app import User, db, hashed_password, chk_if_password_right

db.drop_all()
db.create_all()
hasd_pwd = hashed_password('eslam elbadry')
user = User('eslam', hasd_pwd, 'eslam@eslam.com', 1, 10)
db.session.add(user)
db.session.commit()


users = User.query.all()
print(users)