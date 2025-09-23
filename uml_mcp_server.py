#!/usr/bin/env python3
"""
UML-MCP-Server: UML图制作工具的MCP服务器实现 (修复版)
"""

import base64
import json
import os
import sys
import zlib
import requests
import logging
import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from mcp.server.fastmcp import FastMCP, Context

# 配置日志记录
def setup_logging():
    """配置日志记录器"""
    # 创建logs目录
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # 生成日志文件名，包含日期
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"uml_mcp_server_{current_date}.log")
    
    # 配置根日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logging.info("日志系统初始化完成")
    return logger

# 初始化日志记录器
logger = setup_logging()

# 初始化FastMCP服务器
logger.info("初始化FastMCP服务器")
mcp = FastMCP("UML")

# UML图类型
UML_TYPES = [
    "class", "sequence", "activity", "usecase", 
    "state", "component", "deployment", "object"
]
logger.debug(f"支持的UML图类型: {', '.join(UML_TYPES)}")

# 类图示例
CLASS_EXAMPLES = {
    "user_order": """
class User {
  -String name
  -String email
  +login()
  +logout()
}

class Order {
  -int id
  -Date date
  +process()
}

User "1" -- "many" Order: places
""",
    "student_course": """
class Student {
  -String name
  -int id
  +enroll(Course)
  +dropCourse(Course)
}

class Course {
  -String title
  -String code
  -int credits
  +addStudent(Student)
  +removeStudent(Student)
}

class Professor {
  -String name
  -String department
  +assignCourse(Course)
}

Student "many" -- "many" Course: enrolls in
Professor "1" -- "many" Course: teaches
"""
}

# 序列图示例
SEQUENCE_EXAMPLES = {
    "login": """
actor User
participant "Web App" as A
participant "Auth Service" as B
database "Database" as C

User -> A: Login Request
A -> B: Authenticate
B -> C: Query User
C --> B: Return User Data
B --> A: Auth Token
A --> User: Login Success
""",
    "checkout": """
actor Customer
participant "Shopping Cart" as Cart
participant "Payment Service" as Payment
participant "Order Service" as Order
database "Database" as DB

Customer -> Cart: Checkout
Cart -> Payment: Process Payment
Payment -> DB: Verify Payment Info
DB --> Payment: Payment Info Valid
Payment -> DB: Record Transaction
Payment --> Cart: Payment Success
Cart -> Order: Create Order
Order -> DB: Save Order
DB --> Order: Order Saved
Order --> Cart: Order Created
Cart --> Customer: Order Confirmation
"""
}
logger.debug("UML示例加载完成")

def plantuml_encode(text):
    """
    将PlantUML文本编码为URL安全的字符串
    
    参考: https://plantuml.com/text-encoding
    """
    logger.debug("开始PlantUML编码")
    # 使用官方推荐的编码方式
    compressed = zlib.compress(text.encode('utf-8'))
    
    # 标准base64的字符映射: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
    # PlantUML使用的字符映射: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_
    
    # 首先使用标准base64编码
    standard_b64 = base64.b64encode(compressed).decode('ascii')
    
    # 然后转换为PlantUML的编码
    result = ""
    for c in standard_b64:
        if c == 'A': result += '0'
        elif c == 'B': result += '1'
        elif c == 'C': result += '2'
        elif c == 'D': result += '3'
        elif c == 'E': result += '4'
        elif c == 'F': result += '5'
        elif c == 'G': result += '6'
        elif c == 'H': result += '7'
        elif c == 'I': result += '8'
        elif c == 'J': result += '9'
        elif c == 'K': result += 'A'
        elif c == 'L': result += 'B'
        elif c == 'M': result += 'C'
        elif c == 'N': result += 'D'
        elif c == 'O': result += 'E'
        elif c == 'P': result += 'F'
        elif c == 'Q': result += 'G'
        elif c == 'R': result += 'H'
        elif c == 'S': result += 'I'
        elif c == 'T': result += 'J'
        elif c == 'U': result += 'K'
        elif c == 'V': result += 'L'
        elif c == 'W': result += 'M'
        elif c == 'X': result += 'N'
        elif c == 'Y': result += 'O'
        elif c == 'Z': result += 'P'
        elif c == 'a': result += 'Q'
        elif c == 'b': result += 'R'
        elif c == 'c': result += 'S'
        elif c == 'd': result += 'T'
        elif c == 'e': result += 'U'
        elif c == 'f': result += 'V'
        elif c == 'g': result += 'W'
        elif c == 'h': result += 'X'
        elif c == 'i': result += 'Y'
        elif c == 'j': result += 'Z'
        elif c == 'k': result += 'a'
        elif c == 'l': result += 'b'
        elif c == 'm': result += 'c'
        elif c == 'n': result += 'd'
        elif c == 'o': result += 'e'
        elif c == 'p': result += 'f'
        elif c == 'q': result += 'g'
        elif c == 'r': result += 'h'
        elif c == 's': result += 'i'
        elif c == 't': result += 'j'
        elif c == 'u': result += 'k'
        elif c == 'v': result += 'l'
        elif c == 'w': result += 'm'
        elif c == 'x': result += 'n'
        elif c == 'y': result += 'o'
        elif c == 'z': result += 'p'
        elif c == '0': result += 'q'
        elif c == '1': result += 'r'
        elif c == '2': result += 's'
        elif c == '3': result += 't'
        elif c == '4': result += 'u'
        elif c == '5': result += 'v'
        elif c == '6': result += 'w'
        elif c == '7': result += 'x'
        elif c == '8': result += 'y'
        elif c == '9': result += 'z'
        elif c == '+': result += '-'
        elif c == '/': result += '_'
        elif c == '=': pass  # 忽略填充字符
        else: result += c
    
    logger.debug("PlantUML编码完成")
    return result

def generate_uml_image(uml_code, diagram_type=None, output_dir=None):
    """
    生成UML图的URL和代码，并保存到本地
    
    Args:
        uml_code: PlantUML代码
        diagram_type: UML图类型，用于生成文件名
        output_dir: 输出目录路径，必须显式提供
    
    Returns:
        dict: 包含以下键值对:
            - code: 原始PlantUML代码
            - url: 可访问的PlantUML URL
            - encoded: 编码后的字符串
            - local_path: 本地保存的文件路径
    """
    # 检查输出目录是否提供
    if not output_dir:
        error_msg = "必须提供输出目录（output_dir）"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info(f"开始生成UML图: {diagram_type if diagram_type else 'unknown'}, 输出目录: {output_dir}")
    
    try:
        # 编码UML代码
        encoded = plantuml_encode(uml_code)
        
        # 构建URL，添加~1前缀
        url = f"http://www.plantuml.com/plantuml/png/~1{encoded}"
        logger.debug(f"生成的PlantUML URL: {url}")
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        logger.debug(f"使用输出目录: {output_dir}")
        
        # 生成文件名
        if diagram_type:
            filename = f"{diagram_type}_{encoded[:10]}"
        else:
            filename = f"uml_{encoded[:10]}"
        
        # 构建完整的文件路径
        file_path = os.path.join(output_dir, f"{filename}.png")
        logger.debug(f"图片将保存到: {file_path}")
        
        # 发送请求获取图片
        logger.debug("发送HTTP请求获取图片")
        response = requests.get(url, timeout=30)
        
        # 检查响应状态码
        if response.status_code != 200:
            logger.error(f"PlantUML服务返回错误: {response.status_code}")
            logger.error(f"响应内容: {response.text}")
            raise requests.RequestException(f"PlantUML服务错误: {response.status_code}")
        
        # 检查响应内容是否为图像
        content_type = response.headers.get('Content-Type', '')
        if 'image' not in content_type:
            logger.error(f"响应不是图像，Content-Type: {content_type}")
            logger.error(f"响应内容: {response.text}")
            raise ValueError("未收到有效的图像")
        
        # 保存到文件
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"UML图生成成功，保存到: {file_path}")
        
        # 返回结果
        return {
            "code": uml_code,
            "url": url,
            "encoded": encoded,
            "local_path": file_path
        }
    
    except Exception as e:
        logger.error(f"生成UML图时出错: {str(e)}")
        logger.error(f"UML代码: \n{uml_code}")
        
        # 即使出错也返回URL和代码
        return {
            "code": uml_code,
            "url": url if 'url' in locals() else None,
            "encoded": encoded if 'encoded' in locals() else None,
            "local_path": None,
            "error": str(e)
        }

@mcp.tool()
def generate_uml(diagram_type: str, code: str, output_dir: str) -> str:
    """生成UML图并返回代码、URL和本地路径。

    Args:
        diagram_type: UML图类型 (class, sequence, activity, usecase, state, component, deployment, object)
        code: 完整的PlantUML代码
        output_dir: 输出目录路径，必须显式提供

    Returns:
        包含PlantUML代码、URL和本地路径的JSON字符串
    """
    # 检查输出目录是否提供
    if not output_dir:
        error_msg = "必须提供输出目录（output_dir）"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info(f"调用generate_uml工具: 类型={diagram_type}, 代码长度={len(code)}, 输出目录={output_dir}")
    
    # 验证图表类型
    diagram_type = diagram_type.lower()
    if diagram_type not in UML_TYPES:
        error_msg = f"不支持的UML图类型: {diagram_type}。支持的类型: {', '.join(UML_TYPES)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # 确保代码包含 @startuml 和 @enduml
    if "@startuml" not in code:
        logger.debug("添加缺失的@startuml标记")
        code = f"@startuml\n{code}"
    if "@enduml" not in code:
        logger.debug("添加缺失的@enduml标记")
        code = f"{code}\n@enduml"
    
    logger.debug(f"生成的UML代码:\n{code}")
    
    # 生成URL、代码和本地路径
    result = generate_uml_image(code, diagram_type, output_dir)
    
    # 返回JSON字符串
    logger.debug(f"generate_uml工具执行完成，生成URL: {result.get('url')}")
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
def generate_class_diagram(code: str, output_dir: str) -> str:
    """生成类图并返回代码和URL。

    Args:
        code: 完整的PlantUML类图代码
        output_dir: 输出目录路径，必须显式提供

    Returns:
        包含PlantUML代码和URL的JSON字符串
    """
    logger.info(f"调用generate_class_diagram工具: 代码长度={len(code)}...")
    return generate_uml("class", code, output_dir)

@mcp.tool()
def generate_sequence_diagram(code: str, output_dir: str) -> str:
    """生成序列图并返回代码和URL。

    Args:
        code: 完整的PlantUML序列图代码
        output_dir: 输出目录路径，必须显式提供

    Returns:
        包含PlantUML代码和URL的JSON字符串
    """
    logger.info(f"调用generate_sequence_diagram工具: 代码长度={len(code)}...")
    return generate_uml("sequence", code, output_dir)

@mcp.tool()
def generate_activity_diagram(code: str, output_dir: str) -> str:
    """生成活动图并返回代码和URL。

    Args:
        code: 完整的PlantUML活动图代码
        output_dir: 输出目录路径，必须显式提供

    Returns:
        包含PlantUML代码和URL的JSON字符串
    """
    logger.info(f"调用generate_activity_diagram工具: 代码长度={len(code)}...")
    return generate_uml("activity", code, output_dir)

@mcp.tool()
def generate_usecase_diagram(code: str, output_dir: str) -> str:
    """生成用例图并返回代码和URL。

    Args:
        code: 完整的PlantUML用例图代码
        output_dir: 输出目录路径，必须显式提供

    Returns:
        包含PlantUML代码和URL的JSON字符串
    """
    logger.info(f"调用generate_usecase_diagram工具: 代码长度={len(code)}...")
    return generate_uml("usecase", code, output_dir)

@mcp.tool()
def generate_state_diagram(code: str, output_dir: str) -> str:
    """生成状态图并返回代码和URL。

    Args:
        code: 完整的PlantUML状态图代码
        output_dir: 输出目录路径，必须显式提供

    Returns:
        包含PlantUML代码和URL的JSON字符串
    """
    logger.info(f"调用generate_state_diagram工具: 代码长度={len(code)}...")
    return generate_uml("state", code, output_dir)

@mcp.tool()
def generate_component_diagram(code: str, output_dir: str) -> str:
    """生成组件图并返回代码和URL。

    Args:
        code: 完整的PlantUML组件图代码
        output_dir: 输出目录路径，必须显式提供

    Returns:
        包含PlantUML代码和URL的JSON字符串
    """
    logger.info(f"调用generate_component_diagram工具: 代码长度={len(code)}...")
    return generate_uml("component", code, output_dir)

@mcp.tool()
def generate_deployment_diagram(code: str, output_dir: str) -> str:
    """生成部署图并返回代码和URL。

    Args:
        code: 完整的PlantUML部署图代码
        output_dir: 输出目录路径，必须显式提供

    Returns:
        包含PlantUML代码和URL的JSON字符串
    """
    logger.info(f"调用generate_deployment_diagram工具: 代码长度={len(code)}...")
    return generate_uml("deployment", code, output_dir)

@mcp.tool()
def generate_object_diagram(code: str, output_dir: str) -> str:
    """生成对象图并返回代码和URL。

    Args:
        code: 完整的PlantUML对象图代码
        output_dir: 输出目录路径，必须显式提供

    Returns:
        包含PlantUML代码和URL的JSON字符串
    """
    logger.info(f"调用generate_object_diagram工具: 代码长度={len(code)}...")
    return generate_uml("object", code, output_dir)

@mcp.tool()
def generate_uml_from_code(code: str, output_dir: str) -> str:
    """从PlantUML代码生成UML图并返回URL和本地路径。

    Args:
        code: 完整的PlantUML代码
        output_dir: 输出目录路径，必须显式提供

    Returns:
        包含PlantUML代码、URL和本地路径的JSON字符串
    """
    logger.info("调用generate_uml_from_code工具")
    logger.debug(f"PlantUML代码长度: {len(code)} 字符")
    
    # 确保代码包含@startuml和@enduml
    if "@startuml" not in code:
        logger.debug("添加缺失的@startuml标记")
        code = f"@startuml\n{code}"
    if "@enduml" not in code:
        logger.debug("添加缺失的@enduml标记")
        code = f"{code}\n@enduml"
    
    # 生成URL、代码和本地路径
    result = generate_uml_image(code, output_dir=output_dir)
    
    # 返回JSON字符串
    logger.debug(f"generate_uml_from_code工具执行完成，生成URL: {result.get('url')}")
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.resource("uml://types")
def get_uml_types() -> str:
    """获取支持的UML图类型列表。

    Returns:
        支持的UML图类型列表的JSON字符串
    """
    logger.info("获取UML图类型列表")
    return json.dumps({
        "types": UML_TYPES,
        "descriptions": {
            "class": "展示系统中的类、属性、方法以及它们之间的关系",
            "sequence": "展示对象之间的交互，按时间顺序排列",
            "activity": "展示工作流程或业务流程",
            "usecase": "展示系统功能及其与外部参与者的关系",
            "state": "展示对象在其生命周期内的不同状态",
            "component": "展示系统的组件及其依赖关系",
            "deployment": "展示系统的物理架构",
            "object": "展示系统在特定时刻的对象实例及其关系"
        }
    })

@mcp.prompt()
def create_class_diagram() -> str:
    """创建类图的提示模板。"""
    logger.info("使用类图提示模板")
    return """
请帮我创建一个类图，直接提供完整的PlantUML代码。

例如：
@startuml
class User {
  -String name
  -String email
  +login()
  +logout()
}

class Order {
  -int id
  -Date date
  +process()
}

User "1" -- "many" Order: places
@enduml
"""

@mcp.prompt()
def create_sequence_diagram() -> str:
    """创建序列图的提示模板。"""
    logger.info("使用序列图提示模板")
    return """
请帮我创建一个序列图，描述以下交互流程：

1. 参与者和系统组件
2. 消息交换的顺序
3. 时间线和生命线

例如：
- 用户登录系统的流程
- 包括用户、Web应用、认证服务和数据库
- 展示从用户发起登录请求到登录成功的完整流程
"""

if __name__ == "__main__":
    # 初始化并运行服务器
    logger.info("启动UML-MCP服务器")
    try:
        mcp.settings.host='0.0.0.0'
        mcp.settings.port=8001
        mcp.run(transport='sse')
    except Exception as e:
        logger.critical(f"服务器运行出错: {str(e)}", exc_info=True)
    finally:
        logger.info("服务器已关闭") 