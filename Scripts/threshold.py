import subprocess
import smtplib
import creds_for_email

email_to_received="raymart.orbita@gmail.com"
email = creds_for_email.EMAIL
password = creds_for_email.PASSWORD

output = subprocess.check_output(["df", "-h"], text=True)
lines = output.splitlines()

def check_desk_usage(threshold=80):
    """
    Checks disk space usage and sends an alert if usage exceeds the threshold.\
    Args:
        threshold: Percentage threshold for disk space usage (default: 80).
    """
    for line in lines[1:]:
        parts = line.split()
        try:
            if parts[0] == "rootfs" and float(parts[4][:-1]) >= threshold:
                print(f"WARNING: Threshold reached for {parts[0]}%: {parts[4]}%")
                #send an email
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(user=email, password=password)
                    server.sendmail(
                        from_addr=email, 
                        to_addrs=email_to_received, 
                        msg=f"WARNING: Threshold reached for {parts[0]}: {parts[4]} \nSummary of the current system usage:\n{output}")

        except subprocess.SubprocessError as e:
            print(f"Error checking disk usage: {e}")

if __name__ == "__main__":
    check_desk_usage()
    print("Disk usage check completed.")