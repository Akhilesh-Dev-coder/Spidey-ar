import os
import urllib.request
import urllib.parse
from PIL import Image

def generate_qr_poster(target_url, input_poster_path, output_poster_path):
    print(f"Generating QR Code for: {target_url}")
    
    # 1. Fetch QR code image from free QR server API
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={urllib.parse.quote(target_url)}"
    temp_qr_path = "temp_qr.png"
    
    try:
        urllib.request.urlretrieve(qr_url, temp_qr_path)
    except Exception as e:
        print(f"Error fetching QR code from API: {e}")
        return
    
    # 2. Open poster and QR code
    if not os.path.exists(input_poster_path):
        print(f"Error: Input poster not found at {input_poster_path}")
        return
        
    poster = Image.open(input_poster_path)
    qr_code = Image.open(temp_qr_path)
    
    # Get poster size
    w, h = poster.size
    print(f"Original Poster Size: {w}x{h}")
    
    # 3. Create a white backing square for the QR code to make it stand out and scan easily
    padding = 20
    qr_bg_size = 400 + (padding * 2) # 440x440
    qr_bg = Image.new("RGB", (qr_bg_size, qr_bg_size), "white")
    
    # Paste the QR code onto the white background
    qr_bg.paste(qr_code, (padding, padding))
    
    # 4. Position the QR code on the bottom-right corner of the poster
    margin = 50
    position = (w - qr_bg_size - margin, h - qr_bg_size - margin)
    print(f"Placing QR code at position: {position}")
    
    # Backup original poster if we are overwriting
    if input_poster_path == output_poster_path:
        backup_path = input_poster_path.replace(".jpg", "_original.jpg")
        if not os.path.exists(backup_path):
            poster.save(backup_path)
            print(f"Saved backup of original poster at: {backup_path}")
            
    # Paste on poster
    poster.paste(qr_bg, position)
    
    # Save the modified poster
    poster.save(output_poster_path, quality=95)
    print(f"Success! Saved printable poster with QR code at: {output_poster_path}")
    
    # Clean up temp file
    if os.path.exists(temp_qr_path):
        os.remove(temp_qr_path)

if __name__ == "__main__":
    url = "https://spidey.netlify.app"
    input_path = "assets/spidey.jpg"
    output_path = "assets/spidey.jpg" # Overwrites to automatically update WebAR preview
    generate_qr_poster(url, input_path, output_path)
