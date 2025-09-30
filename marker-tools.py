import os
import sys
import shlex
import shutil
from pathlib import Path
from typing import Dict, Any

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QFileDialog, QCheckBox, QGroupBox, QPlainTextEdit,
    QMessageBox, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QProcess, Qt, QCoreApplication
from PyQt5.QtCore import QSettings


LANGUAGE_CHOICES = {
    "en": "English",
    "zh": "中文",
}


TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "app_title": "Marker GUI Wrapper",
        "input_output_group": "Input & Output",
        "input_file_label": "Input File:",
        "input_file_placeholder": "Select a document to convert",
        "browse_button": "Browse...",
        "output_dir_label": "Output Directory:",
        "output_dir_placeholder": "Choose where converted files will be saved",
        "output_format_label": "Output Format:",
        "marker_options_group": "Marker Options",
        "use_llm": "Use LLM (--use_llm)",
        "use_llm_tooltip": (
            "Improves accuracy (tables, math, forms).\n"
            "Requires appropriate API credentials for the selected service."
        ),
        "llm_service_label": "LLM Service:",
        "redo_math": "Redo Inline Math (--redo_inline_math)",
        "redo_math_tooltip": "Requires --use_llm. Improves inline math conversion.",
        "force_ocr": "Force OCR (--force_ocr)",
        "force_ocr_tooltip": "Force OCR even if text seems extractable. Use for garbled text.",
        "strip_ocr": "Strip Existing OCR (--strip_existing_ocr)",
        "strip_ocr_tooltip": "Remove existing OCR layers before processing.",
        "paginate": "Paginate Output (--paginate_output)",
        "paginate_tooltip": "Add page separators to the output.",
        "no_images": "Disable Image Extraction (--disable_image_extraction)",
        "no_images_tooltip": "Do not save images from the document.",
        "page_range_label": "Page Range (--page_range):",
        "page_range_placeholder": "e.g., 0,5-10,20 (optional)",
        "languages_label": "Languages (--languages):",
        "languages_placeholder": "e.g., en,fr,de (optional, for OCR)",
        "convert_button": "Convert",
        "output_placeholder": "Marker output and status will appear here...",
        "language_selector_label": "Language:",
        "marker_not_found_title": "Marker Not Found",
        "marker_not_found_message": (
            "Could not automatically find 'marker_single'.\n\n"
            "Please ensure Marker is installed in the current virtual environment or system PATH.\n\n"
            "You can also edit the MARKER_COMMAND discovery logic in this script to point to the correct executable."
        ),
        "marker_command_in_use": "Using marker command: {command}\n",
        "missing_input_title": "Missing Input",
        "missing_input_message": "Please select both an input file and an output directory.",
        "missing_fields_title": "Missing Configuration",
        "missing_fields_message": "Please fill in the required fields: {fields}.",
        "command_header": "Running command:\n{command}\n{line}\n",
        "starting_conversion": "Starting conversion...",
        "set_exec_info": "\nINFO: Attempted to set execute permission on {command}",
        "set_exec_warning": "\nWARNING: Could not set execute permission on {command}: {error}",
        "process_failed_start": "\nERROR: Process failed to start. Check marker path and permissions.",
        "process_failed_launch": "\nERROR: Failed to execute process: {error}",
        "process_status_line": "Process {status} with exit code: {code}",
        "process_success": "Conversion successful!",
        "process_failure": "Conversion failed or encountered errors.",
        "output_saved": "Output saved in/near: {path}",
        "process_error_prefix": "PROCESS ERROR: {message}",
        "unknown_process_error": "An unknown process error occurred.",
        "process_finished_divider": "\n{line}",
        "select_input_dialog": "Open File",
        "select_output_dialog": "Select Output Directory",
        "progress_default": "Progress",
        "llm_required_fields": "Required fields",
        "status_finished": "finished",
        "status_crashed": "crashed",
        "process_error_failed_to_start": "Failed to start the process. Is the command correct and executable?",
        "process_error_crashed": "Process crashed.",
        "process_error_timed_out": "Process timed out.",
        "process_error_read": "Error reading from process.",
        "process_error_write": "Error writing to process.",
        "process_error_unknown": "An unknown process error occurred with the process.",
        "service_gemini": "Gemini",
        "service_google_vertex": "Google Vertex",
        "service_ollama": "Ollama",
        "service_claude": "Claude",
        "service_openai": "OpenAI-compatible",
        "service_azure_openai": "Azure OpenAI",
        "field_gemini_api_key_label": "Gemini API Key:",
        "field_gemini_api_key_placeholder": "Enter key (optional if GOOGLE_API_KEY env var is set)",
        "field_vertex_project_id_label": "Vertex Project ID:",
        "field_vertex_project_id_placeholder": "Enter your Google Cloud project ID",
        "field_ollama_base_url_label": "Ollama Base URL:",
        "field_ollama_base_url_placeholder": "Optional (default http://localhost:11434)",
        "field_ollama_model_label": "Ollama Model:",
        "field_ollama_model_placeholder": "e.g., llama3",
        "field_claude_api_key_label": "Claude API Key:",
        "field_claude_api_key_placeholder": "Enter your Claude API key",
        "field_claude_model_name_label": "Claude Model Name:",
        "field_claude_model_name_placeholder": "Optional (e.g., claude-3-sonnet)",
        "field_openai_api_key_label": "OpenAI API Key:",
        "field_openai_api_key_placeholder": "Enter your OpenAI-compatible API key",
        "field_openai_model_label": "OpenAI Model:",
        "field_openai_model_placeholder": "Optional (e.g., gpt-4o-mini)",
        "field_openai_base_url_label": "OpenAI Base URL:",
        "field_openai_base_url_placeholder": "Optional custom endpoint",
        "field_azure_endpoint_label": "Azure Endpoint:",
        "field_azure_endpoint_placeholder": "Enter your Azure OpenAI endpoint",
        "field_azure_api_key_label": "Azure API Key:",
        "field_azure_api_key_placeholder": "Enter your Azure OpenAI API key",
        "field_azure_deployment_name_label": "Azure Deployment Name:",
        "field_azure_deployment_name_placeholder": "Enter your deployment name",
    },
    "zh": {
        "app_title": "Marker 图形界面",
        "input_output_group": "输入与输出",
        "input_file_label": "输入文件：",
        "input_file_placeholder": "请选择需要转换的文档",
        "browse_button": "浏览...",
        "output_dir_label": "输出目录：",
        "output_dir_placeholder": "请选择保存转换结果的位置",
        "output_format_label": "输出格式：",
        "marker_options_group": "Marker 参数",
        "use_llm": "使用 LLM (--use_llm)",
        "use_llm_tooltip": (
            "提升表格、数学公式等识别效果。\n"
            "需要为所选服务准备对应的 API 凭证。"
        ),
        "llm_service_label": "LLM 服务：",
        "redo_math": "重新识别行内数学公式 (--redo_inline_math)",
        "redo_math_tooltip": "需要勾选 --use_llm，提升行内公式转换质量。",
        "force_ocr": "强制 OCR (--force_ocr)",
        "force_ocr_tooltip": "即使文本可提取也强制执行 OCR，适用于乱码情况。",
        "strip_ocr": "移除已有 OCR (--strip_existing_ocr)",
        "strip_ocr_tooltip": "处理前移除文档中已有的 OCR 图层。",
        "paginate": "分页输出 (--paginate_output)",
        "paginate_tooltip": "在输出中加入分页分隔符。",
        "no_images": "不提取图片 (--disable_image_extraction)",
        "no_images_tooltip": "跳过文档中的图片保存。",
        "page_range_label": "页码范围 (--page_range)：",
        "page_range_placeholder": "例如：0,5-10,20（可选）",
        "languages_label": "语言 (--languages)：",
        "languages_placeholder": "例如：en,zh,de（可选，用于 OCR）",
        "convert_button": "开始转换",
        "output_placeholder": "Marker 的输出及状态信息会显示在这里...",
        "language_selector_label": "界面语言：",
        "marker_not_found_title": "未找到 Marker",
        "marker_not_found_message": (
            "未能自动找到 'marker_single'。\n\n"
            "请确认已在当前虚拟环境或系统 PATH 中安装 Marker。\n\n"
            "你也可以修改脚本中的 MARKER_COMMAND 查找逻辑以指定正确的可执行文件。"
        ),
        "marker_command_in_use": "已使用 marker 命令：{command}\n",
        "missing_input_title": "缺少输入",
        "missing_input_message": "请选择输入文件和输出目录。",
        "missing_fields_title": "配置不完整",
        "missing_fields_message": "请填写以下必填项：{fields}。",
        "command_header": "执行命令：\n{command}\n{line}\n",
        "starting_conversion": "开始执行转换...",
        "set_exec_info": "\n提示：已尝试为 {command} 添加可执行权限",
        "set_exec_warning": "\n警告：无法为 {command} 添加可执行权限：{error}",
        "process_failed_start": "\n错误：进程启动失败，请检查命令路径与权限。",
        "process_failed_launch": "\n错误：无法启动进程：{error}",
        "process_status_line": "进程{status}，退出码：{code}",
        "process_success": "转换成功！",
        "process_failure": "转换失败或执行过程中出现错误。",
        "output_saved": "结果已保存于：{path}",
        "process_error_prefix": "进程错误：{message}",
        "unknown_process_error": "发生未知的进程错误。",
        "process_finished_divider": "\n{line}",
        "select_input_dialog": "选择文件",
        "select_output_dialog": "选择输出目录",
        "progress_default": "进度",
        "llm_required_fields": "必填项",
        "status_finished": "已完成",
        "status_crashed": "已崩溃",
        "process_error_failed_to_start": "无法启动进程。请确认命令是否正确且可执行。",
        "process_error_crashed": "进程已崩溃。",
        "process_error_timed_out": "进程执行超时。",
        "process_error_read": "读取进程输出时发生错误。",
        "process_error_write": "向进程写入数据时发生错误。",
        "process_error_unknown": "进程发生未知错误。",
        "service_gemini": "Gemini",
        "service_google_vertex": "Google Vertex",
        "service_ollama": "Ollama",
        "service_claude": "Claude",
        "service_openai": "OpenAI 兼容",
        "service_azure_openai": "Azure OpenAI",
        "field_gemini_api_key_label": "Gemini API Key：",
        "field_gemini_api_key_placeholder": "若已配置 GOOGLE_API_KEY 环境变量则可留空",
        "field_vertex_project_id_label": "Vertex 项目 ID：",
        "field_vertex_project_id_placeholder": "请输入 Google Cloud 项目 ID",
        "field_ollama_base_url_label": "Ollama Base URL：",
        "field_ollama_base_url_placeholder": "可选，默认 http://localhost:11434",
        "field_ollama_model_label": "Ollama 模型：",
        "field_ollama_model_placeholder": "例如：llama3",
        "field_claude_api_key_label": "Claude API Key：",
        "field_claude_api_key_placeholder": "请输入 Claude API Key",
        "field_claude_model_name_label": "Claude 模型名称：",
        "field_claude_model_name_placeholder": "可选，例如：claude-3-sonnet",
        "field_openai_api_key_label": "OpenAI API Key：",
        "field_openai_api_key_placeholder": "请输入 OpenAI 兼容的 API Key",
        "field_openai_model_label": "OpenAI 模型：",
        "field_openai_model_placeholder": "可选，例如：gpt-4o-mini",
        "field_openai_base_url_label": "OpenAI Base URL：",
        "field_openai_base_url_placeholder": "可选，自定义接口地址",
        "field_azure_endpoint_label": "Azure Endpoint：",
        "field_azure_endpoint_placeholder": "请输入 Azure OpenAI Endpoint",
        "field_azure_api_key_label": "Azure API Key：",
        "field_azure_api_key_placeholder": "请输入 Azure OpenAI API Key",
        "field_azure_deployment_name_label": "Azure 部署名称：",
        "field_azure_deployment_name_placeholder": "请输入部署名称",
    },
}


LLM_SERVICES: Dict[str, Dict[str, Any]] = {
    "gemini": {
        "display_key": "service_gemini",
        "llm_service": None,
        "fields": ["gemini_api_key"],
    },
    "google_vertex": {
        "display_key": "service_google_vertex",
        "llm_service": "marker.services.vertex.GoogleVertexService",
        "fields": ["vertex_project_id"],
    },
    "ollama": {
        "display_key": "service_ollama",
        "llm_service": "marker.services.ollama.OllamaService",
        "fields": ["ollama_base_url", "ollama_model"],
    },
    "claude": {
        "display_key": "service_claude",
        "llm_service": "marker.services.claude.ClaudeService",
        "fields": ["claude_api_key", "claude_model_name"],
    },
    "openai": {
        "display_key": "service_openai",
        "llm_service": "marker.services.openai.OpenAIService",
        "fields": ["openai_api_key", "openai_model", "openai_base_url"],
    },
    "azure_openai": {
        "display_key": "service_azure_openai",
        "llm_service": "marker.services.azure_openai.AzureOpenAIService",
        "fields": ["azure_endpoint", "azure_api_key", "azure_deployment_name"],
    },
}


LLM_FIELD_CONFIGS: Dict[str, Dict[str, Any]] = {
    "gemini_api_key": {
        "arg": "--gemini_api_key",
        "settings_key": "GeminiAPIKey",
        "required": False,
        "label_key": "field_gemini_api_key_label",
        "placeholder_key": "field_gemini_api_key_placeholder",
    },
    "vertex_project_id": {
        "arg": "--vertex_project_id",
        "settings_key": "VertexProjectId",
        "required": True,
        "label_key": "field_vertex_project_id_label",
        "placeholder_key": "field_vertex_project_id_placeholder",
    },
    "ollama_base_url": {
        "arg": "--ollama_base_url",
        "settings_key": "OllamaBaseUrl",
        "required": False,
        "label_key": "field_ollama_base_url_label",
        "placeholder_key": "field_ollama_base_url_placeholder",
    },
    "ollama_model": {
        "arg": "--ollama_model",
        "settings_key": "OllamaModel",
        "required": False,
        "label_key": "field_ollama_model_label",
        "placeholder_key": "field_ollama_model_placeholder",
    },
    "claude_api_key": {
        "arg": "--claude_api_key",
        "settings_key": "ClaudeApiKey",
        "required": True,
        "label_key": "field_claude_api_key_label",
        "placeholder_key": "field_claude_api_key_placeholder",
    },
    "claude_model_name": {
        "arg": "--claude_model_name",
        "settings_key": "ClaudeModelName",
        "required": False,
        "label_key": "field_claude_model_name_label",
        "placeholder_key": "field_claude_model_name_placeholder",
    },
    "openai_api_key": {
        "arg": "--openai_api_key",
        "settings_key": "OpenAIApiKey",
        "required": True,
        "label_key": "field_openai_api_key_label",
        "placeholder_key": "field_openai_api_key_placeholder",
    },
    "openai_model": {
        "arg": "--openai_model",
        "settings_key": "OpenAIModel",
        "required": False,
        "label_key": "field_openai_model_label",
        "placeholder_key": "field_openai_model_placeholder",
    },
    "openai_base_url": {
        "arg": "--openai_base_url",
        "settings_key": "OpenAIBaseUrl",
        "required": False,
        "label_key": "field_openai_base_url_label",
        "placeholder_key": "field_openai_base_url_placeholder",
    },
    "azure_endpoint": {
        "arg": "--azure_endpoint",
        "settings_key": "AzureEndpoint",
        "required": True,
        "label_key": "field_azure_endpoint_label",
        "placeholder_key": "field_azure_endpoint_placeholder",
    },
    "azure_api_key": {
        "arg": "--azure_api_key",
        "settings_key": "AzureApiKey",
        "required": True,
        "label_key": "field_azure_api_key_label",
        "placeholder_key": "field_azure_api_key_placeholder",
    },
    "azure_deployment_name": {
        "arg": "--deployment_name",
        "settings_key": "AzureDeploymentName",
        "required": True,
        "label_key": "field_azure_deployment_name_label",
        "placeholder_key": "field_azure_deployment_name_placeholder",
    },
}


def find_marker_command() -> str:
    """Discover the marker executable, preferring the local virtual environment."""

    potential_paths = []
    script_dir = Path(__file__).resolve().parent
    venv_dir = script_dir / ".venv"

    if sys.platform.startswith("win"):
        potential_paths.append(venv_dir / "Scripts" / "marker_single.exe")
        if "VIRTUAL_ENV" in os.environ:
            potential_paths.append(Path(os.environ["VIRTUAL_ENV"]) / "Scripts" / "marker_single.exe")
    else:
        potential_paths.append(venv_dir / "bin" / "marker_single")
        if "VIRTUAL_ENV" in os.environ:
            potential_paths.append(Path(os.environ["VIRTUAL_ENV"]) / "bin" / "marker_single")

    interpreter_prefix = Path(sys.prefix)
    if sys.platform.startswith("win"):
        potential_paths.append(interpreter_prefix / "Scripts" / "marker_single.exe")
    else:
        potential_paths.append(interpreter_prefix / "bin" / "marker_single")

    for candidate in potential_paths:
        if candidate and candidate.is_file():
            return str(candidate)

    return shutil.which("marker_single") or ""


MARKER_COMMAND = find_marker_command()


class MarkerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.process = QProcess(self)
        self.input_file = ""
        self.output_dir = ""
        self.console_text = ""
        self._loading_settings = False

        self.settings = QSettings("MarkerGUI", "Application")
        saved_language = self.settings.value("Language", "en", type=str) or "en"
        self.current_language = saved_language if saved_language in LANGUAGE_CHOICES else "en"

        self.service_order = list(LLM_SERVICES.keys())
        self.service_field_widgets: Dict[str, QWidget] = {}
        self.service_field_labels: Dict[str, QLabel] = {}
        self.service_field_edits: Dict[str, QLineEdit] = {}

        self.init_ui()

        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        self.process.errorOccurred.connect(self.process_error)

        self.check_marker_command()
        self.load_settings()
        self.retranslate_ui()
        self.update_service_fields()

    def init_ui(self) -> None:
        self.setGeometry(300, 300, 720, 640)

        main_layout = QVBoxLayout()

        language_layout = QHBoxLayout()
        self.language_label = QLabel()
        self.language_combo = QComboBox()
        for code, name in LANGUAGE_CHOICES.items():
            self.language_combo.addItem(name, code)
        idx = self.language_combo.findData(self.current_language)
        if idx != -1:
            self.language_combo.setCurrentIndex(idx)
        self.language_combo.currentIndexChanged.connect(self.change_language)
        language_layout.addWidget(self.language_label)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch(1)
        main_layout.addLayout(language_layout)

        self.io_group = QGroupBox()
        io_layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.input_label = QLabel()
        self.input_file_edit = QLineEdit()
        self.input_file_edit.setReadOnly(True)
        self.browse_input_btn = QPushButton()
        self.browse_input_btn.clicked.connect(self.browse_input_file)
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_file_edit)
        input_layout.addWidget(self.browse_input_btn)
        io_layout.addLayout(input_layout)

        output_layout = QHBoxLayout()
        self.output_label = QLabel()
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setReadOnly(True)
        self.browse_output_btn = QPushButton()
        self.browse_output_btn.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_dir_edit)
        output_layout.addWidget(self.browse_output_btn)
        io_layout.addLayout(output_layout)

        format_layout = QHBoxLayout()
        self.format_label = QLabel()
        self.format_combo = QComboBox()
        self.format_combo.addItems(["markdown", "json", "html"])
        format_layout.addWidget(self.format_label)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch(1)
        io_layout.addLayout(format_layout)

        self.io_group.setLayout(io_layout)
        main_layout.addWidget(self.io_group)

        self.options_group = QGroupBox()
        options_layout = QVBoxLayout()

        llm_options_layout = QVBoxLayout()
        llm_check_layout = QHBoxLayout()
        self.use_llm_check = QCheckBox()
        self.use_llm_check.stateChanged.connect(self.toggle_dependent_options)
        llm_check_layout.addWidget(self.use_llm_check)
        llm_check_layout.addStretch(1)
        llm_options_layout.addLayout(llm_check_layout)

        self.llm_service_row = QWidget()
        llm_service_row_layout = QHBoxLayout()
        llm_service_row_layout.setContentsMargins(0, 0, 0, 0)
        self.llm_service_label = QLabel()
        self.llm_service_combo = QComboBox()
        for service_id in self.service_order:
            display_name = TRANSLATIONS[self.current_language].get(
                LLM_SERVICES[service_id]["display_key"],
                LLM_SERVICES[service_id]["display_key"],
            )
            self.llm_service_combo.addItem(display_name, service_id)
        self.llm_service_combo.currentIndexChanged.connect(self.update_service_fields)
        self.llm_service_combo.currentIndexChanged.connect(self.save_settings)
        llm_service_row_layout.addWidget(self.llm_service_label)
        llm_service_row_layout.addWidget(self.llm_service_combo)
        llm_service_row_layout.addStretch(1)
        self.llm_service_row.setLayout(llm_service_row_layout)
        llm_options_layout.addWidget(self.llm_service_row)

        self.service_fields_container = QWidget()
        self.service_fields_layout = QVBoxLayout()
        self.service_fields_layout.setContentsMargins(0, 0, 0, 0)
        self.service_fields_container.setLayout(self.service_fields_layout)
        llm_options_layout.addWidget(self.service_fields_container)

        for field_name, config in LLM_FIELD_CONFIGS.items():
            field_widget = QWidget()
            field_layout = QHBoxLayout()
            field_layout.setContentsMargins(0, 0, 0, 0)
            label = QLabel()
            edit = QLineEdit()
            edit.textChanged.connect(self.save_settings)
            field_layout.addWidget(label)
            field_layout.addWidget(edit)
            field_widget.setLayout(field_layout)
            self.service_fields_layout.addWidget(field_widget)
            field_widget.hide()
            self.service_field_widgets[field_name] = field_widget
            self.service_field_labels[field_name] = label
            self.service_field_edits[field_name] = edit

        self.service_fields_container.hide()
        self.llm_service_row.hide()

        math_check_layout = QHBoxLayout()
        math_check_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))
        self.redo_math_check = QCheckBox()
        self.redo_math_check.setEnabled(False)
        math_check_layout.addWidget(self.redo_math_check)
        math_check_layout.addStretch(1)
        llm_options_layout.addLayout(math_check_layout)

        options_layout.addLayout(llm_options_layout)
        options_layout.addSpacerItem(QSpacerItem(10, 10))

        flags_layout = QHBoxLayout()
        flags_col1_layout = QVBoxLayout()
        flags_col2_layout = QVBoxLayout()

        self.force_ocr_check = QCheckBox()
        flags_col1_layout.addWidget(self.force_ocr_check)

        self.strip_ocr_check = QCheckBox()
        flags_col1_layout.addWidget(self.strip_ocr_check)

        self.paginate_check = QCheckBox()
        flags_col2_layout.addWidget(self.paginate_check)

        self.no_images_check = QCheckBox()
        flags_col2_layout.addWidget(self.no_images_check)

        flags_layout.addLayout(flags_col1_layout)
        flags_layout.addLayout(flags_col2_layout)
        options_layout.addLayout(flags_layout)

        page_range_layout = QHBoxLayout()
        self.page_range_label = QLabel()
        self.page_range_edit = QLineEdit()
        page_range_layout.addWidget(self.page_range_label)
        page_range_layout.addWidget(self.page_range_edit)
        options_layout.addLayout(page_range_layout)

        lang_layout = QHBoxLayout()
        self.lang_label = QLabel()
        self.lang_edit = QLineEdit()
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_edit)
        options_layout.addLayout(lang_layout)

        self.options_group.setLayout(options_layout)
        main_layout.addWidget(self.options_group)

        action_layout = QHBoxLayout()
        self.convert_btn = QPushButton()
        self.convert_btn.clicked.connect(self.start_conversion)
        action_layout.addWidget(self.convert_btn)
        action_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        main_layout.addLayout(action_layout)

        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)

        self.setLayout(main_layout)

    def tr_text(self, key: str, **kwargs) -> str:
        language_map = TRANSLATIONS.get(self.current_language, TRANSLATIONS["en"])
        text = language_map.get(key, TRANSLATIONS["en"].get(key, key))
        if kwargs:
            return text.format(**kwargs)
        return text

    def change_language(self) -> None:
        new_language = self.language_combo.currentData()
        if not new_language or new_language == self.current_language:
            return
        self.current_language = new_language
        self.settings.setValue("Language", self.current_language)
        self.retranslate_ui()
        self.update_service_fields()

    def retranslate_ui(self) -> None:
        self.setWindowTitle(self.tr_text("app_title"))
        self.language_label.setText(self.tr_text("language_selector_label"))
        self.io_group.setTitle(self.tr_text("input_output_group"))
        self.input_label.setText(self.tr_text("input_file_label"))
        self.input_file_edit.setPlaceholderText(self.tr_text("input_file_placeholder"))
        self.browse_input_btn.setText(self.tr_text("browse_button"))
        self.output_label.setText(self.tr_text("output_dir_label"))
        self.output_dir_edit.setPlaceholderText(self.tr_text("output_dir_placeholder"))
        self.browse_output_btn.setText(self.tr_text("browse_button"))
        self.format_label.setText(self.tr_text("output_format_label"))

        self.options_group.setTitle(self.tr_text("marker_options_group"))
        self.use_llm_check.setText(self.tr_text("use_llm"))
        self.use_llm_check.setToolTip(self.tr_text("use_llm_tooltip"))
        self.llm_service_label.setText(self.tr_text("llm_service_label"))

        for index, service_id in enumerate(self.service_order):
            display_text = self.tr_text(LLM_SERVICES[service_id]["display_key"])
            if index < self.llm_service_combo.count():
                self.llm_service_combo.setItemText(index, display_text)

        for field_name, label in self.service_field_labels.items():
            config = LLM_FIELD_CONFIGS[field_name]
            label.setText(self.tr_text(config["label_key"]))
            self.service_field_edits[field_name].setPlaceholderText(
                self.tr_text(config["placeholder_key"])
            )

        self.redo_math_check.setText(self.tr_text("redo_math"))
        self.redo_math_check.setToolTip(self.tr_text("redo_math_tooltip"))
        self.force_ocr_check.setText(self.tr_text("force_ocr"))
        self.force_ocr_check.setToolTip(self.tr_text("force_ocr_tooltip"))
        self.strip_ocr_check.setText(self.tr_text("strip_ocr"))
        self.strip_ocr_check.setToolTip(self.tr_text("strip_ocr_tooltip"))
        self.paginate_check.setText(self.tr_text("paginate"))
        self.paginate_check.setToolTip(self.tr_text("paginate_tooltip"))
        self.no_images_check.setText(self.tr_text("no_images"))
        self.no_images_check.setToolTip(self.tr_text("no_images_tooltip"))
        self.page_range_label.setText(self.tr_text("page_range_label"))
        self.page_range_edit.setPlaceholderText(self.tr_text("page_range_placeholder"))
        self.lang_label.setText(self.tr_text("languages_label"))
        self.lang_edit.setPlaceholderText(self.tr_text("languages_placeholder"))
        self.convert_btn.setText(self.tr_text("convert_button"))
        self.output_text.setPlaceholderText(self.tr_text("output_placeholder"))

    def get_current_service_id(self) -> str:
        current_index = self.llm_service_combo.currentIndex()
        if current_index < 0:
            return self.service_order[0]
        return self.llm_service_combo.itemData(current_index)

    def check_marker_command(self) -> None:
        if not MARKER_COMMAND or not Path(MARKER_COMMAND).exists():
            QMessageBox.warning(
                self,
                self.tr_text("marker_not_found_title"),
                self.tr_text("marker_not_found_message"),
            )
            self.convert_btn.setEnabled(False)
        else:
            self.convert_btn.setEnabled(True)
            self._append_console_text(
                self.tr_text("marker_command_in_use", command=MARKER_COMMAND)
            )

    def browse_input_file(self) -> None:
        file_filter = (
            "Supported Files (*.pdf *.png *.jpg *.jpeg *.bmp *.tiff *.pptx *.docx *.xlsx *.html *.epub);;"
            "PDF Files (*.pdf);;Images (*.png *.jpg *.jpeg *.bmp *.tiff);;"
            "Office Docs (*.pptx *.docx *.xlsx);;Web Files (*.html);;Ebooks (*.epub);;All Files (*)"
        )
        fname, _ = QFileDialog.getOpenFileName(
            self,
            self.tr_text("select_input_dialog"),
            "",
            file_filter,
        )
        if fname:
            self.input_file = fname
            self.input_file_edit.setText(fname)
            if not self.output_dir_edit.text():
                default_output_dir = os.path.dirname(fname)
                self.output_dir = default_output_dir
                self.output_dir_edit.setText(default_output_dir)
            self.save_settings()

    def browse_output_dir(self) -> None:
        dirname = QFileDialog.getExistingDirectory(
            self,
            self.tr_text("select_output_dialog"),
        )
        if dirname:
            self.output_dir = dirname
            self.output_dir_edit.setText(dirname)
            self.save_settings()

    def toggle_dependent_options(self, state: int) -> None:
        is_checked = state == Qt.Checked
        self.llm_service_row.setVisible(is_checked)
        self.service_fields_container.setVisible(is_checked)
        self.redo_math_check.setEnabled(is_checked)
        if not is_checked:
            self.redo_math_check.setChecked(False)
        self.update_service_fields()
        self.save_settings()

    def update_service_fields(self) -> None:
        service_id = self.get_current_service_id()
        service_config = LLM_SERVICES.get(service_id, {})
        service_fields = set(service_config.get("fields", []))
        is_checked = self.use_llm_check.isChecked()

        for field_name, widget in self.service_field_widgets.items():
            should_show = is_checked and (field_name in service_fields)
            widget.setVisible(should_show)

        self.service_fields_container.setVisible(is_checked)
        self.llm_service_row.setVisible(is_checked)
        self.redo_math_check.setEnabled(is_checked)

    def _append_console_text(self, text: str, *, replace_line: bool = False) -> None:
        if text == "":
            return
        if replace_line:
            last_newline = self.console_text.rfind("\n")
            if last_newline == -1:
                self.console_text = text
            else:
                self.console_text = self.console_text[: last_newline + 1] + text
        else:
            self.console_text += text
        self.output_text.setPlainText(self.console_text)
        self.output_text.moveCursor(QTextCursor.End)
        self.output_text.ensureCursorVisible()
        QCoreApplication.processEvents()

    def _format_command_preview(self, args: list[str]) -> str:
        if os.name == "nt":
            return f"{MARKER_COMMAND} " + " ".join(args)
        quoted_args = " ".join(shlex.quote(arg) for arg in args)
        return f"{shlex.quote(MARKER_COMMAND)} {quoted_args}"

    def build_command_args(self) -> list[str] | None:
        if not self.input_file or not self.output_dir:
            QMessageBox.warning(
                self,
                self.tr_text("missing_input_title"),
                self.tr_text("missing_input_message"),
            )
            return None

        if not MARKER_COMMAND or not Path(MARKER_COMMAND).exists():
            self.check_marker_command()
            return None

        args = [self.input_file, "--output_dir", self.output_dir, "--output_format", self.format_combo.currentText()]

        page_range = self.page_range_edit.text().strip()
        if page_range:
            args.extend(["--page_range", page_range])

        languages = self.lang_edit.text().strip()
        if languages:
            args.extend(["--languages", languages])

        if self.force_ocr_check.isChecked():
            args.append("--force_ocr")
        if self.strip_ocr_check.isChecked():
            args.append("--strip_existing_ocr")
        if self.paginate_check.isChecked():
            args.append("--paginate_output")
        if self.no_images_check.isChecked():
            args.append("--disable_image_extraction")

        if self.use_llm_check.isChecked():
            args.append("--use_llm")
            service_id = self.get_current_service_id()
            service_config = LLM_SERVICES.get(service_id, {})
            llm_service_name = service_config.get("llm_service")
            if llm_service_name:
                args.extend(["--llm_service", llm_service_name])

            missing_fields = []
            for field_name in service_config.get("fields", []):
                config = LLM_FIELD_CONFIGS[field_name]
                value = self.service_field_edits[field_name].text().strip()
                if config.get("required") and not value:
                    label = self.tr_text(config["label_key"]).rstrip(":：")
                    missing_fields.append(label)
                if value:
                    args.extend([config["arg"], value])

            if missing_fields:
                QMessageBox.warning(
                    self,
                    self.tr_text("missing_fields_title"),
                    self.tr_text("missing_fields_message", fields=", ".join(missing_fields)),
                )
                return None

            if self.redo_math_check.isChecked():
                args.append("--redo_inline_math")
        else:
            if self.redo_math_check.isChecked():
                self.redo_math_check.setChecked(False)

        return args

    def start_conversion(self) -> None:
        args = self.build_command_args()
        if args is None:
            return

        command_str = self._format_command_preview(args)
        divider = "-" * 40
        self._append_console_text(self.tr_text("command_header", command=command_str, line=divider))

        self.convert_btn.setEnabled(False)
        self._append_console_text(self.tr_text("starting_conversion") + "\n")

        try:
            if not os.access(MARKER_COMMAND, os.X_OK) and os.name != "nt":
                try:
                    current_mode = os.stat(MARKER_COMMAND).st_mode
                    os.chmod(MARKER_COMMAND, current_mode | 0o111)
                    self._append_console_text(
                        self.tr_text("set_exec_info", command=MARKER_COMMAND)
                    )
                except OSError as error:
                    self._append_console_text(
                        self.tr_text("set_exec_warning", command=MARKER_COMMAND, error=error)
                    )

            self.process.start(MARKER_COMMAND, args)
            if not self.process.waitForStarted(3000):
                self._append_console_text(self.tr_text("process_failed_start"))
                self.process_finished(-1, QProcess.CrashExit)
        except Exception as error:  # pylint: disable=broad-except
            self._append_console_text(
                self.tr_text("process_failed_launch", error=error)
            )
            self.process_finished(-1, QProcess.CrashExit)

    def _format_error_segment(self, segment: str) -> str:
        lines = segment.split("\n")
        formatted_lines = []
        for line in lines:
            if line:
                formatted_lines.append(self.tr_text("process_error_prefix", message=line))
            else:
                formatted_lines.append("")
        return "\n".join(formatted_lines)

    def _process_console_output(self, text: str, *, is_error: bool = False) -> None:
        if not text:
            return
        normalized = text.replace("\r\n", "\n")
        segments = normalized.split("\r")
        for index, segment in enumerate(segments):
            replace_line = index < len(segments) - 1
            if is_error and segment:
                segment = self._format_error_segment(segment)
            if not segment:
                continue
            self._append_console_text(segment, replace_line=replace_line)

    def handle_stdout(self) -> None:
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode(sys.stdout.encoding or "utf-8", errors="ignore")
        self._process_console_output(stdout, is_error=False)

    def handle_stderr(self) -> None:
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode(sys.stderr.encoding or "utf-8", errors="ignore")
        self._process_console_output(stderr, is_error=True)

    def process_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        divider = "-" * 40
        status_key = "status_finished" if exit_status == QProcess.NormalExit else "status_crashed"
        status_text = self.tr_text(status_key)
        self._append_console_text(self.tr_text("process_finished_divider", line=divider) + "\n")
        self._append_console_text(
            self.tr_text("process_status_line", status=status_text, code=exit_code) + "\n"
        )

        if exit_code == 0 and exit_status == QProcess.NormalExit:
            self._append_console_text(self.tr_text("process_success") + "\n")
            output_format = self.format_combo.currentText()
            base_name = os.path.basename(self.input_file)
            name_without_ext = os.path.splitext(base_name)[0]
            potential_output_subfolder = os.path.join(self.output_dir, name_without_ext)
            potential_output_file = os.path.join(
                potential_output_subfolder,
                f"{name_without_ext}.{output_format}",
            )
            potential_output_file_nosub = os.path.join(
                self.output_dir,
                f"{name_without_ext}.{output_format}",
            )

            display_path = ""
            if os.path.exists(potential_output_file):
                display_path = potential_output_file
            elif os.path.exists(potential_output_file_nosub):
                display_path = potential_output_file_nosub
            else:
                display_path = self.output_dir

            self._append_console_text(
                self.tr_text("output_saved", path=display_path) + "\n"
            )
        else:
            self._append_console_text(self.tr_text("process_failure") + "\n")

        self.convert_btn.setEnabled(True)

    def process_error(self, error: QProcess.ProcessError) -> None:
        error_map = {
            QProcess.FailedToStart: self.tr_text("process_error_failed_to_start"),
            QProcess.Crashed: self.tr_text("process_error_crashed"),
            QProcess.Timedout: self.tr_text("process_error_timed_out"),
            QProcess.ReadError: self.tr_text("process_error_read"),
            QProcess.WriteError: self.tr_text("process_error_write"),
            QProcess.UnknownError: self.tr_text("process_error_unknown"),
        }
        message = error_map.get(error, self.tr_text("unknown_process_error"))
        self._append_console_text(self.tr_text("process_error_prefix", message=message) + "\n")
        if not self.convert_btn.isEnabled():
            self.process_finished(error, QProcess.CrashExit)

    def load_settings(self) -> None:
        self._loading_settings = True

        saved_service = self.settings.value("LLMService", self.service_order[0], type=str)
        index = self.llm_service_combo.findData(saved_service)
        if index != -1:
            self.llm_service_combo.setCurrentIndex(index)

        use_llm = self.settings.value("UseLLM", False, type=bool)
        self.use_llm_check.setChecked(use_llm)

        for field_name, edit in self.service_field_edits.items():
            settings_key = LLM_FIELD_CONFIGS[field_name]["settings_key"]
            value = self.settings.value(settings_key, "", type=str)
            if value:
                edit.setText(value)

        recent_input = self.settings.value("RecentInput", "", type=str)
        if recent_input:
            self.input_file = recent_input
            self.input_file_edit.setText(recent_input)

        recent_output = self.settings.value("RecentOutputDir", "", type=str)
        if recent_output:
            self.output_dir = recent_output
            self.output_dir_edit.setText(recent_output)

        self._loading_settings = False
        self.update_service_fields()

    def save_settings(self) -> None:
        if self._loading_settings:
            return

        self.settings.setValue("UseLLM", self.use_llm_check.isChecked())
        self.settings.setValue("LLMService", self.get_current_service_id())
        for field_name, edit in self.service_field_edits.items():
            settings_key = LLM_FIELD_CONFIGS[field_name]["settings_key"]
            self.settings.setValue(settings_key, edit.text())
        self.settings.setValue("RecentInput", self.input_file)
        self.settings.setValue("RecentOutputDir", self.output_dir)
        self.settings.setValue("Language", self.current_language)

    def closeEvent(self, event) -> None:  # type: ignore[override]
        self.save_settings()
        super().closeEvent(event)


if __name__ == '__main__':
    try:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    except AttributeError:
        pass

    app = QApplication(sys.argv)
    gui = MarkerGUI()
    gui.show()
    sys.exit(app.exec_())
