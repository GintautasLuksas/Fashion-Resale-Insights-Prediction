from PIL import Image
import os

source_folder = r"C:\Program Files (x86)\Ginto\Muzika\Softcore Shutdown"
output_folder = os.path.join(source_folder, "converted")
os.makedirs(output_folder, exist_ok=True)

for file_name in os.listdir(source_folder):
    if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
        img_path = os.path.join(source_folder, file_name)
        img = Image.open(img_path)
        img = img.resize((1280, 720), Image.LANCZOS)
        output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".png")
        img.save(output_path, format="PNG", quality=100)

print("All images converted to 1280x720 PNGs in", output_folder)
