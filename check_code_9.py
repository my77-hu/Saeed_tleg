import os
import re
import asyncio
from telethon import TelegramClient

# مسار جلسة الرقم المحدد بدقة
session_path = 'Run-It/sessions/+967774134476.session'
project_dir = 'Run-It'

def find_api_credentials():
    api_id = None
    api_hash = None
    
    # البحث التلقائي عن بيانات API_ID و API_HASH في ملفات المشروع
    if os.path.exists(project_dir):
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith(('.py', '.env', '.json', '.txt', '.php')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            if not api_id:
                                id_match = re.search(r'(?:api_id|API_ID)\s*[:=]\s*["\']?(\d+)["\']?', content)
                                if id_match:
                                    api_id = int(id_match.group(1))
                                    
                            if not api_hash:
                                hash_match = re.search(r'(?:api_hash|API_HASH)\s*[:=]\s*["\']([a-fA-F0-9]{32})["\']', content)
                                if hash_match:
                                    api_hash = hash_match.group(1)
                    except Exception:
                        pass
                        
    return api_id, api_hash

async def main():
    if not os.path.exists(session_path):
        print(f"[x] ملف الجلسة غير موجود في المسار: {session_path}")
        return

    print("[*] جارٍ البحث عن بيانات API_ID و API_HASH داخل ملفات المشروع تلقائياً...")
    api_id, api_hash = find_api_credentials()
    
    if not api_id or not api_hash:
        print("[!] لم يتم العثور على API_ID أو API_HASH تلقائياً.")
        return

    print(f"[+] تم العثور بنجاح -> API_ID: {api_id} | API_HASH: {api_hash}")
    print(f"[*] جارٍ الاتصال بجلسة الرقم: +967774134476 ...")
    
    client = TelegramClient(session_path, api_id, api_hash)
    
    try:
        await client.connect()
        if not await client.is_user_authorized():
            print("[-] عذراً، هذه الجلسة غير مسجلة الدخول حالياً أو منتهية.")
            return

        print("[+] متصل بنجاح! جارٍ جلب أحدث رسائل التحقق من تليجرام (777000)...")
        
        async for message in client.iter_messages(777000, limit=2):
            print(f"\n--------------------------------------------------")
            print(f"التاريخ: {message.date}")
            print(f"نص الرسالة:\n{message.text}")
            print(f"--------------------------------------------------")
            
    except Exception as e:
        print(f"[!] حدث خطأ أثناء الاتصال: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
