import dearpygui.dearpygui as dpg


lencolumn = 3
lenrow = 16
opcdcmdatainput = [[0 for i in range(lencolumn)] for i in range(lenrow)]
list_of_items = ["A", "B", "C", "D", "E", "F", "G", "H"]
items2 = ("I", "J", "K", "L", "M", "N", "O", "P")
items3 = ("Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=300)


def myfunprint(sender, data, user_data):
    global opcdcmdatainput
    global list_of_items, rowidx

    if user_data[0] == 1:
        opcdcmdatainput[user_data[1]][0] = f'//To co Mariusz chce {data}'
        list_of_items.remove(data)
        print(f'items w funkcji {list_of_items}')
        for i in range(lenrow):
            dpg.configure_item(121+i, items=list_of_items)
    elif user_data[0] == 2:
        opcdcmdatainput[user_data[1]][1] = data
    elif user_data[0] == 3:
        opcdcmdatainput[user_data[1]][2] = data
    print(user_data)
    print(f"Kolumna {user_data[0]} Wiersz {user_data[1]}: {data}")
    print(opcdcmdatainput)
    return


def myfunfilegenerate(sender, data):
    global opcdcmdatainput
    print(f"Generacja plików")
    with open('readme.txt', 'w') as f:
        for i in range(lencolumn):
                f.writelines(str(opcdcmdatainput[i]) + '\n')
    f.close()


with dpg.window(label="OPCDCM Configurator", tag="Primary Window"):
    dpg.add_text("Test version")
    dpg.add_button(label="Generate files", callback=myfunfilegenerate)

    with dpg.table(width=780, header_row=True, row_background=True,
                   borders_innerH=True, borders_outerH=True, borders_innerV=True,
                   borders_outerV=True, delay_search=True, resizable=True) as table_id:
        dpg.add_table_column(label="Signal number")
        dpg.add_table_column(label="Signal tag", width=200)
        dpg.add_table_column(label="UserDatagApp", width=200)
        dpg.add_table_column(label="Header 3", width=200)

        for i in range(lenrow):
            with dpg.table_row():
                dpg.add_text(i)
                dpg.add_combo(tag=121+i, items=list_of_items, height_mode=dpg.mvComboHeight_Small, no_arrow_button=False,
                              no_preview=False, popup_align_left=True, callback=myfunprint, user_data=[1, i])
                dpg.add_combo(tag=221+i, items=items2, height_mode=dpg.mvComboHeight_Small, no_arrow_button=False,
                                         no_preview=False, popup_align_left=True, callback=myfunprint, user_data=[2, i])
                dpg.add_combo(tag=321+i, items=items3, height_mode=dpg.mvComboHeight_Small, no_arrow_button=False,
                                         no_preview=False, popup_align_left=True, callback=myfunprint, user_data=[3, i])

dpg.create_viewport(title='Custom Title', width=790, height=500)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
