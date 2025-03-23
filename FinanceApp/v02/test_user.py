from user_manager import create_user, verify_user

def test_user():
    # Create test user
    success = create_user('pavel2', 'password', 'pavel2@example.com', 'Pavel')
    print(f'User created: {success}')
    
    # Verify test user
    success, user_data = verify_user('pavel2', 'password')
    print(f'User verified: {success}')
    if user_data:
        print(f'User data: {user_data}')

if __name__ == '__main__':
    test_user() 