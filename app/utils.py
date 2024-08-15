from email_validator import validate_email, EmailNotValidError

def is_valid_email(email):
    try:
        valid = validate_email(email)
        email = valid.email 
        return True
    except EmailNotValidError as e:
        return False