def send_verification_email(email, token):
    print(f"Verify: http://localhost:8000/verify?token={token}")

def send_reset_email(email, token):
    print(f"Reset: http://localhost:8000/reset-password?token={token}")