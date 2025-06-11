import os
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(Fore.MAGENTA + Style.BRIGHT + r"""

      Hack With Rohith (. .)
                         -

                  - Subscribe to my Youtube Channel

    """)
    print(Fore.CYAN + Style.BRIGHT + "[ HackRecon v1.0 ] - Automated Bug Bounty Recon Tool")
    print(Fore.YELLOW + "Author: Hack With Rohit")
    print(Fore.GREEN + "🔗 YouTube  : https://www.youtube.com/@hackwithrohit-new-2k")
    print(Fore.GREEN + "🔗 LinkedIn : https://www.linkedin.com/in/rohith-s-0b9b2b267/")
    print(Fore.GREEN + "🔗 Telegram : https://t.me/hackwithrohit\n")

def run_command(command, message):
    print(Fore.CYAN + f"\n[+] {message}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(Fore.RED + f"[!] Error running: {command}")

def main():
    banner()
    domain = input(Fore.LIGHTYELLOW_EX + "Enter the target domain (e.g., vulnweb.com): ").strip()
    base_dir = input(Fore.LIGHTYELLOW_EX + "Enter base output directory (e.g., /home/kali/bounty): ").strip()
    nuclei_templates = input(Fore.LIGHTYELLOW_EX + "Enter path to nuclei templates (e.g., /home/kali/tools/nuclei-templates-10.2.2): ").strip()

    full_dir = os.path.join(base_dir, domain)
    os.makedirs(full_dir, exist_ok=True)
    os.chdir(full_dir)

    # Step 1: Subfinder
    finder_txt = os.path.join(full_dir, "finder.txt")
    run_command(f"subfinder -d {domain} -all -recursive -o {finder_txt}", "Running Subfinder...")

    # Step 2: Httpx
    livehosts_txt = os.path.join(full_dir, "livehosts.txt")
    run_command(f"httpx -l {finder_txt} -o {livehosts_txt}", "Running Httpx...")

    # Step 3: Waybackurls
    wayback_txt = os.path.join(full_dir, "wayback.txt")
    run_command(f"cat {livehosts_txt} | waybackurls > {wayback_txt}", "Extracting URLs from Wayback...")

    # Step 4: Paramspider
    run_command(f"paramspider -l {livehosts_txt}", "Running Paramspider...")

    # Step 5: Nuclei on testphp file
    paramspider_results_dir = os.path.join(full_dir, "results")
    testphp_file = os.path.join(paramspider_results_dir, f"testphp.{domain}.txt")
    if os.path.exists(testphp_file):
        run_command(f"nuclei -l {testphp_file} -t {nuclei_templates} -dast", "Running Nuclei (DAST)...")
    else:
        print(Fore.LIGHTRED_EX + f"[!] File not found: {testphp_file}. Skipping nuclei step.")

    print(Fore.LIGHTGREEN_EX + "\n[✔] Recon automation completed. Good luck hunting!")

if __name__ == "__main__":
    main()
