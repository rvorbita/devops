#Check the cpu load of the system
import subprocess
import time
import smtplib
import creds_for_email
email_to_received="Add the email of the receiver here"
email = creds_for_email.EMAIL
password = creds_for_email.PASSWORD


def check_cpu_load():
    """
    Checks the CPU load of the system and send an email if the load is above 80%.

    """
    cpu_load = subprocess.run(["top -bn1 | grep 'Cpu(s):' | awk '{print $2}' | cut -d. -f1"], shell=True, capture_output=True, text=True).stdout
    print(cpu_load)

    #convert the output into a whole number and check if it is greater than 80%
    if int(cpu_load) > 80:
        print("WARNING: CPU load is above 80%")
        #send an email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(user=email, password=password)
            server.sendmail(
                from_addr=email, 
                to_addrs=email_to_received, 
                msg=f"Subject:SYSTEM WARNING: CPU load is above 80%. \n\nSummary of the current system usage:\nCurrent CPU load:{cpu_load}%")
        print("email sent successfully")

    else:
        print("CPU load is below 80%")

if __name__ == "__main__":
    check_cpu_load()
    


