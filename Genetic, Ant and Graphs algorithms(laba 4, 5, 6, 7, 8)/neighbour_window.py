from template import EditableSpinbox, EditableCombobox
from body import WidgetTemp

def Neighbor_Window(frame_neighbor):
    # Создание скелета окна
    WTemp = WidgetTemp(root=frame_neighbor, main_title="Метод близьлежайшнго соседа", img_title="Граф",
                       table_title="Таблица рёбер", algorithm="neighborhood_algorithm")
    WTemp.pack(padx=5, pady=5)