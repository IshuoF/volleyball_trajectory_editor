import json
import os
from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def draw_volleyball_court(ax):
        points = np.array([
            [0, 0, 0], [9, 0, 0], [0, 6, 0], [9, 6, 0], [0, 9, 0],
            [9, 9, 0], [0, 12, 0], [9, 12, 0], [0, 18, 0], [9, 18, 0]
        ])
        courtedge = [2, 0, 1, 3, 2, 4, 5, 3, 5, 7, 6, 4, 6, 8, 9, 7]
        curves = points[courtedge]

        netpoints = np.array([
            [0, 9, 0], [0, 9, 1.24], [0, 9, 2.24], [9, 9, 0], [9, 9, 1.24], [9, 9, 2.24]])
        netedge = [0, 1, 2, 5, 4, 1, 4, 3]
        netcurves = netpoints[netedge]

        court = points.T
        courtX, courtY, courtZ = court
        # plot 3D court reference points

        ax.scatter(courtX, courtY, courtZ, c='black', marker='o', s=1)
        ax.plot(curves[:, 0], curves[:, 1], c='k',
                linewidth=2, alpha=0.5)  # plot 3D court edges
        ax.plot(netcurves[:, 0], netcurves[:, 1], netcurves[:, 2],
                c='k', linewidth=2, alpha=0.5)  # plot 3D net edges


class Backend:
    def __init__(self, gui_instance):
        # Initialize any backend-specific variables here
        self.loaded_filename = None
        self.gui_instance = gui_instance
    
    def select_folder(self):
        # 打開資料夾選擇對話框
        folder_path = QFileDialog.getExistingDirectory(self.gui_instance, '選擇資料夾')

        if folder_path:
            # 更新標籤顯示選擇的資料夾路徑
            self.gui_instance.label_selected_folder.setText(f'選擇的資料夾: {folder_path}')

    def load_json(self):
        # 打開檔案對話框以選擇 JSON 檔案
        file_path, _ = QFileDialog.getOpenFileName(self.gui_instance, '選擇JSON檔', '', 'JSON 檔案 (*.json)')

        with open('../VTC/classification_categories.json') as f:
            categories = json.load(f)
            
        
        description = ""
        if file_path:
            # 讀取 JSON 檔案
            with open(file_path, 'r') as file:
                json_content = file.read()
            
                
                # 解析 JSON
                try:
                    data = json.loads(json_content)
                    pose_3d_length = len(data.get("frame_pos3d", []))
                    
                    if "label" in data:
                        self.save_label = data["label"]
                    else:
                        self.save_label = "N/A"
                        print("No label in this json file")
                        
                        
                    min_frame_id = min(data.get("frame_pos3d", {}), key=int, default="N/A")
                    max_frame_id = max(data.get("frame_pos3d", {}), key=int, default="N/A")
                    
                    for category, keywords in categories.items():
                        if int(keywords) == int(self.save_label):
                            description = category
                            break
                
                    
                    # 更新 GUI 中的標籤、滑桿等
                    self.gui_instance.label_min_max_frame_id.setText(f'最小 frame id: {min_frame_id}\n最大 frame id: {max_frame_id}')
                    self.gui_instance.slider_min_frame_id.setMinimum(int(min_frame_id))
                    self.gui_instance.slider_min_frame_id.setMaximum(int(max_frame_id))
                    self.gui_instance.slider_min_frame_id.setValue(int(min_frame_id))
                    self.gui_instance.slider_max_frame_id.setMinimum(int(min_frame_id))
                    self.gui_instance.slider_max_frame_id.setMaximum(int(max_frame_id))
                    self.gui_instance.slider_max_frame_id.setValue(int(max_frame_id))
                    self.gui_instance.label_json_length.setText(f'["frame_pos3d"]的長度: {pose_3d_length}')
                    self.gui_instance.label_data_type.setText(f'JSON data type: {self.save_label}')
                    self.gui_instance.label_type_description.setText(f'Type Description: {description}')
                    self.data = data
                    self.filename = file_path.split('/')[-1]
                    self.gui_instance.label_selected_json.setText(f'選擇的JSON檔: {self.filename}')
                    
                except json.JSONDecodeError:
                    self.gui_instance.label_json_length.setText('JSON 解析錯誤')

    
        
    def plot_3d_points(self):
        if not hasattr(self, 'data') or 'frame_pos3d' not in self.data:
            self.gui_instance.label_json_length.setText('請先讀取 JSON 檔')
            return

        min_frame_id = self.gui_instance.slider_min_frame_id.value()
        max_frame_id = self.gui_instance.slider_max_frame_id.value()
        frame_pos3d = self.data['frame_pos3d']

        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        ax.set_xlim3d(left=0, right=9)
        ax.set_ylim3d(bottom=-1, top=19)
        ax.set_zlim3d(bottom=0, top=5)
        ax.view_init(elev=5, azim=195)

        

        for frame_id, points in frame_pos3d.items():
            if int(frame_id) >= min_frame_id and int(frame_id) <= max_frame_id:
                x, y, z = points
                ax.plot([x], [y], [z], color='b', marker='o')
                
        draw_volleyball_court(ax)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        
        ax.legend()
        plt.show()

    def update_min_frame_label(self):
        min_frame_id_value = self.gui_instance.slider_min_frame_id.value()
        self.gui_instance.label_min_frame_id_value.setText(f'最小 frame id: {min_frame_id_value}')    

    
    def update_max_frame_label(self):
        max_frame_id_value = self.gui_instance.slider_max_frame_id.value()
        self.gui_instance.label_max_frame_id_value.setText(f'最大 frame id: {max_frame_id_value}')
    
    def save_json(self):
        if not hasattr(self, 'data') or 'frame_pos3d' not in self.data:
            self.gui_instance.label_json_length.setText('請先讀取 JSON 檔')
            return

        min_frame_id = self.gui_instance.slider_min_frame_id.value()
        max_frame_id = self.gui_instance.slider_min_frame_id.maximum()
        frame_pos3d = self.data['frame_pos3d']

        # Create a new dictionary to store the adjusted data
        adjusted_data = {
            'frame_pos3d': {},
            'label': self.save_label
        }

        # Iterate through frames and store adjusted data
        for frame_id, points in frame_pos3d.items():
            if min_frame_id <= int(frame_id) <= max_frame_id:
                adjusted_data['frame_pos3d'][frame_id] = points

        save_folder_path = 'D:/Programming/Python/VTC/dataset'
        save_filename = self.filename
        save_file_path = os.path.join(save_folder_path, f'{self.save_label}', save_filename)

        if save_file_path:
            try:
                # Save the adjusted data to the new JSON file
                with open(save_file_path, 'w') as file:
                    json.dump(adjusted_data, file, indent=2)

                self.gui_instance.label_json_length.setText(f'已儲存至: {save_file_path}')
                print(f'已儲存至: {save_file_path}')
                plt.close("all")
            except Exception as e:
                self.gui_instance.label_json_length.setText(f'儲存失敗: {str(e)}')

                # Close the matplotlib figure
                plt.close()
    