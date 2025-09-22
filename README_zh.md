# UML-MCP-Server

[English](README.md) | [中文](README_zh.md)

UML-MCP-Server 是一个基于 MCP (Model Context Protocol) 的 UML 图生成工具，可以帮助用户通过自然语言描述或直接编写 PlantUML 代码来生成各种类型的 UML 图。

## 功能特点

- 支持多种 UML 图类型：类图、序列图、活动图、用例图、状态图、组件图、部署图、对象图
- 可以通过自然语言描述生成 UML 图
- 可以直接使用 PlantUML 代码生成 UML 图
- 返回 PlantUML 代码和可访问的 URL 链接，方便分享和查看
- 同时将生成的 UML 图保存到本地，提供本地文件路径
- 支持自定义保存路径，可以指定 UML 图片的输出目录
- 作为 MCP 服务器，可以与支持 MCP 的客户端（如 Claude）集成
- 完善的日志记录系统，记录服务器运行状态和操作日志

## 安装

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/UML-MCP-Server.git
cd UML-MCP-Server
```

2. 创建并激活虚拟环境：

```bash
python -m venv uml-mcp-venv
source uml-mcp-venv/bin/activate  # Linux/Mac
# 或
uml-mcp-venv\Scripts\activate  # Windows
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 使用容器
```bash
# 构建容器
docker compose build

# 启动容器
docker compose up -d

# 访问验证 http://localhost:8001/see 

```

### 作为 Python 库使用

```python
from fix_plantuml import generate_uml

# 创建UML代码
uml_code = """
@startuml
title 简单类图

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

# 生成UML图的URL、代码和本地路径
result = generate_uml(uml_code)

# 输出结果
print("PlantUML代码:")
print(result["code"])
print("\nPlantUML URL:")
print(result["url"])
print("\n本地文件路径:")
print(result["local_path"])
```

### 在 Cursor 中配置 MCP

Cursor 支持 MCP（Model Context Protocol）服务器，可以让你直接在 Cursor 中使用 UML-MCP-Server 生成 UML 图。配置步骤如下：

1. 确保已安装最新版本的 Cursor IDE（支持 MCP 功能的版本）。

2. 打开 Cursor 的配置文件：

   - 在 macOS 上：`~/Library/Application Support/Cursor/config.json`
   - 在 Windows 上：`%APPDATA%\Cursor\config.json`
   - 在 Linux 上：`~/.config/Cursor/config.json`

3. 在配置文件中添加或修改`mcpServers`部分：

```json
{
  "mcpServers": {
    "UML-MCP-Server": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/yourpath/UML-MCP-Server",
        "run",
        "uml_mcp_server.py"
      ],
      "output_dir": "/Users/yourpath/uml-output"
    }
  }
}
```

配置说明：

- `UML-MCP-Server`：MCP 服务器的名称，可以根据需要修改
- `command`：使用 `uv` 作为运行命令
- `args`：
  - `--directory`：指定项目目录的绝对路径
  - `run`：运行命令
  - `uml_mcp_server.py`：主程序文件
- `output_dir`：指定 UML 图片的输出目录

请根据你的实际情况修改以下路径：

- 将 `/Users/yourpath/UML-MCP-Server` 替换为你的 UML-MCP-Server 项目的实际路径
- 将 `/Users/yourpath/uml-output` 替换为你想要保存 UML 图片的目录路径

4. 保存配置文件并重启 Cursor。

5. 在 Cursor 中使用 UML-MCP-Server：
   - 打开一个新的聊天窗口
   - 在聊天界面底部的工具栏中，你会看到"UML-MCP-Server"工具图标
   - 点击该图标，会出现 UML 工具的选项菜单
   - 选择你需要的 UML 图类型（如"生成类图"、"生成序列图"等）

### 在 Cursor 中使用 UML 工具

在 Cursor 中，你可以输入

例如：
```
1、理解项目的认证流程
2、把认证流程生成UML代码通过UML-MCP-Server生成流程图
3、注意："output_dir": "/Users/edy/vs-code/bjwa-task-project/uml-output"
```

### UML 工具返回的结果

无论通过哪种方式使用 UML 工具，Cursor 都会调用 UML-MCP-Server 并返回以下内容：

1. **PlantUML 代码** - 你可以复制这段代码在其他 PlantUML 工具中使用
2. **PlantUML URL** - 你可以在浏览器中打开这个 URL 查看生成的 UML 图
3. **本地文件路径** - 生成的 UML 图片保存在本地的这个路径下

例如：

```
已生成类图：

PlantUML代码：
@startuml
title 用户和订单系统
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

PlantUML URL：
http://www.plantuml.com/plantuml/png/~1UDgCqB5Bn0G1k1zYWM_EfPYQYY0Qd9oQc9oQaPcKYYcKc9gMYaiKc9gK...

本地文件路径：
/Users/username/projects/UML-MCP-Server/output/class_diagram_12345.png
```

你可以通过以下方式查看生成的 UML 图：

- 点击返回的 URL 链接在浏览器中查看
- 在文件浏览器中打开本地文件路径查看保存的图片
- 在 Cursor 中，你可以使用 Markdown 语法在聊天窗口中直接显示图片：


## 故障排除

如果你在使用 UML-MCP-Server 时遇到问题，可以尝试以下步骤：

1. **检查日志文件**：查看`logs`目录下的日志文件，了解错误详情
2. **验证依赖安装**：确保所有依赖已正确安装
3. **检查网络连接**：确保可以访问 PlantUML 服务器（www.plantuml.com）
4. **检查输出目录权限**：确保程序有权限写入`output`目录

常见问题及解决方案：

- **无法生成 UML 图**：检查日志中的错误信息，可能是网络问题或 PlantUML 服务器暂时不可用
- **图片未保存到本地**：检查`output`目录是否存在且有写入权限
- **MCP 服务器无法启动**：检查日志文件，确保没有端口冲突或其他程序错误

## 贡献

欢迎贡献代码、报告问题或提出改进建议！请通过 GitHub Issues 或 Pull Requests 参与项目开发。

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。
