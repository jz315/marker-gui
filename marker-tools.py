import sys
import os
import subprocess
import shutil # To check if marker_single exists
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QFileDialog, QCheckBox, QGroupBox, QTextEdit,
    QMessageBox, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QProcess, Qt, QCoreApplication
from PyQt5.QtCore import QSettings
# --- Configuration ---
# Attempt to find the marker_single executable
MARKER_COMMAND = shutil.which('marker_single')
# If not found in PATH, you might need to specify the full path manually
# MARKER_COMMAND = "/path/to/your/virtualenv/bin/marker_single"
# MARKER_COMMAND = "C:\\Users\\YourUser\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\marker_single.exe" # Example Windows path

# --- Main GUI Class ---
class MarkerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.process = QProcess(self)
        self.input_file = ""
        self.output_dir = ""
        self.initUI()
        self.check_marker_command()
        self.load_settings()

    def initUI(self):
        self.setWindowTitle('Marker GUI Wrapper')
        self.setGeometry(300, 300, 700, 600) # Increased height slightly for API key field

        self.settings = QSettings("MarkerGUI", "Application") 

        main_layout = QVBoxLayout()

        # --- Input / Output Selection ---
        io_group = QGroupBox("Input & Output")
        io_layout = QVBoxLayout()

        # Input File
        input_layout = QHBoxLayout()
        input_label = QLabel("Input File:")
        self.input_file_edit = QLineEdit()
        self.input_file_edit.setReadOnly(True)
        browse_input_btn = QPushButton("Browse...")
        browse_input_btn.clicked.connect(self.browse_input_file)
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_file_edit)
        input_layout.addWidget(browse_input_btn)
        io_layout.addLayout(input_layout)

        # Output Directory
        output_layout = QHBoxLayout()
        output_label = QLabel("Output Directory:")
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setReadOnly(True)
        browse_output_btn = QPushButton("Browse...")
        browse_output_btn.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_dir_edit)
        output_layout.addWidget(browse_output_btn)
        io_layout.addLayout(output_layout)

        # Output Format
        format_layout = QHBoxLayout()
        format_label = QLabel("Output Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["markdown", "json", "html"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch(1) # Push combo box to the left
        io_layout.addLayout(format_layout)

        io_group.setLayout(io_layout)
        main_layout.addWidget(io_group)

        # --- Marker Options ---
        options_group = QGroupBox("Marker Options")
        options_layout = QVBoxLayout()

        # -- LLM Options --
        llm_options_layout = QVBoxLayout() # Separate layout for LLM related things

        # Use LLM Checkbox
        llm_check_layout = QHBoxLayout()
        self.use_llm_check = QCheckBox("Use LLM (--use_llm)")
        self.use_llm_check.setToolTip(
            "Improves accuracy (tables, math, forms).\n"
            "Requires Gemini API Key below OR GOOGLE_API_KEY env var."
        )
        self.use_llm_check.stateChanged.connect(self.toggle_dependent_options)
        llm_check_layout.addWidget(self.use_llm_check)
        llm_check_layout.addStretch(1) # Push checkbox to the left
        llm_options_layout.addLayout(llm_check_layout)

        # Gemini API Key Input (Initially Hidden)
        self.gemini_api_key_layout = QHBoxLayout()
        self.gemini_api_key_label = QLabel("Gemini API Key:")
        self.gemini_api_key_edit = QLineEdit()
        self.gemini_api_key_edit.setPlaceholderText("Enter key (optional if GOOGLE_API_KEY env var is set)")
        #self.gemini_api_key_edit.setEchoMode(QLineEdit.Password) # Hide the key
        self.gemini_api_key_layout.addWidget(self.gemini_api_key_label)
        self.gemini_api_key_layout.addWidget(self.gemini_api_key_edit)
        llm_options_layout.addLayout(self.gemini_api_key_layout)
        # Hide initially
        self.gemini_api_key_label.hide()
        self.gemini_api_key_edit.hide()

        self.gemini_api_key_edit.textChanged.connect(self.save_settings)

        # Redo Math Checkbox (Dependent on Use LLM)
        math_check_layout = QHBoxLayout() # Layout to indent slightly maybe
        math_check_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)) # Indent
        self.redo_math_check = QCheckBox("Redo Inline Math (--redo_inline_math)")
        self.redo_math_check.setToolTip("Requires --use_llm. Improves inline math conversion.")
        self.redo_math_check.setEnabled(False) # Disabled by default
        math_check_layout.addWidget(self.redo_math_check)
        math_check_layout.addStretch(1)
        llm_options_layout.addLayout(math_check_layout)

        options_layout.addLayout(llm_options_layout)
        options_layout.addSpacerItem(QSpacerItem(10, 10)) # Add some space before other flags

        # -- Other Flags --
        flags_layout = QHBoxLayout()
        flags_col1_layout = QVBoxLayout()
        flags_col2_layout = QVBoxLayout()

        self.force_ocr_check = QCheckBox("Force OCR (--force_ocr)")
        self.force_ocr_check.setToolTip("Force OCR even if text seems extractable. Use for garbled text.")
        flags_col1_layout.addWidget(self.force_ocr_check)

        self.strip_ocr_check = QCheckBox("Strip Existing OCR (--strip_existing_ocr)")
        self.strip_ocr_check.setToolTip("Remove existing OCR layers before processing.")
        flags_col1_layout.addWidget(self.strip_ocr_check)

        self.paginate_check = QCheckBox("Paginate Output (--paginate_output)")
        self.paginate_check.setToolTip("Add page separators to the output.")
        flags_col2_layout.addWidget(self.paginate_check)

        self.no_images_check = QCheckBox("Disable Image Extraction (--disable_image_extraction)")
        self.no_images_check.setToolTip("Do not save images from the document.")
        flags_col2_layout.addWidget(self.no_images_check)

        flags_layout.addLayout(flags_col1_layout)
        flags_layout.addLayout(flags_col2_layout)
        options_layout.addLayout(flags_layout)

        # String options
        page_range_layout = QHBoxLayout()
        page_range_label = QLabel("Page Range (--page_range):")
        self.page_range_edit = QLineEdit()
        self.page_range_edit.setPlaceholderText("e.g., 0,5-10,20 (optional)")
        page_range_layout.addWidget(page_range_label)
        page_range_layout.addWidget(self.page_range_edit)
        options_layout.addLayout(page_range_layout)

        lang_layout = QHBoxLayout()
        lang_label = QLabel("Languages (--languages):")
        self.lang_edit = QLineEdit()
        self.lang_edit.setPlaceholderText("e.g., en,fr,de (optional, for OCR)")
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_edit)
        options_layout.addLayout(lang_layout)

        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)

        # --- Conversion & Output ---
        action_layout = QHBoxLayout()
        self.convert_btn = QPushButton("Convert") # Changed button text slightly
        self.convert_btn.clicked.connect(self.start_conversion)
        action_layout.addWidget(self.convert_btn)
        action_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)) # Add spacer
        main_layout.addLayout(action_layout)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Marker output and status will appear here...")
        main_layout.addWidget(self.output_text)

        self.setLayout(main_layout)

        # Connect QProcess signals
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        self.process.errorOccurred.connect(self.process_error)


    def check_marker_command(self):
        """Checks if the marker command is found."""
        if not MARKER_COMMAND:
            QMessageBox.warning(self, "Marker Not Found",
                                f"Could not automatically find 'marker_single' in your system's PATH.\n\n"
                                f"Please ensure 'marker-pdf' is installed correctly in your Python environment "
                                f"and that the environment's 'Scripts' or 'bin' directory is in your PATH.\n\n"
                                f"Alternatively, edit the MARKER_COMMAND variable at the top of this script "
                                f"to point to the full path of 'marker_single'.\n\n"
                                f"The application might not work correctly.")
            self.convert_btn.setEnabled(False) # Disable button if command not found
        else:
             self.output_text.append(f"Using marker command: {MARKER_COMMAND}\n")

    def browse_input_file(self):
        """Opens a file dialog to select the input PDF/document."""
        file_filter = "Supported Files (*.pdf *.png *.jpg *.jpeg *.bmp *.tiff *.pptx *.docx *.xlsx *.html *.epub);;PDF Files (*.pdf);;Images (*.png *.jpg *.jpeg *.bmp *.tiff);;Office Docs (*.pptx *.docx *.xlsx);;Web Files (*.html);;Ebooks (*.epub);;All Files (*)"
        fname, _ = QFileDialog.getOpenFileName(self, 'Open File', '', file_filter)
        if fname:
            self.input_file = fname
            self.input_file_edit.setText(fname)
            if not self.output_dir_edit.text():
                 default_output_dir = os.path.dirname(fname)
                 self.output_dir = default_output_dir
                 self.output_dir_edit.setText(default_output_dir)

    def browse_output_dir(self):
        """Opens a directory dialog to select the output folder."""
        dirname = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        if dirname:
            self.output_dir = dirname
            self.output_dir_edit.setText(dirname)

    def toggle_dependent_options(self, state):
        """Enable/disable options that depend on --use_llm."""
        is_checked = (state == Qt.Checked)

        # Toggle Gemini API Key field visibility
        self.gemini_api_key_label.setVisible(is_checked)
        self.gemini_api_key_edit.setVisible(is_checked)

        # Toggle Redo Inline Math checkbox enabled state
        self.redo_math_check.setEnabled(is_checked)

        if not is_checked:
            # Optionally clear the key field when unchecked
            # self.gemini_api_key_edit.clear()
            self.redo_math_check.setChecked(False) # Uncheck if parent is unchecked

    def build_command_args(self):
        """Constructs the list of arguments for marker_single."""
        if not self.input_file or not self.output_dir:
            QMessageBox.warning(self, "Missing Input", "Please select both an input file and an output directory.")
            return None

        # Ensure MARKER_COMMAND is valid before proceeding
        if not MARKER_COMMAND or not os.path.exists(MARKER_COMMAND):
             self.check_marker_command() # Show warning
             return None

        args = [self.input_file]

        args.extend(["--output_dir", self.output_dir])
        args.extend(["--output_format", self.format_combo.currentText()])

        if self.use_llm_check.isChecked():
            args.append("--use_llm")

            # Add Gemini API Key if provided in the GUI
            api_key = self.gemini_api_key_edit.text().strip()
            if api_key:
                args.extend(["--gemini_api_key", api_key])
            # If the GUI field is empty, marker will fall back to checking
            # the GOOGLE_API_KEY environment variable if it's set.

            # Only add --redo_inline_math if --use_llm is also checked
            if self.redo_math_check.isChecked():
                 args.append("--redo_inline_math")

        if self.force_ocr_check.isChecked():
            args.append("--force_ocr")
        if self.strip_ocr_check.isChecked():
             args.append("--strip_existing_ocr")
        if self.paginate_check.isChecked():
            args.append("--paginate_output")
        if self.no_images_check.isChecked():
            args.append("--disable_image_extraction")

        page_range = self.page_range_edit.text().strip()
        if page_range:
            args.extend(["--page_range", page_range])

        languages = self.lang_edit.text().strip()
        if languages:
            args.extend(["--languages", languages])

        return args

    def start_conversion(self):
        """Starts the marker_single process."""
        args = self.build_command_args()
        if args is None:
            return # Error message already shown or command not found

        self.output_text.clear()
        # Use list2cmdline on Windows for better quoting/spaces, otherwise join
        if os.name == 'nt':
             command_str = subprocess.list2cmdline([MARKER_COMMAND] + args)
        else:
             # Simple join might not be perfect for args with spaces, but okay for display
             command_str = f"{MARKER_COMMAND} {' '.join(args)}"

        self.output_text.append(f"Running command:\n{command_str}\n" + "-"*40 + "\n")
        QCoreApplication.processEvents() # Update UI to show the command

        self.convert_btn.setEnabled(False)
        self.output_text.append("Starting conversion...")

        try:
            # Make sure MARKER_COMMAND is executable
            if not os.access(MARKER_COMMAND, os.X_OK):
                 # Attempt to make it executable (Linux/macOS) - might fail due to permissions
                 try:
                     os.chmod(MARKER_COMMAND, os.stat(MARKER_COMMAND).st_mode | 0o111) # Add execute perm
                     self.output_text.append(f"\nINFO: Attempted to set execute permission on {MARKER_COMMAND}")
                 except OSError as e:
                     self.output_text.append(f"\nWARNING: Could not set execute permission on {MARKER_COMMAND}: {e}")

            self.process.start(MARKER_COMMAND, args)
            if not self.process.waitForStarted(3000):
                 self.output_text.append("\nERROR: Process failed to start. Check MARKER_COMMAND path and permissions.")
                 self.process_finished(-1, QProcess.CrashExit)
        except Exception as e:
             self.output_text.append(f"\nERROR: Failed to execute process: {e}")
             self.process_finished(-1, QProcess.CrashExit)

    def handle_stdout(self):
        """Reads and displays standard output from the process."""
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode(sys.stdout.encoding or 'utf-8', errors='ignore') # Use system encoding
        self.output_text.moveCursor(QTextCursor.End) # Ensure cursor is at end before append
        self.output_text.insertPlainText(stdout)
        self.output_text.moveCursor(QTextCursor.End) # Scroll down

    def handle_stderr(self):
        """Reads and displays standard error from the process."""
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode(sys.stderr.encoding or 'utf-8', errors='ignore') # Use system encoding
        # Make errors more prominent
        self.output_text.moveCursor(QTextCursor.End) # Ensure cursor is at end
        # Insert HTML for red color
        self.output_text.insertHtml(f"<font color='red'>{stderr.replace('<', '<').replace('>', '>').replace('&', '&').replace('\"', '"')}</font>") # Basic HTML escaping
        self.output_text.moveCursor(QTextCursor.End) # Scroll down

    def process_finished(self, exitCode, exitStatus):
        """Called when the marker process finishes."""
        status_msg = "finished"
        if exitStatus == QProcess.CrashExit:
            status_msg = "crashed"

        self.output_text.append("\n" + "-"*40)
        self.output_text.append(f"Process {status_msg} with exit code: {exitCode}")

        if exitCode == 0 and exitStatus == QProcess.NormalExit:
             self.output_text.append("Conversion successful!")
             output_format = self.format_combo.currentText()
             base_name = os.path.basename(self.input_file)
             name_without_ext = os.path.splitext(base_name)[0]
             potential_output_subfolder = os.path.join(self.output_dir, name_without_ext)
             potential_output_file = os.path.join(potential_output_subfolder, f"{name_without_ext}.{output_format}")
             potential_output_file_nosub = os.path.join(self.output_dir, f"{name_without_ext}.{output_format}")

             display_path = ""
             if os.path.exists(potential_output_file):
                 display_path = potential_output_file
             elif os.path.exists(potential_output_file_nosub):
                 display_path = potential_output_file_nosub
             else:
                 display_path = self.output_dir

             self.output_text.append(f"Output saved in/near: {display_path}")

        else:
             self.output_text.append("<font color='red'>Conversion failed or encountered errors.</font>")

        self.convert_btn.setEnabled(True)

    def process_error(self, error):
        """Handles errors related to starting or running the process itself."""
        error_map = {
            QProcess.FailedToStart: "Failed to start the process. Is the command correct and executable?",
            QProcess.Crashed: "Process crashed.",
            QProcess.Timedout: "Process timed out.",
            QProcess.ReadError: "Error reading from process.",
            QProcess.WriteError: "Error writing to process.",
            QProcess.UnknownError: "An unknown error occurred with the process."
        }
        error_string = error_map.get(error, "An unknown process error occurred.")
        self.output_text.moveCursor(QTextCursor.End)
        self.output_text.insertHtml(f"<br><font color='red'>PROCESS ERROR: {error_string}</font>")
        self.output_text.moveCursor(QTextCursor.End)

        # Ensure button is re-enabled even if process fails to start properly
        if not self.convert_btn.isEnabled():
             self.process_finished(error, QProcess.CrashExit) # Call finished to re-enable button

    def load_settings(self):
        """加载保存的配置"""
        # 加载API密钥
        api_key = self.settings.value("GeminiAPIKey", "", type=str)
        if api_key:
            self.gemini_api_key_edit.setText(api_key)
        
        # 可以加载其他设置（可选）
        recent_input = self.settings.value("RecentInput", "", type=str)
        if recent_input:
            self.input_file_edit.setText(recent_input)
            self.input_file = recent_input

    def save_settings(self):
        """保存当前配置"""
        # 保存API密钥
        self.settings.setValue("GeminiAPIKey", self.gemini_api_key_edit.text())
        
        # 保存最近使用的输入文件路径（可选）
        self.settings.setValue("RecentInput", self.input_file)

    def closeEvent(self, event):
        """窗口关闭时保存设置"""
        self.save_settings()
        super().closeEvent(event)

    # Import QTextCursor for scrolling
    from PyQt5.QtGui import QTextCursor

# --- Main Execution ---
if __name__ == '__main__':
    # Set high DPI scaling attribute if needed (before creating QApplication)
    # Based on Qt version, you might use different attributes
    try:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    except AttributeError:
        print("Note: High DPI attributes not available in this Qt version.")

    app = QApplication(sys.argv)
    ex = MarkerGUI()
    ex.show()
    sys.exit(app.exec_())