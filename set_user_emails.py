import json
from api_client import ApiClient
from logger import setup_logger

logger = setup_logger(__name__)


def get_users_without_email(users: list):
    users_without_email = []
    for user in users:
        if "email" in user.keys():
            if user["email"] is None:
                users_without_email.append(user)
    try:
        with open("users_without_email.json", "w") as f:
            f.write(json.dumps(users_without_email))
    except Exception as e:
        logger.error(e)

    return users_without_email

def generate_email_address(user: dict):
    """
    Generates the email address for a user based on first name, last name and external/internal
    """
    if "is_external" in user.keys():
        if user["is_external"] is True:
            email = f"external_{user['lastname']}.{user['firstname']}@wps-allianz.de"
        else:
            email = f"{user['firstname']}.{user['lastname']}@wps-allianz.de"
        return email
    else:
        raise KeyError("User object missing \"is_external\" attribute.")


def main():

    client = ApiClient()

    all_users = client.get_users()
    users_without_email = get_users_without_email(all_users)
    emails_in_use = [u['email'] for u in all_users if u['email']]

    for user in users_without_email:
        email = generate_email_address(user)
        if email in emails_in_use:
            logger.info(f"User with email {email} already exists.")
            return
        else:
            client.update_user(user_id=user['id'], email=email)

if __name__ == '__main__':
    main()