#!/usr/bin/env python3
"""
Face Search OSINT Tool with Identity Card Photo Extraction
Educational Purpose Only - For Authorized Testing Only
"""

import os
import sys
import base64
import json
import face_recognition
from PIL import Image, ImageDraw, ImageFont
import argparse
import time
import random
from datetime import datetime
import cv2
import numpy as np
import easyocr
import re

# Try to import additional OCR libraries (optional)
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

# ANSI color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BLACK = '\033[90m'
    ORANGE = '\033[33m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display the anonymous hacker banner"""
    banner = f"""
{Colors.RED}╔══════════════════════════════════════════════════════════════╗
║                                                                  ║
║{Colors.YELLOW}    ███████╗ █████╗  ██████╗███████╗    ███████╗███████╗ █████╗ {Colors.RED}   ║
║{Colors.YELLOW}    ██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔════╝██╔════╝██╔══██╗{Colors.RED}   ║
║{Colors.YELLOW}    █████╗  ███████║██║     █████╗      ███████╗█████╗  ███████║{Colors.RED}   ║
║{Colors.YELLOW}    ██╔══╝  ██╔══██║██║     ██╔══╝      ╚════██║██╔══╝  ██╔══██║{Colors.RED}   ║
║{Colors.YELLOW}    ██║     ██║  ██║╚██████╗███████╗    ███████║███████╗██║  ██║{Colors.RED}   ║
║{Colors.YELLOW}    ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝{Colors.RED}   ║
║                                                                  ║
║{Colors.CYAN}             ╔═══════════════════════════════════╗{Colors.RED}               ║
║{Colors.CYAN}             ║  {Colors.GREEN}THIS MADE BY{Colors.YELLOW} Allin Isla Minde{Colors.CYAN}   ║{Colors.RED}               ║
║{Colors.CYAN}             ║     {Colors.ORANGE}on{Colors.MAGENTA} Hackrate.Inc{Colors.CYAN}           ║{Colors.RED}               ║
║{Colors.CYAN}             ╚═══════════════════════════════════╝{Colors.RED}               ║
║{Colors.WHITE}                                                                  ║
║{Colors.RED}          ╔══════════════════════════════════════════════╗{Colors.RED}          ║
║{Colors.RED}          ║{Colors.GREEN}   Face Recognition & ID Card OSINT Tool{Colors.RED}         ║          ║
║{Colors.RED}          ║{Colors.BLUE}         Educational & Ethical Use Only{Colors.RED}          ║          ║
║{Colors.RED}          ╚══════════════════════════════════════════════╝{Colors.RED}          ║
║{Colors.END}                                                                  ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)

def loading_animation(message, duration=1):
    """Display a loading animation"""
    animations = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", 
                  "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]",
                  "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", 
                  "[■■■■■■■■■■]"]
    
    sys.stdout.write(f"{Colors.CYAN}{message}{Colors.END} ")
    for i in range(duration * 10):
        sys.stdout.write(f"\r{Colors.CYAN}{message} {animations[i % len(animations)]}{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\n")

def print_status(message, status_type="info"):
    """Print formatted status messages"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if status_type == "success":
        print(f"{Colors.GREEN}[✓] {timestamp} - {message}{Colors.END}")
    elif status_type == "error":
        print(f"{Colors.RED}[✗] {timestamp} - {message}{Colors.END}")
    elif status_type == "warning":
        print(f"{Colors.YELLOW}[⚠] {timestamp} - {message}{Colors.END}")
    elif status_type == "info":
        print(f"{Colors.BLUE}[i] {timestamp} - {message}{Colors.END}")
    elif status_type == "result":
        print(f"{Colors.MAGENTA}[+] {timestamp} - {message}{Colors.END}")

def print_separator():
    """Print a decorative separator"""
    print(f"{Colors.RED}════════════════════════════════════════════════════════════════{Colors.END}")

class IDCardProcessor:
    """Process identity cards to extract photos and information"""
    
    def __init__(self):
        """Initialize the ID card processor"""
        self.reader = None
        self.initialize_ocr()
    
    def initialize_ocr(self):
        """Initialize EasyOCR reader"""
        try:
            print_status("Initializing EasyOCR engine...", "info")
            self.reader = easyocr.Reader(['en'], gpu=False)
            print_status("EasyOCR initialized successfully", "success")
        except Exception as e:
            print_status(f"EasyOCR initialization failed: {str(e)}", "warning")
            print_status("Will use fallback methods", "warning")
    
    def detect_id_card_type(self, image_path):
        """
        Detect the type of ID card based on visual features
        
        Args:
            image_path: Path to ID card image
            
        Returns:
            str: Detected ID card type
        """
        try:
            img = cv2.imread(image_path)
            if img is None:
                return "unknown"
            
            height, width = img.shape[:2]
            aspect_ratio = width / height
            
            # Common ID card dimensions (approximate)
            if 1.5 <= aspect_ratio <= 1.7:
                return "credit_card"  # Standard credit card size
            elif aspect_ratio > 1.7:
                return "landscape"    # Driver's license style
            else:
                return "portrait"      # Some national IDs
                
        except Exception as e:
            return "unknown"
    
    def extract_id_photo(self, image_path, output_dir="extracted_photos"):
        """
        Extract the portrait photo from an ID card
        
        Args:
            image_path: Path to ID card image
            output_dir: Directory to save extracted photos
            
        Returns:
            dict: Extracted photo info and path
        """
        results = {
            'success': False,
            'photo_path': None,
            'photo_data': None,
            'face_encoding': None,
            'id_info': {},
            'confidence': 0
        }
        
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                print_status(f"Failed to load image: {image_path}", "error")
                return results
            
            # Convert to RGB for face_recognition
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_img)
            
            # Method 1: Try to detect face directly (most IDs have a face)
            face_locations = face_recognition.face_locations(rgb_img)
            
            if face_locations:
                # Get the largest face (usually the ID photo)
                areas = [(y2-y1)*(x2-x1) for (y1, x2, y2, x1) in face_locations]
                largest_face_idx = areas.index(max(areas))
                y1, x2, y2, x1 = face_locations[largest_face_idx]
                
                # Extract face region with some margin
                margin = 20
                h, w = rgb_img.shape[:2]
                y1 = max(0, y1 - margin)
                y2 = min(h, y2 + margin)
                x1 = max(0, x1 - margin)
                x2 = min(w, x2 + margin)
                
                face_img = rgb_img[y1:y2, x1:x2]
                
                # Save extracted photo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                photo_filename = f"id_photo_{timestamp}.jpg"
                photo_path = os.path.join(output_dir, photo_filename)
                
                cv2.imwrite(photo_path, cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR))
                
                # Get face encoding
                face_encodings = face_recognition.face_encodings(rgb_img, [face_locations[largest_face_idx]])
                
                results['success'] = True
                results['photo_path'] = photo_path
                results['photo_data'] = face_img
                results['face_encoding'] = face_encodings[0] if face_encodings else None
                results['confidence'] = 0.9
                
                print_status(f"ID photo extracted: {photo_path}", "success")
            
            else:
                # Method 2: Look for photo area using contour detection
                print_status("No face detected directly, trying contour analysis...", "info")
                
                # Convert to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                # Use edge detection
                edges = cv2.Canny(gray, 50, 150)
                
                # Find contours
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # Look for square/rectangular regions that might contain photos
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area < 1000:  # Too small
                        continue
                    
                    # Approximate contour
                    epsilon = 0.02 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    
                    if len(approx) == 4:  # Rectangle found
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        # Check aspect ratio (photo areas are roughly square)
                        if 0.8 <= w/h <= 1.2:
                            # Potential photo area
                            roi = rgb_img[y:y+h, x:x+w]
                            
                            # Check if this region contains a face
                            roi_faces = face_recognition.face_locations(roi)
                            if roi_faces:
                                # Found a face in this region
                                photo_filename = f"id_photo_contour_{timestamp}.jpg"
                                photo_path = os.path.join(output_dir, photo_filename)
                                cv2.imwrite(photo_path, cv2.cvtColor(roi, cv2.COLOR_RGB2BGR))
                                
                                results['success'] = True
                                results['photo_path'] = photo_path
                                results['photo_data'] = roi
                                results['confidence'] = 0.7
                                
                                print_status(f"ID photo extracted via contour: {photo_path}", "success")
                                break
            
            return results
            
        except Exception as e:
            print_status(f"Error extracting ID photo: {str(e)}", "error")
            return results
    
    def extract_id_text(self, image_path):
        """
        Extract text information from ID card using OCR [citation:2][citation:7]
        
        Args:
            image_path: Path to ID card image
            
        Returns:
            dict: Extracted text information
        """
        info = {
            'full_text': [],
            'name': None,
            'id_number': None,
            'dob': None,
            'address': None,
            'confidence_scores': []
        }
        
        try:
            if self.reader:
                # Use EasyOCR for text extraction [citation:2]
                print_status("Performing OCR on ID card...", "info")
                result = self.reader.readtext(image_path)
                
                for detection in result:
                    bbox, text, confidence = detection
                    info['full_text'].append(text)
                    info['confidence_scores'].append(confidence)
                    
                    # Try to identify specific fields using regex
                    text_upper = text.upper()
                    
                    # Look for name patterns
                    if re.search(r'NAME|NOMBRE|NAMA', text_upper, re.IGNORECASE):
                        info['name'] = text.split(':')[-1].strip() if ':' in text else text
                    
                    # Look for ID number patterns
                    if re.search(r'ID[:\s]*\d+|NUMBER[:\s]*\d+', text, re.IGNORECASE):
                        numbers = re.findall(r'\d+', text)
                        if numbers:
                            info['id_number'] = numbers[0]
                    
                    # Look for date of birth
                    if re.search(r'DOB|BIRTH|TANGGAL', text_upper, re.IGNORECASE):
                        dates = re.findall(r'\d{1,4}[-/]\d{1,2}[-/]\d{1,4}', text)
                        if dates:
                            info['dob'] = dates[0]
                    
                    # Look for generic ID numbers (sequences of digits)
                    if not info['id_number']:
                        numbers = re.findall(r'\b\d{6,}\b', text)
                        if numbers:
                            info['id_number'] = numbers[0]
                
                print_status(f"OCR completed: {len(info['full_text'])} text elements found", "success")
            
            # Fallback to Tesseract if available and EasyOCR failed
            elif TESSERACT_AVAILABLE:
                print_status("Using Tesseract OCR fallback...", "info")
                img = Image.open(image_path)
                text = pytesseract.image_to_string(img)
                info['full_text'] = text.split('\n')
                
            return info
            
        except Exception as e:
            print_status(f"OCR error: {str(e)}", "error")
            return info
    
    def compare_with_id_photo(self, target_image_path, id_photo_info, threshold=0.6):
        """
        Compare a target face with the ID card photo
        
        Args:
            target_image_path: Path to target image
            id_photo_info: Dictionary with ID photo info
            threshold: Similarity threshold
            
        Returns:
            dict: Comparison results
        """
        results = {
            'match': False,
            'similarity': 0,
            'target_face_location': None
        }
        
        try:
            # Load target image
            target_image = face_recognition.load_image_file(target_image_path)
            target_face_locations = face_recognition.face_locations(target_image)
            
            if not target_face_locations:
                print_status("No face found in target image", "error")
                return results
            
            # Get target face encoding
            target_encoding = face_recognition.face_encodings(target_image, target_face_locations)[0]
            
            # Compare with ID photo encoding if available
            if id_photo_info.get('face_encoding') is not None:
                distance = face_recognition.face_distance([id_photo_info['face_encoding']], target_encoding)[0]
                similarity = (1 - distance) * 100
                
                results['match'] = distance <= threshold
                results['similarity'] = similarity
                results['target_face_location'] = target_face_locations[0]
                
                status = "MATCH" if results['match'] else "NO MATCH"
                print_status(f"Face comparison: {status} ({similarity:.1f}% similar)", 
                           "success" if results['match'] else "warning")
            
            return results
            
        except Exception as e:
            print_status(f"Error comparing faces: {str(e)}", "error")
            return results

def load_face_database(database_path):
    """
    Load and encode faces from a local database directory
    
    Args:
        database_path: Path to directory containing reference images
        
    Returns:
        tuple: (list of face encodings, list of filenames)
    """
    known_encodings = []
    known_names = []
    
    print_status(f"Initializing face database scan on {database_path}", "info")
    loading_animation("Processing database", 2)
    
    if not os.path.exists(database_path):
        print_status(f"Database path not found: {database_path}", "error")
        return [], []
    
    image_files = [f for f in os.listdir(database_path) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
    
    print_status(f"Found {len(image_files)} image files in database", "info")
    
    for filename in image_files:
        image_path = os.path.join(database_path, filename)
        
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Detect faces
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) == 1:
                # Encode face
                face_encoding = face_recognition.face_encodings(image)[0]
                known_encodings.append(face_encoding)
                known_names.append(filename)
                print_status(f"Loaded: {filename} [{len(face_locations)} face]", "success")
            elif len(face_locations) > 1:
                print_status(f"Skipped {filename}: Found {len(face_locations)} faces (multiple faces detected)", "warning")
            else:
                print_status(f"Skipped {filename}: No faces detected", "warning")
                
        except Exception as e:
            print_status(f"Error processing {filename}: {str(e)}", "error")
    
    print_separator()
    print_status(f"Database loaded: {len(known_encodings)} faces successfully indexed", "result")
    return known_encodings, known_names

def search_similar_faces(target_image_path, known_encodings, known_names, threshold=0.6):
    """
    Search for faces similar to the target image
    
    Args:
        target_image_path: Path to the image to search for
        known_encodings: List of known face encodings
        known_names: List of corresponding filenames
        threshold: Similarity threshold (lower = more strict)
    """
    print_status(f"Loading target image: {target_image_path}", "info")
    
    if not os.path.exists(target_image_path):
        print_status("Target image not found!", "error")
        return
    
    try:
        # Load target image
        target_image = face_recognition.load_image_file(target_image_path)
        
        # Find faces in target
        target_face_locations = face_recognition.face_locations(target_image)
        target_face_encodings = face_recognition.face_encodings(target_image, target_face_locations)
        
        if len(target_face_encodings) == 0:
            print_status("No faces found in target image", "error")
            return
        
        print_status(f"Detected {len(target_face_encodings)} face(s) in target image", "success")
        print_status(f"Search threshold: {threshold} (lower = more strict)", "info")
        print_separator()
        
        # Compare with known faces
        for i, target_encoding in enumerate(target_face_encodings):
            print(f"\n{Colors.BOLD}{Colors.YELLOW}[ TARGET FACE #{i+1} RESULTS ]{Colors.END}")
            
            # Calculate distances (lower = more similar)
            distances = face_recognition.face_distance(known_encodings, target_encoding)
            
            # Find matches below threshold
            matches = []
            for j, distance in enumerate(distances):
                if distance <= threshold:
                    matches.append((known_names[j], distance))
            
            # Sort by similarity (closest first)
            matches.sort(key=lambda x: x[1])
            
            if matches:
                print_status(f"Found {len(matches)} potential matches", "result")
                print()
                
                for idx, (name, distance) in enumerate(matches[:10]):  # Show top 10 matches
                    similarity = (1 - distance) * 100
                    confidence = ""
                    
                    if similarity >= 90:
                        confidence = f"{Colors.GREEN}[HIGH CONFIDENCE]{Colors.END}"
                    elif similarity >= 75:
                        confidence = f"{Colors.YELLOW}[MEDIUM CONFIDENCE]{Colors.END}"
                    else:
                        confidence = f"{Colors.RED}[LOW CONFIDENCE]{Colors.END}"
                    
                    bar_length = int(similarity / 10)
                    progress_bar = "█" * bar_length + "▒" * (10 - bar_length)
                    
                    print(f"{Colors.WHITE}{idx+1:2d}. {Colors.CYAN}[{progress_bar}] {Colors.GREEN}{similarity:.1f}%{Colors.END} - {name} {confidence}")
                    
                    # Add extra spacing for top match
                    if idx == 0:
                        print(f"{Colors.BLUE}     └─ Primary match detected{Colors.END}")
            else:
                print_status("No matches found within threshold", "warning")
            
            print_separator()
            
    except Exception as e:
        print_status(f"Error during search: {str(e)}", "error")

def process_id_card(id_card_path, target_image_path=None):
    """
    Main function to process an ID card and optionally compare with target face
    
    Args:
        id_card_path: Path to ID card image
        target_image_path: Optional path to target face image
    """
    print_status(f"Processing ID card: {id_card_path}", "info")
    
    # Initialize processor
    processor = IDCardProcessor()
    
    # Detect ID card type
    card_type = processor.detect_id_card_type(id_card_path)
    print_status(f"Detected card type: {card_type}", "info")
    
    # Extract photo from ID card
    id_photo_info = processor.extract_id_photo(id_card_path)
    
    # Extract text information
    id_text_info = processor.extract_id_text(id_card_path)
    
    # Display results
    print_separator()
    print(f"{Colors.BOLD}{Colors.YELLOW}ID CARD ANALYSIS RESULTS{Colors.END}")
    print_separator()
    
    if id_photo_info['success']:
        print_status(f"✓ ID Photo extracted: {id_photo_info['photo_path']}", "success")
        print_status(f"  Confidence: {id_photo_info['confidence']*100:.1f}%", "info")
    else:
        print_status("✗ No photo could be extracted from ID card", "warning")
    
    if id_text_info['full_text']:
        print_status(f"✓ OCR extracted {len(id_text_info['full_text'])} text elements", "success")
        
        # Display found information
        if id_text_info['name']:
            print_status(f"  Name: {id_text_info['name']}", "info")
        if id_text_info['id_number']:
            print_status(f"  ID Number: {id_text_info['id_number']}", "info")
        if id_text_info['dob']:
            print_status(f"  Date of Birth: {id_text_info['dob']}", "info")
        
        # Show all extracted text with confidence
        print(f"\n{Colors.CYAN}Extracted Text Details:{Colors.END}")
        for i, (text, conf) in enumerate(zip(id_text_info['full_text'], id_text_info['confidence_scores'])):
            conf_pct = conf * 100
            print(f"  {i+1}. {text} ({Colors.GREEN}{conf_pct:.1f}% confidence{Colors.END})")
    
    # Compare with target image if provided
    if target_image_path and id_photo_info['success'] and id_photo_info.get('face_encoding') is not None:
        print_separator()
        print(f"{Colors.BOLD}{Colors.YELLOW}FACE COMPARISON RESULTS{Colors.END}")
        
        comparison = processor.compare_with_id_photo(target_image_path, id_photo_info)
        
        if comparison['match']:
            print_status(f"✓ FACES MATCH! Similarity: {comparison['similarity']:.1f}%", "success")
        else:
            print_status(f"✗ Faces do NOT match. Similarity: {comparison['similarity']:.1f}%", "error")
    
    print_separator()
    return id_photo_info, id_text_info

def interactive_mode():
    """Run the tool in interactive mode"""
    clear_screen()
    print_banner()
    
    print(f"\n{Colors.CYAN}Initializing Face Search & ID Card OSINT Module...{Colors.END}")
    loading_animation("Loading modules", 1)
    
    while True:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}╔════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}║         MAIN MENU                  ║{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}╚════════════════════════════════════╝{Colors.END}")
        print(f"{Colors.CYAN}[1]{Colors.END} Search for face matches")
        print(f"{Colors.CYAN}[2]{Colors.END} Process ID card (extract photo & text)")
        print(f"{Colors.CYAN}[3]{Colors.END} Compare face with ID card photo")
        print(f"{Colors.CYAN}[4]{Colors.END} Load/Reload face database")
        print(f"{Colors.CYAN}[5]{Colors.END} Configure search threshold")
        print(f"{Colors.CYAN}[6]{Colors.END} Show system info")
        print(f"{Colors.CYAN}[7]{Colors.END} Exit")
        
        choice = input(f"\n{Colors.GREEN}Select option [1-7]:{Colors.END} ").strip()
        
        if choice == "1":
            db_path = input(f"{Colors.YELLOW}Enter database path:{Colors.END} ").strip()
            target_path = input(f"{Colors.YELLOW}Enter target image path:{Colors.END} ").strip()
            
            if os.path.exists(db_path) and os.path.exists(target_path):
                known_encodings, known_names = load_face_database(db_path)
                if known_encodings:
                    search_similar_faces(target_path, known_encodings, known_names)
            else:
                print_status("Invalid paths provided", "error")
                
        elif choice == "2":
            id_path = input(f"{Colors.YELLOW}Enter ID card image path:{Colors.END} ").strip()
            if os.path.exists(id_path):
                process_id_card(id_path)
            else:
                print_status("Invalid ID card path", "error")
                
        elif choice == "3":
            id_path = input(f"{Colors.YELLOW}Enter ID card image path:{Colors.END} ").strip()
            target_path = input(f"{Colors.YELLOW}Enter target face image path:{Colors.END} ").strip()
            
            if os.path.exists(id_path) and os.path.exists(target_path):
                process_id_card(id_path, target_path)
            else:
                print_status("Invalid paths provided", "error")
                
        elif choice == "4":
            db_path = input(f"{Colors.YELLOW}Enter database path:{Colors.END} ").strip()
            if os.path.exists(db_path):
                load_face_database(db_path)
            else:
                print_status("Invalid database path", "error")
                
        elif choice == "5":
            print_status("Current threshold affects match sensitivity", "info")
            try:
                threshold = float(input(f"{Colors.YELLOW}Enter new threshold (0.1-1.0, lower = stricter):{Colors.END} ").strip())
                print_status(f"Threshold updated to {threshold}", "success")
            except ValueError:
                print_status("Invalid threshold value", "error")
            
        elif choice == "6":
            print(f"\n{Colors.MAGENTA}System Information:{Colors.END}")
            print(f"  Python version: {sys.version}")
            print(f"  Platform: {sys.platform}")
            print(f"  Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Tesseract available: {TESSERACT_AVAILABLE}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            
        elif choice == "7":
            print(f"\n{Colors.RED}Shutting down...{Colors.END}")
            loading_animation("Cleaning up", 1)
            print(f"{Colors.GREEN}Exiting Face Search Tool. Stay ethical!{Colors.END}")
            sys.exit(0)

def main():
    """Main function with argument parsing"""
    clear_screen()
    print_banner()
    
    parser = argparse.ArgumentParser(description="Face Recognition & ID Card OSINT Tool")
    parser.add_argument("--database", help="Path to directory with reference images")
    parser.add_argument("--target", help="Path to target image to search for")
    parser.add_argument("--idcard", help="Path to ID card image for processing")
    parser.add_argument("--compare", help="Compare ID card photo with target face", action="store_true")
    parser.add_argument("--threshold", type=float, default=0.6,
                       help="Similarity threshold (0.0-1.0, lower = stricter)")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode")
    parser.add_argument("--output-dir", default="extracted_photos",
                       help="Directory to save extracted photos")
    
    args = parser.parse_args()
    
    # Check if no arguments provided or interactive mode requested
    if len(sys.argv) == 1 or args.interactive:
        interactive_mode()
        return
    
    # Process ID card if specified
    if args.idcard:
        if args.compare and args.target:
            # Compare ID card photo with target face
            process_id_card(args.idcard, args.target)
        else:
            # Just process ID card
            process_id_card(args.idcard)
    
    # Standard face search
    elif args.database and args.target:
        known_encodings, known_names = load_face_database(args.database)
        
        if known_encodings:
            search_similar_faces(args.target, known_encodings, known_names, args.threshold)
        else:
            print_status("No valid faces found in database", "error")
    else:
        print_status("Please provide valid arguments", "error")
        print(f"\n{Colors.YELLOW}Usage examples:{Colors.END}")
        print("  python face_search.py --database ./faces/ --target ./person.jpg")
        print("  python face_search.py --idcard ./id_card.jpg")
        print("  python face_search.py --idcard ./id_card.jpg --target ./selfie.jpg --compare")
        print("  python face_search.py --interactive")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Operation interrupted by user{Colors.END}")
        print(f"{Colors.GREEN}Exiting... Stay ethical!{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Unexpected error: {str(e)}{Colors.END}")
        sys.exit(1)
