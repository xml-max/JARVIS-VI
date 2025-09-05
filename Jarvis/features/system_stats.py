import psutil, math

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   #print("%s %s" % (s, size_name[i]))
   return "%s %s" % (s, size_name[i])


def system_stats():
    cpu_stats = str(psutil.cpu_percent())
    battery_percent = psutil.sensors_battery()
    if not battery_percent:
        battery_percent = "Not Present"
    else:
        battery_percent = f"{battery_percent}%"
    
    memory_in_use = convert_size(psutil.virtual_memory().used)
    total_memory = convert_size(psutil.virtual_memory().total)
    final_res = f"""CPU:{cpu_stats}%, used RAM:{memory_in_use} total RAM:{total_memory} battery: {battery_percent}"""
    return final_res

print(system_stats())
 
