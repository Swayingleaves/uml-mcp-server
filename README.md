# UML-MCP-Server

[English](README.md) | [中文](README_zh.md)

[![smithery badge](https://smithery.ai/badge/@Swayingleaves/uml-mcp-server)](https://smithery.ai/server/@Swayingleaves/uml-mcp-server)

UML-MCP Server is a UML diagram generation tool based on MCP (Model Context Protocol), which can help users generate various types of UML diagrams through natural language description or directly writing PlantUML code.

## Functional Features

- Supports multiple UML diagram types: class diagram, sequence diagram, activity diagram, use case diagram, state diagram, component diagram, deployment diagram, object diagram
- UML diagrams can be generated through natural language description
- You can directly use PlantUML code to generate UML diagrams
- Return PlantUML code and accessible URL links for easy sharing and viewing
- Simultaneously save the generated UML diagram locally and provide the local file path
- Support custom save path and specify the output directory for UML images
- As an MCP server, it can integrate with clients that support MCP, such as Claude
- A comprehensive logging system that records server operating status and operation logs

## Installation

### Installing via Smithery

To install UML Diagram Generation Tool for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@Swayingleaves/uml-mcp-server):

```bash
npx -y @smithery/cli install @Swayingleaves/uml-mcp-server --client claude
```

### Manual Installation
1. Clone repository:

```bash
git clone https://github.com/yourusername/UML-MCP-Server.git
cd UML-MCP-Server
```

2. Create and activate a virtual environment:

```bash
python -m venv uml-mcp-venv
source uml-mcp-venv/bin/activate  # Linux/Mac
# Or
uml-mcp-venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage Method

### Used as a Python Library

```python
from fix_plantuml import generate_uml

# Create UML code
uml_code = """
@startuml
Title: Simple Class Diagram

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

# Generate URLs, code, and local paths for UML diagrams
result = generate_uml(uml_code)

# Output result
print("PlantUML code: ")
print(result["code"])
print("\nPlantUML URL:")
print(result["url"])
print("\nLocal file path: ")
print(result["local_path"])
```

### Configure MCP in Cursor

The Cursor supports MCP (Model Context Protocol) servers, allowing you to directly generate UML diagrams using UML-MCP Server in the Cursor. The configuration steps are as follows:

1. Ensure that the latest version of Cursor IDE (which supports MCP functionality) is installed.

2. Open the configuration file of Cursor:

- On macOS: `~/Library/Application Support/Cursor/config.json`
- On Windows: `%APPDATA%\Cursor\config.json`
- On Linux: `~/.config/Cursor/config.json`

3. Add or modify the 'mcpServer' section in the configuration file:

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

Configuration Description:

- UML-MCP-Server: The name of the MCP server can be modified as needed
- Command: Use UV as the running command
- `args`:
  - directory: Specify the absolute path of the project directory
  - `run`: Run the command
  - uml_mcp_server.py: Main program file
- `output_dir`: Specify the output directory for UML images

Please modify the following path according to your actual situation:

- Replace '/Users/Yourpath/UML-MCP Server' with the actual path of your UML-MCP Server project
- Replace '/Users/Yourpath/uml-output' with the directory path where you want to save the UML image

4. Save the configuration file and restart the Cursor.

5. Use UML-MCP Server in Cursor:
- Open a new chat window
- In the toolbar at the bottom of the chat interface, you will see the "UML-MCP Server" tool icon
- Clicking on this icon will bring up the options menu for UML tools
- Select the UML diagram type you need (such as "Generate Class Diagram", "Generate Sequence Diagram", etc.)

### Using UML Tools in Cursor

In the Cursor, you can input:

For example:
```
1. Understand the certification process of the project
2. Generate UML code for the authentication process and generate a flowchart through UML-MCP Server
3. Attention: "output_dir": "/Users/my-project/uml-output"
```

### The Results Returned by UML Tools

Regardless of how UML tools are used, Cursor will call UML-MCP-Server and return the following:

1. **PlantUML Code** - You can copy this code to use in other PlantUML tools
2. PlantUML URL - You can open this URL in a browser to view the generated UML diagram
3. **Local file path** - The generated UML image is saved in this local path

For example:

```
Class diagram generated:

PlantUML code:
@startuml
Title: User and Order System
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

Local file path:
/Users/username/projects/UML-MCP-Server/output/class_diagram_12345.png
```

You can view the generated UML diagram in the following ways:

- Click on the returned URL link to view in the browser
- Open the local file path in the file browser to view the saved image
- In Cursor, you can use Markdown syntax to directly display images in the chat window

## Troubleshooting

If you encounter problems while using UML-MCP Server, you can try the following steps:

1. **Check log files**: View the log files in the 'logs' directory for error details
2. **Verify Dependency Installation**: Ensure that all dependencies are installed correctly
3. **Check network connection**: Ensure that PlantUML server (www.plantuml.com) can be accessed
4. **Check output directory permissions**: Ensure that the program has permission to write to the 'output' directory

Common problems and solutions:

- Unable to generate UML diagram: Check for error messages in the log, which may be due to network issues or temporary unavailability of PlantUML server
- **Image not saved locally**: Check if the 'output' directory exists and has write permission
- MCP server cannot start: Check the log file to ensure there are no port conflicts or other program errors

## Contribution

Welcome to contribute code, report issues, or provide improvement suggestions! Please participate in project development through GitHub Issues or Pull Requests.

## License

This project adopts the MIT license. Please refer to the LICENSE document for details.
