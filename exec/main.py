import os
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
        return base64.b64encode(f"不支持的语言: {language}".encode('utf-8')).decode('utf-8')
    
    config = language_config[language]
    
    try:
        with open(f'cmd.{config["extension"]}', 'w', encoding='utf-8') as file:
            file.write(code)
        
        res = os.popen(config["command"]).read()
        
        string_bytes = res.encode('utf-8')
        res_raw = base64.b64encode(string_bytes)
        
        return res_raw.decode('utf-8')
        
    except Exception as e:
        error_msg = f"执行代码时出错: {str(e)}"
        return base64.b64encode(error_msg.encode('utf-8')).decode('utf-8')


def main():
    if len(sys.argv) != 3:
        error_msg = "用法: python main.py <语言> <base64编码的代码>"
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
        error_msg = "错误: Base64编码无效"
        print(base64.b64encode(error_msg.encode('utf-8')).decode('utf-8'), end='')
    except UnicodeDecodeError:
        error_msg = "错误: 无法将代码解码为UTF-8格式"
        print(base64.b64encode(error_msg.encode('utf-8')).decode('utf-8'), end='')
    except Exception as e:
        error_msg = f"错误: {str(e)}"
        print(base64.b64encode(error_msg.encode('utf-8')).decode('utf-8'), end='')


if __name__ == "__main__":
    main()