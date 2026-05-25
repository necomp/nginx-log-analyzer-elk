import time
import random
import os
from datetime import datetime
from faker import Faker

LOG_FILE = "logs/access.log"
fake = Faker()

USER_POOL = [fake.ipv4() for _ in range(300)]

# Saldırgan IP'si
ATTACKER_IP = "192.168.66.66" 

# Endpointler
PAGES = [
    "/index.html", "/contact", "/about", "/products", "/services", 
    "/blog/post-1", "/blog/tech-news", "/assets/style.css", "/assets/main.js", 
    "/images/banner.jpg", "/images/logo.png"
]
LOGIN_PAGE = "/api/login"
ADMIN_PAGE = "/admin/dashboard"

def generate_realistic_log():
    # UTC Saat
    dt = datetime.utcnow().strftime('%d/%b/%Y:%H:%M:%S +0000')
    
    # Zar at: Normal mi Saldırı mı?
    dice = random.randint(1, 100)

    # SENARYO A: NORMAL TRAFİK (%95)
    if dice <= 95:
        # %80 havuzdan, %20 yeni ziyaretçi
        if random.random() < 0.8:
            ip = random.choice(USER_POOL)
        else:
            ip = fake.ipv4()
        
        endpoint = random.choice(PAGES)
        method = random.choice(["GET", "GET", "GET", "POST"]) # Ağırlıklı GET
        
        # Çeşitlendirilmiş Durum Kodları
        codes = [200, 201, 301, 302, 404, 403, 500, 503]
        weights = [85, 2, 3, 2, 5, 2, 2, 1]
        status = random.choices(codes, weights=weights, k=1)[0]
        
        referer = random.choice(["-", "http://google.com", "http://twitter.com", "http://linkedin.com", "http://bing.com"])
        user_agent = fake.user_agent()

    # SENARYO B: SALDIRI (%5 - Brute Force)
    else:
        ip = ATTACKER_IP
        endpoint = LOGIN_PAGE
        method = "POST"
        status = 401 # Unauthorized (Şifre yanlış)
        referer = "-"
        user_agent = "Mozilla/5.0 (Hydra/Tool/v1.0)"
  

    size = random.randint(200, 5000)
    
    return f'{ip} - - [{dt}] "{method} {endpoint} HTTP/1.1" {status} {size} "{referer}" "{user_agent}"\n'

def main():
    sayac=10483
    # Dosya ve klasör kontrolü
    if not os.path.exists("logs"):
        os.makedirs("logs")
    try:
        with open(LOG_FILE, "a") as f:
            while sayac > 0:
                line = generate_realistic_log()
                f.write(line)
                f.flush()
                print(line.strip()) # Terminalde görelim
                time.sleep(random.uniform(0.05, 0.6))
                sayac -= 1
    except KeyboardInterrupt:
        print("İşlem durduruldu.")

if __name__ == "__main__":
    main()
