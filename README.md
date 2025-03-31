# Marker GUI Wrapper

Marker GUI Wrapper 是一个基于 PyQt5 的图形用户界面 (GUI)，[marker](https://github.com/vikparuchuri/marker) 项目的GUI包装。`marker` 是一个强大的文档处理工具，支持从 PDF、图片、Office 文档等多种格式中提取内容并进行转换。

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
   git clone https://github.com/jz315/marker-gui.git
   cd marker-gui
   ```

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

## 贡献

欢迎提交问题和功能请求！您可以通过 GitHub 提交 Pull Request 或 Issue。

## 许可证

本项目基于 [MIT License](LICENSE) 开源。

---

# Marker GUI Wrapper 

Marker GUI Wrapper is a GUI based on PyQt5, serving as a wrapper for the [marker](https://github.com/vikparuchuri/marker) project. `marker` is a powerful document processing tool that supports extracting and converting content from various formats such as PDFs, images, and Office documents.

## Installation

1. Ensure Python 3 and the `marker_single` tool are installed.
   ```bash
   pip install marker-pdf
   ```

2. Install PyQt5:
   ```bash
   pip install PyQt5
   ```

3. Clone or download this project locally:
   ```bash
   git clone https://github.com/jz315/marker-gui.git
   cd marker-gui
   ```

## Usage

1. Run the GUI:
   ```bash
   python marker-tools.py
   ```

2. In the interface:
   - Click the **Browse...** button to select the input file and output directory.
   - Configure the required options (e.g., output format, LLM settings, etc.).
   - Click the **Convert** button to start the conversion.

3. Once the conversion is complete, the output files will be saved in the specified output directory.

## Contribution

Feel free to submit issues and feature requests! You can contribute via GitHub by submitting Pull Requests or Issues.

## License

This project is open-sourced under the [MIT License](LICENSE).