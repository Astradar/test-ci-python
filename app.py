print("Hello from CI/CD 🚀")
import os

def run_command():
    cmd = input("Commande : ")
    os.system(cmd)  # Vulnérabilité : injection de commande
