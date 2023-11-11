from update import send_decrease;

if send_decrease():
    print("Decreased capacity successfully.")
else:
    print("Failed to decrease capacity or capacity is already zero.")
