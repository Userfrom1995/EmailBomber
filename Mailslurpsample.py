import mailslurp_client
from smtplib import SMTP

# MailSlurp API key
configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = ""  # Replace with your API key

with mailslurp_client.ApiClient(configuration) as api_client:
    inbox_controller = mailslurp_client.InboxControllerApi(api_client)
    
    # Create an SMTP-enabled inbox
    options = mailslurp_client.CreateInboxDto()
    options.name = "My test box"
    options.inbox_type = "SMTP_INBOX"  # Ensure this is an SMTP inbox
    
    inbox = inbox_controller.create_inbox_with_options(options)
    print("Email Address is:", inbox.email_address)
    
    # Get SMTP access details
    smtp_access = inbox_controller.get_imap_smtp_access(inbox_id=inbox.id)
    print("SMTP Access Details:", smtp_access)
    
    # Use SMTP to send an email
    with SMTP(
        host=smtp_access.smtp_server_host,  # Use SMTP-specific host
        port=smtp_access.smtp_server_port   # Use SMTP-specific port
    ) as smtp:
        smtp.starttls()  # Optional, ensures secure communication
        smtp.login(user=smtp_access.smtp_username, password=smtp_access.smtp_password)
        
        msg = "Subject: Test Email\r\n\r\nWE LIVE YOUNG, WE LIVE FREE"
        while(1):
         smtp.sendmail(
            from_addr=inbox.email_address, 
            to_addrs=[inbox.email_address], 
            msg=msg
         )
         print("Email sent successfully.")
    
    
