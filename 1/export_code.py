import os

output_file = 'tum_kodlar.txt'
source_dir = '.'  # Current directory (1/)

extensions = ['.py', '.html', '.css', '.txt']
skip_dirs = ['__pycache__', 'instance', '.git', 'venv', 'static/img', '.pytest_cache'] 
skip_files = ['tum_kodlar.txt', 'export_code.py', 'club_management.db']

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write("PROJE KODLARI\n")
    outfile.write("==================================================\n\n")
    
    for root, dirs, files in os.walk(source_dir):
        # Modify dirs in-place to skip unwanted directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions) and file not in skip_files:
                file_path = os.path.join(root, file)
                
                outfile.write(f"{'='*50}\n")
                outfile.write(f"DOSYA: {file_path}\n")
                outfile.write(f"{'='*50}\n\n")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"Hata: Dosya okunamadı ({e})")
                
                outfile.write("\n\n")

print(f"Tüm kodlar {output_file} dosyasına başarıyla kaydedildi.")
