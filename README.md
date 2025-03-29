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
   git clone https://github.com/your-repo/marker-gui-wrapper.git
   cd marker-gui-wrapper
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