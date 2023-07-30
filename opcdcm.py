import dearpygui.dearpygui as dpg
from Variable import list_of_variable
from VariableNaming import list_of_variable_naming
from LogDataConf import list_log_data_conf

error = 0
lencolumn = 3
lenrow = 22
opcdcmdatainput = [[0 for i in range(lencolumn)] for i in range(lenrow)]
list_of_variable_mapping = list_of_variable_naming

items2 = [i for i in range(4)]
items3 = ("Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")

dpg.create_context()
dpg.create_viewport(title='OPCDCM config generator', width=600, height=300)


def myfunprint(sender, data, user_data):
    global opcdcmdatainput
    global list_of_variable_mapping, rowidx

    if user_data[0] == 1:
        opcdcmdatainput[user_data[1]][2] = list_of_variable_naming.index(data)
        opcdcmdatainput[user_data[1]][0] = f'{data}'
        #list_of_variable_mapping.remove(data)
        #list_of_variable_mapping = [x for x in list_of_variable_mapping if x != data]
        print(f'list_of_variable_mapping {list_of_variable_mapping}')
        print(f"list_of_variable {list_of_variable_naming}")
        for i in range(lenrow):
            dpg.configure_item(121+i, items=list_of_variable_mapping)
    elif user_data[0] == 2:
        opcdcmdatainput[user_data[1]][1] = data
    #elif user_data[0] == 3:
    #    opcdcmdatainput[user_data[1]][2] = data
    print(user_data)
    print(f"Kolumna {user_data[0]} Wiersz {user_data[1]}: {data}")
    print(opcdcmdatainput)


def myfunfilegenerate(sender, data):
    global opcdcmdatainput
    print(f"Generacja plików")
    global error
    with open('Initialize.txt', 'w') as f:
        f.write(f"//*********************************// \n")
        f.write(f"//*** Names for UserDataLogging ***// \n")
        f.write(f"//*********************************// \n")
        f.write(f"\n")
        for i in range(lenrow):
            if opcdcmdatainput[i][0] != 0:
                temp = list_of_variable[opcdcmdatainput[i][2]]
                temp = temp.replace("?", opcdcmdatainput[i][1])
                f.writelines(f"// Naming for the {temp} \n")
                temp = opcdcmdatainput[i][0]
                for k in range(16):
                    if k < len(temp):
                        if temp[k] != "?":
                            f.writelines({f"UserDataLoggingColumnName100ms[{i}].DATA[{k}] := {ord(temp[k])} \n"})
                        else:
                            f.writelines(
                                {f"UserDataLoggingColumnName100ms[{i}].DATA[{k}] := {ord(opcdcmdatainput[i][1])} \n"})
                    else:
                        f.writelines({f"UserDataLoggingColumnName100ms[{i}].DATA[{k}] := 32 \n"})
                f.writelines({f"UserDataLoggingColumnName100ms[{i}].LEN := 16; \n\n"})
            else:
                f.writelines(f"Pusto \n\n")
    f.close()

    #UserTask_LogData file creation
    with open('UserTask1_LogData.txt', 'w') as f:
        for i in range(lenrow):
            if opcdcmdatainput[i][0] != 0:
                tempp = opcdcmdatainput[i][2]
                temp = list_of_variable[opcdcmdatainput[i][2]]
                temp = temp.replace("?", opcdcmdatainput[i][1])
                if list_log_data_conf[tempp][0] == '0':
                    f.writelines(f"//----------------------------------------------------------------------------------------------------------------------------------- \n")
                    opcdcmdatainput[i][0] = opcdcmdatainput[i][0].replace("?", opcdcmdatainput[i][1])
                    f.writelines(f"//{opcdcmdatainput[i][0]} \n")
                    f.writelines(f"UserDataLogBuffer100ms[{i}] := {temp}; \n\n")
                else:
                    f.writelines(f"//----------------------------------------------------------------------------------------------------------------------------------- \n")
                    opcdcmdatainput[i][0] = opcdcmdatainput[i][0].replace("?", opcdcmdatainput[i][1])
                    f.writelines(f"//{opcdcmdatainput[i][0]} \n")
                    f.writelines(f"If {temp} Then\n")
                    #print(f" wiersz {i}")
                    #print(f" log_data_conf {list_log_data_conf[i][2]}")
                    f.writelines(f"\t UserDataLogBuffer100ms[{i}] := {list_log_data_conf[tempp][2]}; \n")
                    f.writelines(f"Else \n")
                    f.writelines(f"\t UserDataLogBuffer100ms[{i}] := {list_log_data_conf[tempp][4]}; \n\n")
                    f.writelines(f"end_if; \n\n")
            else:
                f.writelines(f"//----------------------------------------------------------------------------------------------------------------------------------- \n")
                f.writelines(f"//Not defined \n")
                f.writelines(f"UserDataLogBuffer100ms[{i}] := 0; \n\n")
    f.close()


with dpg.window(label="OPCDCM Configurator", tag="Primary Window"):

    with dpg.table(width=780, header_row=True, row_background=True,
                   borders_innerH=True, borders_outerH=True, borders_innerV=True,
                   borders_outerV=True, delay_search=True, resizable=True) as table_id:
        dpg.add_table_column(label="Signal number")
        dpg.add_table_column(label="Signal tag", width=200)
        dpg.add_table_column(label="Loop No", width=200)

        for i in range(lenrow):
            with dpg.table_row():
                dpg.add_text(i)
                dpg.add_combo(tag=121+i, items=list_of_variable_mapping, height_mode=dpg.mvComboHeight_Small, no_arrow_button=False,
                              no_preview=False, popup_align_left=True, callback=myfunprint, user_data=[1, i])
                dpg.add_combo(tag=221+i, items=items2, height_mode=dpg.mvComboHeight_Small, no_arrow_button=False,
                                         no_preview=False, popup_align_left=True, callback=myfunprint, user_data=[2, i])

    dpg.add_button(label="Generate files", tag="GenFile", pos=(280, 540), width=200, height=30, callback=myfunfilegenerate)
    dpg.add_text("Test version", pos=(340, 590), color=[255, 0, 0])
    with dpg.popup(parent="GenFile", tag="GenInfo", mousebutton=0, modal=True):
        if error ==0:
            dpg.add_text("Files generated with success")
            dpg.add_button(label="Ok", callback=lambda: dpg.configure_item("GenInfo", show=False))
        else:
            dpg.add_text("Files generation failed")


dpg.create_viewport(title='OPCDCM Configurator', width=790, height=660)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
