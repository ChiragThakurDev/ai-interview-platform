import time 

def send_welcome_email(email:str):
    """
    Simulate sending a welcome email,
    """
    print(f"Sending welcome email to{email}...")

    #Simulate slow work
    time.sleep(5)

    print(f"Welcome email sent to {email}")
