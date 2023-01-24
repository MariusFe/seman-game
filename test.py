from cryptography.fernet import Fernet

KEY='1C1JAk5Eu4Hfxuj05CkghQK1aXtQiQDLW7f6_03HVak='
titre = "France"

print(Fernet(KEY).encrypt(titre.encode()).decode())

oui = Fernet(KEY).decrypt('gAAAAABj0DjUDXu_1xowICzFqgtOs-KJHkWxGKq1StIuy1WT8uBxzwc-IkKEe9LCzB0Ss_QC5d0PQEBZUsvogLQdDHpQKliWqQ==')

print(oui.decode())