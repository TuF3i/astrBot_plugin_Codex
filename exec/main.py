import os 
import sys
import base64

def main():
    language =sys.argv[1]
    cmd_raw = sys.argv[2]

    decoded_cmd = base64.b64decode(cmd_raw)
    str_cmd = decoded_cmd.decode('utf-8')

    if language == "shell":
        with open('cmd.sh', 'w', encoding='utf-8') as file:
            file.write(str_cmd)
        res = os.popen("bash cmd.sh").read()
        string_bytes = res.encode('utf-8')
        res_raw = base64.b64encode(string_bytes)
        print(res_raw.decode('utf-8'),end='')

    elif language == "python":
        with open('cmd.py', 'w', encoding='utf-8') as file:
            file.write(str_cmd)
        res = os.popen("python3 cmd.py").read()
        string_bytes = res.encode('utf-8')
        res_raw = base64.b64encode(string_bytes)
        print(res_raw.decode('utf-8'),end='')

    elif language == "java":
        with open('cmd.java', 'w', encoding='utf-8') as file:
            file.write(str_cmd)
        res = os.popen("java cmd.java").read()
        string_bytes = res.encode('utf-8')
        res_raw = base64.b64encode(string_bytes)
        print(res_raw.decode('utf-8'),end='')

    
    elif language == "C":
        with open('cmd.c', 'w', encoding='utf-8') as file:
            file.write(str_cmd)
        res = os.popen("gcc cmd.c -o output && ./output").read()
        string_bytes = res.encode('utf-8')
        res_raw = base64.b64encode(string_bytes)
        print(res_raw.decode('utf-8'),end='')

    
if __name__ == "__main__":
    main()