import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog

class VisualNovelLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Novel Launcher")

        self.project_name_label = QLabel("Project Name:")
        self.project_name_entry = QLineEdit()
        self.project_folder_label = QLabel("Project Folder:")
        self.project_folder_button = QPushButton("Choose Folder")
        self.create_project_button = QPushButton("Create Project")

        self.project_folder_button.clicked.connect(self.choose_folder)
        self.create_project_button.clicked.connect(self.create_project)

        layout = QVBoxLayout()
        layout.addWidget(self.project_name_label)
        layout.addWidget(self.project_name_entry)
        layout.addWidget(self.project_folder_label)
        layout.addWidget(self.project_folder_button)
        layout.addWidget(self.create_project_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Project Folder")
        if folder:
            self.project_folder_label.setText(f"Project Folder: {folder}")
            self.project_folder = folder

    def create_project(self):
        project_name = self.project_name_entry.text()
        if hasattr(self, "project_folder"):
            project_data = {
                "project_name": project_name,
                "project_folder": self.project_folder
                # Add more project settings here
            }

            project_file_path = os.path.join(self.project_folder, "project.json")
            with open(project_file_path, "w") as project_file:
                json.dump(project_data, project_file)

            self.close()

def main():
    app = QApplication(sys.argv)
    launcher = VisualNovelLauncher()
    launcher.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
