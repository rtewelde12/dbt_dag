# import smtplib


# def test_smtp():
#     smtp_server = 'smtp.office365.com'
#     smtp_port = 587
#     smtp_user = 'robel_tewelde@hotmail.com'
#     smtp_password = 'Lateralus85!'
#     to_email = 'robel_tewelde@hotmail.com'

#     subject = "Test Email"
#     body = "This is a test email."

#     message = f"Subject: {subject}\n\n{body}"

#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(smtp_user, smtp_password)
#         server.sendmail(smtp_user, to_email, message)
#         print("Test email sent successfully")
#     except Exception as e:
#         print(f"Failed to send test email: {e}")
#     finally:
#         server.quit()


# test_smtp()


import smtplib

try:
    # Set up the SMTP server and port (for Office 365 use smtp.office365.com and port 587)
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()  # Upgrade to secure connection
    # Replace with your email and password
    server.login('robel_tewelde@hotmail.com', 'Lateralus85!')
    print('Connection successful')
    server.quit()  # Close the connection
except Exception as e:
    print(f'Failed to connect: {e}')
