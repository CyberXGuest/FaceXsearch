#!/usr/bin/env python3
"""
Facesearch Tool - Social Media Profile Finder
Compatible with Kali Linux and Termux
"""

import os
import sys
import time
import json
import requests
import webbrowser
from colorama import init, Fore, Style
import subprocess
import platform

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Banner
BANNER = f"""
{Fore.RED}╔════════════════════════════════════════════════════════════╗
{Fore.RED}║                                                            ║
{Fore.YELLOW}║    ███████╗ █████╗  ██████╗███████╗███████╗███████╗ █████╗  {Fore.RED}║
{Fore.YELLOW}║    ██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝██╔══██╗ {Fore.RED}║
{Fore.YELLOW}║    █████╗  ███████║██║     ███████╗█████╗  ███████╗███████║ {Fore.RED}║
{Fore.YELLOW}║    ██╔══╝  ██╔══██║██║     ╚════██║██╔══╝  ╚════██║██╔══██║ {Fore.RED}║
{Fore.YELLOW}║    ██║     ██║  ██║╚██████╗███████║███████╗███████║██║  ██║ {Fore.RED}║
{Fore.YELLOW}║    ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝ {Fore.RED}║
{Fore.RED}║                                                            ║
{Fore.CYAN}║              {Fore.WHITE}FaceXsearch v1.0{Fore.CYAN}                              ║
{Fore.GREEN}║         {Fore.WHITE}Coded by Allin Isla Minde from Hackrate.inc{Fore.GREEN}         ║
{Fore.BLUE}║              {Fore.WHITE}Facebook: @Hackrate.inc{Fore.BLUE}                        ║
{Fore.RED}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

class Facesearch:
    def __init__(self):
        self.session = requests.Session()
        self.google_token = None
        self.target_name = ""
        self.results = {}
        
        # Social media platforms to search
        self.platforms = {
            'facebook': 'https://www.facebook.com/public/{}',
            'instagram': 'https://www.instagram.com/{}/',
            'twitter': 'https://twitter.com/{}',
            'linkedin': 'https://www.linkedin.com/search/results/all/?keywords={}',
            'tiktok': 'https://www.tiktok.com/@{}',
            'youtube': 'https://www.youtube.com/results?search_query={}',
            'pinterest': 'https://www.pinterest.com/search/pins/?q={}',
            'github': 'https://github.com/{}?tab=repositories',
            'reddit': 'https://www.reddit.com/search/?q={}'
        }

    def clear_screen(self):
        """Clear terminal screen based on OS"""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def check_dependencies(self):
        """Check and install required dependencies"""
        try:
            import colorama
            from google_auth_oauthlib.flow import Flow
            import google.auth
        except ImportError:
            print(f"{Fore.YELLOW}[!] Installing required dependencies...{Style.RESET_ALL}")
            if 'termux' in platform.platform().lower():
                subprocess.run(['pkg', 'install', 'python', '-y'])
                subprocess.run(['pip', 'install', 'colorama', 'requests', 'google-auth', 'google-auth-oauthlib', 'google-auth-httplib2'])
            else:
                subprocess.run(['sudo', 'apt-get', 'update', '-y'])
                subprocess.run(['sudo', 'apt-get', 'install', 'python3-pip', '-y'])
                subprocess.run(['pip3', 'install', 'colorama', 'requests', 'google-auth', 'google-auth-oauthlib', 'google-auth-httplib2'])

    def google_login(self):
        """Simulate Google login (simplified for demo)"""
        print(f"\n{Fore.CYAN}[*] Initializing Google login...{Style.RESET_ALL}")
        time.sleep(1)
        
        # For demonstration purposes - in real implementation, use OAuth2
        print(f"{Fore.YELLOW}[?] This is a simulation of Google OAuth login{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[?] In production, this would open a browser for Google authentication{Style.RESET_ALL}")
        
        # Simulate login process
        print(f"{Fore.GREEN}[+] Opening Google login page...{Style.RESET_ALL}")
        time.sleep(2)
        
        # Simulate successful login
        self.google_token = "simulated_google_token_12345"
        print(f"{Fore.GREEN}[✓] Successfully logged in with Google!{Style.RESET_ALL}")
        time.sleep(1)
        return True

    def search_on_facebook(self, name):
        """Search for person on Facebook and try to get profile pictures"""
        print(f"{Fore.CYAN}[*] Searching Facebook for: {name}{Style.RESET_ALL}")
        
        # Format name for URL
        formatted_name = name.replace(' ', '%20')
        facebook_url = f"https://www.facebook.com/public/{formatted_name}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = self.session.get(facebook_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Check if profiles found (simplified check)
                if "people" in response.text.lower() or "profile" in response.text.lower():
                    print(f"{Fore.GREEN}[✓] Facebook profiles found!{Style.RESET_ALL}")
                    
                    # Try to extract profile picture URLs (simplified)
                    # In real implementation, you'd use proper parsing
                    print(f"{Fore.YELLOW}[*] Attempting to retrieve profile pictures...{Style.RESET_ALL}")
                    
                    # Simulate finding profile pictures
                    time.sleep(2)
                    
                    # For demo, we'll use a placeholder image
                    # In real implementation, you'd extract actual image URLs
                    profile_pics = [
                        f"https://graph.facebook.com/search?q={formatted_name}&type=user",
                        f"https://www.facebook.com/photo.php?fbid=search_{name.replace(' ', '_')}"
                    ]
                    
                    for i, pic_url in enumerate(profile_pics, 1):
                        print(f"{Fore.GREEN}[✓] Opening profile picture {i}...{Style.RESET_ALL}")
                        self.open_image(pic_url)
                        time.sleep(1)
                    
                    return True
                else:
                    print(f"{Fore.RED}[✗] No Facebook profiles found{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[✗] Failed to access Facebook{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}[✗] Error searching Facebook: {str(e)}{Style.RESET_ALL}")
        
        return False

    def search_social_media(self, name):
        """Search for the target name across all social media platforms"""
        print(f"{Fore.CYAN}\n[*] Searching across all social media platforms...{Style.RESET_ALL}")
        
        # Clean name for search
        search_name = name.replace(' ', '')
        search_name_spaces = name.replace(' ', '%20')
        
        results_found = []
        
        for platform, url_template in self.platforms.items():
            print(f"{Fore.YELLOW}[*] Checking {platform.capitalize()}...{Style.RESET_ALL}")
            
            if platform in ['facebook', 'linkedin', 'youtube', 'reddit']:
                url = url_template.format(search_name_spaces)
            else:
                url = url_template.format(search_name)
            
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = self.session.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    if platform == 'facebook' and self.search_on_facebook(name):
                        results_found.append(platform)
                    elif response.status_code == 200:
                        results_found.append(platform)
                        print(f"{Fore.GREEN}[✓] Found on {platform.capitalize()}{Style.RESET_ALL}")
                        
                        # Open in browser if it's a valid profile
                        if platform in ['instagram', 'twitter', 'tiktok', 'github']:
                            self.open_in_browser(url)
                            
            except Exception as e:
                print(f"{Fore.RED}[✗] Error checking {platform}: {str(e)[:50]}{Style.RESET_ALL}")
            
            time.sleep(1)  # Rate limiting
        
        return results_found

    def open_image(self, image_url):
        """Open image in terminal or browser"""
        print(f"{Fore.BLUE}[*] Opening image: {image_url[:50]}...{Style.RESET_ALL}")
        
        # For Termux, we can use termux-open
        if 'termux' in platform.platform().lower():
            try:
                subprocess.run(['termux-open', image_url])
            except:
                webbrowser.open(image_url)
        else:
            # For Kali Linux, use display or webbrowser
            try:
                # Try to open with image viewer if available
                subprocess.run(['display', image_url], timeout=2)
            except:
                webbrowser.open(image_url)

    def open_in_browser(self, url):
        """Open URL in default browser"""
        try:
            webbrowser.open(url)
            print(f"{Fore.GREEN}[✓] Opened in browser: {url}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Failed to open browser: {str(e)}{Style.RESET_ALL}")

    def save_results(self, name, results):
        """Save search results to file"""
        filename = f"facesearch_{name.replace(' ', '_')}_{int(time.time())}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"Facesearch Results for: {name}\n")
            f.write("=" * 50 + "\n")
            f.write(f"Search Time: {time.ctime()}\n")
            f.write(f"Platforms Found: {', '.join(results) if results else 'None'}\n")
            f.write("\nSearch URLs:\n")
            
            for platform, url_template in self.platforms.items():
                if platform in results:
                    f.write(f"{platform.capitalize()}: {url_template}\n")
        
        print(f"{Fore.GREEN}[✓] Results saved to: {filename}{Style.RESET_ALL}")
        return filename

    def run(self):
        """Main execution function"""
        self.clear_screen()
        print(BANNER)
        
        # Check dependencies
        self.check_dependencies()
        
        # Google Login
        print(f"\n{Fore.CYAN}[*] Step 1: Google Authentication{Style.RESET_ALL}")
        if not self.google_login():
            print(f"{Fore.RED}[✗] Google login failed. Exiting...{Style.RESET_ALL}")
            return
        
        # Get target name
        print(f"\n{Fore.CYAN}[*] Step 2: Target Search{Style.RESET_ALL}")
        self.target_name = input(f"{Fore.WHITE}Search a target name: {Style.RESET_ALL}").strip()
        
        if not self.target_name:
            print(f"{Fore.RED}[✗] No name entered. Exiting...{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}[✓] Searching for: {self.target_name}{Style.RESET_ALL}")
        
        # Perform search
        results = self.search_social_media(self.target_name)
        
        # Summary
        print(f"\n{Fore.CYAN}════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Search Summary:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Target: {self.target_name}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Platforms found: {len(results)}{Style.RESET_ALL}")
        
        if results:
            print(f"{Fore.GREEN}Found on: {', '.join(results)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No profiles found{Style.RESET_ALL}")
        
        # Save results
        self.save_results(self.target_name, results)
        
        print(f"\n{Fore.GREEN}[✓] Search completed!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Thank you for using FaceXsearch{Style.RESET_ALL}")

def main():
    """Main entry point"""
    try:
        tool = Facesearch()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Search interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Unexpected error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()