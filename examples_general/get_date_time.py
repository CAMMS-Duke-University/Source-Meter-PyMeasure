from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)

print("-------",type(dt_string))

dt_string_with_head = "HEAD"+dt_string
print("Merged with text:", dt_string_with_head)