import subprocess
import io
import sys
import base64


def execute_code(language, code):
    language_config = {
        "shell": {
            "extension": "sh",
            "command": "bash cmd.sh"
        },
        "python": {
            "extension": "py",
            "command": "python3 cmd.py"
        },
        "java": {
            "extension": "java",
            "command": "java cmd.java"
        },
        "C": {
            "extension": "c",
            "command": "gcc cmd.c -o output && ./output"
        }
    }
    
    if language not in language_config:
        return base64.b64encode(f"Unsupport Language: {language}".encode('utf-8')).decode('utf-8')
    
    config = language_config[language]
    
    try:
        with open(f'cmd.{config["extension"]}', 'w', encoding='utf-8') as file:
            file.write(code)
        
        CMD = config["command"]
        proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
        proc.wait()
        stream_stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8')
        stream_stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8')
      
        str_stdout = str(stream_stdout.read())
        str_stderr = str(stream_stderr.read())

        res = "Stdout:\n" + str_stdout + "\n" +"Stderr:\n" + str_stderr
        #res = os.popen(config["command"]).read()
        
        string_bytes = res.encode('utf-8')
        res_raw = base64.b64encode(string_bytes)
        
        return res_raw.decode('utf-8')
        
    except Exception as e:
        error_msg = f"Runtime Error: {str(e)}"
        return base64.b64encode(error_msg.encode('utf-8')).decode('utf-8')


def main():
    if len(sys.argv) != 3:
        error_msg = "Useage: python main.py <language> <base64>"
        print(base64.b64encode(error_msg.encode('utf-8')).decode('utf-8'), end='')
        return
    
    language = sys.argv[1]
    cmd_raw = sys.argv[2]
    
    try:
        decoded_cmd = base64.b64decode(cmd_raw)
        str_cmd = decoded_cmd.decode('utf-8')
        
        result = execute_code(language, str_cmd)
        print(result, end='')
        
    except base64.binascii.Error:
        error_msg = "Error: Base64 code unsopport"
        print(base64.b64encode(error_msg.encode('utf-8')).decode('utf-8'), end='')
    except UnicodeDecodeError:
        error_msg = "Error: Cant translate code into UTF-8"
        print(base64.b64encode(error_msg.encode('utf-8')).decode('utf-8'), end='')
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(base64.b64encode(error_msg.encode('utf-8')).decode('utf-8'), end='')


if __name__ == "__main__":
    main()