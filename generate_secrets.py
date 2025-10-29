#!/usr/bin/env python3
"""
Helper script to generate secrets for deployment
"""
import secrets
import string

def generate_jwt_secret(length=32):
    """Generate a secure JWT secret key"""
    return secrets.token_urlsafe(length)

def generate_password(length=16):
    """Generate a secure password"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in string.punctuation for c in password)):
            return password

if __name__ == "__main__":
    print("=" * 60)
    print("AI Campus Admin - Secret Generator")
    print("=" * 60)
    print()
    
    print("🔐 JWT Secret Key (for JWT_SECRET_KEY):")
    jwt_secret = generate_jwt_secret(32)
    print(f"   {jwt_secret}")
    print()
    
    print("🔑 Strong Password (for database or admin user):")
    password = generate_password(20)
    print(f"   {password}")
    print()
    
    print("💡 Tips:")
    print("   - Copy JWT secret to your Hugging Face Space secrets")
    print("   - Never commit these secrets to Git")
    print("   - Store them securely")
    print("   - Rotate them regularly in production")
    print()
    
    print("📋 Quick Copy Format for HF Spaces:")
    print("-" * 60)
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print(f"# EXAMPLE_PASSWORD={password}")
    print("-" * 60)
    print()
    
    print("✅ Done! Use these secrets in your Hugging Face Space settings.")

