import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QTextEdit, QSlider
import json
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from Backend import Backend

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        
        self.init_ui()

    def init_ui(self):
        
        # 創建按鈕、標籤和文字方塊
        self.backend = Backend(self)
        self.button_select_folder = QPushButton('選擇資料夾')
        self.label_selected_folder = QLabel('選擇的資料夾:')
        # self.text_edit_file_list = QTextEdit()
        self.button_load_json = QPushButton('讀取JSON檔')
        self.label_selected_json = QLabel('選擇的JSON檔:')
        self.label_json_length = QLabel('["pose_3D"]的長度: N/A')
        self.label_min_max_frame_id = QLabel('最小 frame id: N/A\n最大 frame id: N/A')
        self.label_data_type = QLabel('JSON data type: N/A')
        self.label_type_description = QLabel('Type Description: N/A')
        self.button_plot_3d = QPushButton('畫出3D點')
        
        self.label_slider_min_frame_id = QLabel('調整最小 frame id')
        self.slider_min_frame_id = QSlider()
        self.slider_min_frame_id.setOrientation(1)  # 1 corresponds to horizontal orientation
        self.slider_min_frame_id.setTickInterval(1)
        self.slider_min_frame_id.setTickPosition(2)  # 2 corresponds to ticks below the slider
        self.label_min_frame_id_value = QLabel('最小 frame id: 0')
        
        self.label_slider_max_frame_id = QLabel('調整最大 frame id')
        self.slider_max_frame_id = QSlider()
        self.slider_max_frame_id.setOrientation(1)
        self.slider_max_frame_id.setTickInterval(1)
        self.slider_max_frame_id.setTickPosition(2)
        self.label_max_frame_id_value = QLabel('最大 frame id: 0')
        self.button_save_json = QPushButton('儲存')
        
        
        # 設置按鈕的點擊事件
        self.button_select_folder.clicked.connect(self.backend.select_folder)
        self.button_load_json.clicked.connect(self.backend.load_json)
        self.button_plot_3d.clicked.connect(self.backend.plot_3d_points)
        self.button_save_json.clicked.connect(self.backend.save_json)
        self.slider_min_frame_id.valueChanged.connect(self.backend.update_min_frame_label)
        self.slider_max_frame_id.valueChanged.connect(self.backend.update_max_frame_label)
        
        
       

        # 設置布局
        layout = QVBoxLayout()
        layout.addWidget(self.button_select_folder)
        layout.addWidget(self.label_selected_folder)
        layout.addWidget(self.button_load_json)
        layout.addWidget(self.label_selected_json)
        layout.addWidget(self.label_type_description)
        layout.addWidget(self.label_data_type)
        layout.addWidget(self.label_json_length)
        layout.addWidget(self.label_min_max_frame_id)
        layout.addWidget(self.button_plot_3d)
        layout.addWidget(self.label_slider_min_frame_id)
        layout.addWidget(self.slider_min_frame_id)
        layout.addWidget(self.label_min_frame_id_value)
        layout.addWidget(self.label_slider_max_frame_id)
        layout.addWidget(self.slider_max_frame_id)
        layout.addWidget(self.label_max_frame_id_value)
        layout.addWidget(self.button_save_json)

        # 設置主窗口的布局
        self.setLayout(layout)

        # 設置主窗口的屬性
        self.setWindowTitle('PyQt5 資料夾瀏覽器')
        self.setGeometry(300, 300, 600, 300)

        # 顯示主窗口
        self.show()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
