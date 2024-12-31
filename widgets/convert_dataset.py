import os

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QWidget,
    QFileDialog,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QCheckBox,
    QLineEdit,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
)

from widgets.convert_run import ConvertWork


class DataSetConvert(QWidget):
    signal_start_or_stop_convert = Signal(bool, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.convert_progress = None
        self.adjust_point = None
        self.in_dataset_list = QListWidget(self)
        self.input_label_item = None
        self.out_dataset_list = QListWidget(self)
        self.output_label_item = None

        self._set_in_dataset_list_items()
        self._set_out_dataset_list_items()

        self.input_label = None
        self.output_label = None
        self.output_edit = None
        self.convert_button = None
        self.work_thread = None

        self.init_ui()
        self.connect_signal()

    def init_ui(self):
        self.convert_progress = QProgressBar(self)

        group_box = QGroupBox(self.tr("DataSet List"), self)
        self.adjust_point = QCheckBox(self.tr("point 조정"), self)
        self.adjust_point.setChecked(True)
        self.input_label = QLabel(self.tr("Input 라벨"), self)
        self.output_label = QLabel(self.tr("Convert 라벨"), self)

        in_h_layout = QHBoxLayout()
        in_h_layout.addWidget(self.input_label)
        in_h_layout.addWidget(self.in_dataset_list)

        out_h_layout = QHBoxLayout()
        out_h_layout.addWidget(self.output_label)
        out_h_layout.addWidget(self.out_dataset_list)

        self.convert_button = QPushButton(self.tr("변환"), self)

        v_layout_sub = QVBoxLayout()
        v_layout_sub.addLayout(in_h_layout)
        v_layout_sub.addLayout(out_h_layout)
        v_layout_sub.addWidget(self.adjust_point)
        v_layout_sub.addWidget(self.convert_button)
        group_box.setLayout(v_layout_sub)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.convert_progress)
        v_layout.addWidget(group_box)

        self.setLayout(v_layout)

    def _set_in_dataset_list_items(self):
        QListWidgetItem(self.tr("labelme"), self.in_dataset_list)
        QListWidgetItem(self.tr("voc"), self.in_dataset_list)
        QListWidgetItem(self.tr("ade20k"), self.in_dataset_list)
        QListWidgetItem(self.tr("coco"), self.in_dataset_list)

    def _set_out_dataset_list_items(self):
        QListWidgetItem(self.tr("labelme"), self.out_dataset_list)
        QListWidgetItem(self.tr("voc"), self.out_dataset_list)
        QListWidgetItem(self.tr("ade20k"), self.out_dataset_list)
        QListWidgetItem(self.tr("coco"), self.out_dataset_list)

    def connect_signal(self):
        self.convert_button.clicked.connect(self.on_click_convert_button)
        self.signal_start_or_stop_convert.connect(self.on_start_or_stop_convert)

    def on_click_convert_button(self):

        if (
            self.in_dataset_list.currentItem() is None
            or self.out_dataset_list.currentItem() is None
        ):
            self.show_not_selected_dataset()
            return

        if (
            self.in_dataset_list.currentItem().text()
            == self.out_dataset_list.currentItem().text()
        ):
            self.show_same_dataset()
            return

        file_path = QFileDialog.getExistingDirectory(
            self,
            self.tr("Select directory"),
            os.getenv("HOME"),
            QFileDialog.ShowDirsOnly,
        )
        self.signal_start_or_stop_convert.emit(True, file_path)

    def _init_work(self):
        self.convert_progress.reset()
        self.convert_button.setEnabled(True)

    def _set_work(self):
        self.convert_button.setEnabled(False)
        self.convert_progress.setValue(0)

    @Slot(bool, str, str)
    def on_start_or_stop_convert(self, start, data):
        if start:
            self.start_convert(data)
        else:
            self.stop_convert(data)

    @Slot(int)
    def on_update_progress(self, value):
        self.convert_progress.setValue(value)
        self.update()

    def start_convert(self, file_path):

        if file_path is None or file_path.strip() == "":
            self.show_critical_wrong_path(file_path)
            return

        self._set_work()

        if self.work_thread is not None and self.work_thread.isRunning():
            self.work_thread.quit()
            self.work_thread.wait(5)

        self.input_label_item = self.in_dataset_list.currentItem().text()
        self.output_label_item = self.out_dataset_list.currentItem().text()

        self.work_thread = ConvertWork(self)
        self.work_thread.signal_update_progress.connect(self.on_update_progress)
        self.work_thread.set_signal(self.signal_start_or_stop_convert)
        self.work_thread.set_file_path(file_path)
        self.work_thread.set_input_label(self.input_label_item)
        self.work_thread.set_output_label(self.output_label_item)
        self.work_thread.set_adjust_point(self.adjust_point)
        self.work_thread.set_file_path(file_path)
        self.work_thread.start()

    def stop_convert(self, reason):
        if reason is not None and reason != "":
            self.show_critical_fail_convert(reason)
        else:
            self.show_info_success()
        self._init_work()

    def show_critical_wrong_setting(self):
        _ = QMessageBox.critical(
            self,
            self.tr("Wrong setting."),
            self.tr(f'If "모두 병합" is checked, "출력 라벨" should be set!'),
            QMessageBox.Ok,
        )

    def show_critical_wrong_path(self, file_path):
        _ = QMessageBox.critical(
            self,
            self.tr("Invalid Path."),
            self.tr(f"The path({file_path}) is wrong!"),
            QMessageBox.Ok,
        )

    def show_not_selected_dataset(self):
        _ = QMessageBox.critical(
            self,
            self.tr("Please select Dataset..."),
            self.tr("Please select Dataset!!"),
            QMessageBox.Ok,
        )

    def show_same_dataset(self):
        _ = QMessageBox.critical(
            self,
            self.tr("Please Different Dataset..."),
            self.tr(
                f"Please Different Dataset...!!\n"
                f"input : {self.in_dataset_list.currentItem().text()}\n"
                f"output : {self.out_dataset_list.currentItem().text()}"
            ),
            QMessageBox.Ok,
        )

    def show_critical_fail_convert(self, reason):
        _ = QMessageBox.critical(
            self, self.tr("Fail Convert!"), self.tr(reason), QMessageBox.Ok
        )

    def show_info_success(self):
        _ = QMessageBox.information(
            self,
            self.tr("Success Convert!"),
            self.tr("A converting work is ended successfully."),
            QMessageBox.Ok,
        )
