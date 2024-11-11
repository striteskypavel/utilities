import smtplib

my_email = "striteskypavel@gmail.com"
password = "oqrr iijr bcxz wugb"

# Nastavení připojení k SMTP serveru
connection = smtplib.SMTP("smtp.gmail.com", 587)  # Port 587 pro TLS
connection.starttls()  # Zahájení šifrovaného spojení
connection.login(user=my_email, password=password)

# Formátování emailu
subject = "Informace o projektu"
body = """\
Dobrý den,

dovoluji si Vás informovat o aktuálním stavu našeho projektu. Níže naleznete hlavní body:

- Projekt je v plném proudu a drží se plánovaného harmonogramu.
- Tým usilovně pracuje na dokončení klíčových úkolů.
- Rádi bychom Vás pozvali na příští poradu, kde podrobně probereme další kroky.

Pokud máte jakékoliv dotazy, neváhejte mě kontaktovat.

S pozdravem,

Pavel Striteský
"""

# Složení zprávy s UTF-8 kódováním
msg = f"Subject: {subject}\n\n{body}".encode('utf-8')

# Odeslání emailu
connection.sendmail(from_addr=my_email, to_addrs="pavel.stritesky@unicorn.com", msg=msg)

# Ukončení spojení
connection.close()
