import os 

def get_oui(mac):
    parts = mac.split(':')
    mac = parts[0] + parts[1] + parts[2]
    return mac

def load_oui_db(filename):
    oui_dict = {}
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                a = f.readlines()    
                for line in a:
                    parts = line.split()
                    if 'base 16' in line and len(parts) >= 4:
                        oui = parts[0]
                        company = ' '.join(parts[3:])
                        oui_dict[oui] = company
        else:
            print(f"[!] Файл {filename} не найден")                        
    except Exception as e:
        print(f"[!] Ошибка при чтении файла: {e}")
    return oui_dict

def get_manufacturer(oui, oui_db):
    return oui_db.get(oui, "Неизвестный производитель")

oui = get_oui("3C:17:10:E6:E3:F4")
oui_db = load_oui_db("oui.txt")

comp = get_manufacturer(oui, oui_db)
print(comp)

