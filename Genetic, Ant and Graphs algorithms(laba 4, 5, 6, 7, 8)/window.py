from template import EditableSpinbox, EditableCombobox
from body import WidgetTemp


def Genetic_Window(frame_genetic):
    # Создание окна
    WTemp = WidgetTemp(root=frame_genetic, main_title="Параметры:", img_title="Хромосмы выбранного поколения",
                       table_title="Лучшие гены поколения", algorithm="genetic_algorithm")

    EditableSpinbox(text="Колличество хромосом:", initial_value="10", check_index=0,
                    from_=2, to=999, increment=1, frame=WTemp.frame_input, name='numberOfIndividuals').pack()
    EditableSpinbox(text="Колличесво поколени:", initial_value="10", check_index=0,
                    from_=1, to=999, increment=1, frame=WTemp.frame_input, name='numberGeneration').pack()
    EditableSpinbox(text="Колличесво прошлых поколений:", initial_value="10", check_index=0,
                    from_=1, to=999, increment=1, frame=WTemp.frame_input, name='mutationSteps').pack()
    EditableSpinbox(text="Какая доля популяции должна производить потомство:", initial_value="1", check_index=2,
                   from_=0.01, to=1, increment=1, frame=WTemp.frame_input, name='crossoverRate').pack_forget()
    EditableSpinbox(text="Шанс мутации :", initial_value="0.5", check_index=2,
                    from_=0.01, to=1, increment=0.01, frame=WTemp.frame_input, name='chanceMutations').pack()
    EditableSpinbox(text="Минимальное значение гена:", initial_value="-5", check_index=1,
                    from_=-99999, to=99999, increment=1, frame=WTemp.frame_input, name='start').pack()
    EditableSpinbox(text="Максимальное значение гена:", initial_value="5", check_index=1,
                    from_=-99999, to=99999, increment=1, frame=WTemp.frame_input, name='end').pack()

    EditableCombobox(WTemp.frame_input, text="Функция:", name='func').pack()
    WTemp.pack(padx=5, pady=5)

