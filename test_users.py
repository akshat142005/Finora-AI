from database.users import register_user, login_user


# Test Registration
success, message = register_user(
    "Akshat",
    "akshat@test.com",
    "123456"
)

print(success)
print(message)


# Test Login
success, result = login_user(
    "akshat@test.com",
    "123456"
)

print(success)
print(result)