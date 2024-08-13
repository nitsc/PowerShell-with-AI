from zhipuai import ZhipuAI
import os,subprocess

# 将自然语言转换为Python代码
def transform_code(code,address, key):
    
    # 构造提示
    prompt = f"请将以下给出的自然语言转为powershell命令，不需要任何解释：{code}"
    
    # 初始化响应
    response = None
    # 调用智谱AI API
    client = ZhipuAI(api_key=key)
    model_name = "glm-4"
    try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )
    except Exception as e:
            print(f"API调用失败: {e}")
            return
    
    # 如果响应为空，打印提示信息
    if response is None:
        print("API调用未能返回结果，请检查您的API Key和网络连接")
        return
    
    # 打印响应
    print(response)
    
    # 处理响应
    try:
        if hasattr(response, 'choices') and response.choices:
            choice = response.choices[0]
            if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                message_content = choice.message.content.replace("`", "").replace("python", "")
            else:
                message_content = choice.text.replace("`", "").replace("powershell", "")
                
            # 拼接新文件路径
            new_address = os.path.join(os.path.dirname(address), os.path.splitext(os.path.basename(address))[0] + '.ps1')
            # 写入新文件
            with open(new_address, 'w', encoding='utf-8') as file:
                file.write(message_content.strip())
            # 打印提示信息
            print(f"代码转换成功，路径为：{new_address}")
            subprocess.run(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'RemoteSigned', '-File', new_address], check=True)
            print("Powershell脚本已执行")
        else:
            print("API返回的对象没有choices属性或为空")
    except (AttributeError, KeyError) as e:
        print(f"处理API返回结果时出错: {e}")
        
while True:
    key = input("请输入API Key：")
    code = input("请输入自然语言：")
    transform_code(code,'D:\\',key)
