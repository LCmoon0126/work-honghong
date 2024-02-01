from flask import Flask, request, jsonify
from flask import render_template
import os
from zhipuai import ZhipuAI
import logging
from dotenv import load_dotenv

load_dotenv()
zhipu_apikey = os.getenv('ZHIPU_API_KEY')
use_model = "glm-4" #GLM-4
#use_model = "glm-3-turbo" #GLM-3-TURBO

app = Flask(__name__)

# 初始化 ZhipuAI 客户端
client = ZhipuAI(api_key=zhipu_apikey)  # 替换为你的 API Key

@app.route('/get-sys-prompt')
def get_sys_prompt():
    #print("Request received for sys prompt")
    return get_markdown_content('prompt/prompt-sys.md')

@app.route('/get-ass-prompt')
def get_ass_prompt():
    #print("Request received for ass prompt")
    return get_markdown_content('prompt/prompt-ass.md')

def get_markdown_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 转义换行和双引号
            content = content.replace('\n', '\\n').replace('"', '\\"')
            return jsonify({"content": content})
    else:
        return jsonify({"content": "Markdown 文件不存在"})

@app.route('/get-use-model')
def get_use_model():
    return jsonify({"use_model": use_model})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    try:
        response = client.chat.completions.create(
            model=use_model,
            messages=data['messages']
        )
        # 提取文本信息
        message_text = response.choices[0].message.content
        logging.info("Request data: %s", data)  # 记录请求数据
        logging.info("Response data: %s", response)  # 记录响应数据
        return jsonify({"response": message_text})
    except Exception as e:
        logging.error("Error in chat completion: %s", e)
        return jsonify({"response": "Error occurred"})

@app.route('/')
def index():
    return render_template('index.html')

# 配置日志
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

if __name__ == '__main__':
    app.run(debug=True)
