pip install --user -r requirements.txt
pyinstaller --onefile --key "$(openssl rand -base64 30)" commodoor.py