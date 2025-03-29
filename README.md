# Marker GUI Wrapper

Marker GUI Wrapper 是一个基于 PyQt5 的图形用户界面 (GUI)，[marker](https://github.com/vikparuchuri/marker) 项目的使用。`marker` 是一个强大的文档处理工具，支持从 PDF、图片、Office 文档等多种格式中提取内容并进行转换。

## 功能特性

- **输入/输出管理**：
  - 支持选择输入文件（PDF、图片、Office 文档等）。
  - 支持选择输出目录。
  - 支持多种输出格式（Markdown、JSON、HTML）。

- **高级选项**：
  - 支持启用 LLM（大语言模型）增强功能。
  - 支持配置 Gemini API 密钥或使用环境变量 `GOOGLE_API_KEY`。
  - 支持重新处理内联数学公式。
  - 支持强制 OCR、移除现有 OCR 层、分页输出等选项。
  - 支持指定页面范围和语言。

- **实时输出**：
  - 实时显示 `marker_single` 的标准输出和错误信息。
  - 高亮显示错误信息。

- **设置管理**：
  - 自动保存和加载用户的配置（如 API 密钥和最近使用的输入文件）。

## 安装

1. 确保已安装 Python 3 和 `marker_single` 工具。
   ```bash
   pip install marker-pdf
   ```

2. 安装 PyQt5：
   ```bash
   pip install PyQt5
   ```

3. 克隆或下载此项目到本地：
   ```bash
   git clone https://github.com/your-repo/marker-gui-wrapper.git
   cd marker-gui-wrapper
   ```

4. 确保 `marker_single` 可执行文件在系统的 PATH 中，或者在 `marker-tools.py` 文件顶部手动设置 `MARKER_COMMAND` 的路径。

## 使用方法

1. 运行 GUI：
   ```bash
   python marker-tools.py
   ```

2. 在界面中：
   - 点击 **Browse...** 按钮选择输入文件和输出目录。
   - 配置所需的选项（如输出格式、LLM 设置等）。
   - 点击 **Convert** 按钮开始转换。

3. 转换完成后，输出文件将保存在指定的输出目录中。

## 常见问题

### 1. 无法找到 `marker_single`
- 确保 `marker_single` 已正确安装并在系统的 PATH 中。
- 如果未在 PATH 中，请在 `marker-tools.py` 文件顶部手动设置 `MARKER_COMMAND` 的完整路径。

### 2. 高 DPI 显示问题
- 如果界面显示模糊，可以尝试在代码中启用高 DPI 支持：
  ```python
  QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
  QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
  ```

### 3. LLM 功能无法使用
- 确保已设置 Gemini API 密钥或环境变量 `GOOGLE_API_KEY`。

## 贡献

欢迎提交问题和功能请求！您可以通过 GitHub 提交 Pull Request 或 Issue。

## 许可证

本项目基于 [MIT License](LICENSE) 开源。