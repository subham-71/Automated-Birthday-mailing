from datetime import datetime
import pandas
import random
import smtplib
import ssl

MY_EMAIL = "[your email here]"
MY_PASSWORD = "[email password here]"
port = 587
context = ssl.create_default_context()

today = datetime.now()
today_tuple = (today.month, today.day)

# create a birthday.csv file containing birthdays of people format: -name,email,year,month,day
data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.ehlo()  # Can be omitted
        connection.starttls(context=context)
        connection.ehlo()  # Can be omitted
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday!\n\n{contents}"
        )
