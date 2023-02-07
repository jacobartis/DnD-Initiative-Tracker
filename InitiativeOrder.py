import StatHandler
import PySimpleGUI as sg

sg.theme('DarkAmber') 

title = sg.Text('Initiative Tracker')
initiative_table = sg.Table([],["Id","Name","Initiative"],num_rows=1,expand_x=True,expand_y=True, justification="center", enable_click_events=True)
add_button = sg.Button("Add",expand_x=True)
change_button = sg.Button('Change',expand_x=True)
delete_button = sg.Button('Delete',expand_x=True)

entry_stats = [] 

#Adds a charater to the table
def add_char_sheet(file_path):
    current = initiative_table.get()
    id = len(current)
    current.append([id,StatHandler.get_char_from_pdf(file_path)["Name"],0])
    initiative_table.update(current)

    entry_stats.insert(id,StatHandler.get_char_from_pdf(file_path))

def get_initiative(e):
    return e[2]

#Changes the initative of the selected entry and sorts the list
def change_initative(roll):
    selection = initiative_table.SelectedRows[0]
    current = initiative_table.get()
    selection_id = current[selection][0]

    current[selection][2]= int(roll) + entry_stats[selection_id]["Initiative"]
    current.sort(reverse=True,key=get_initiative)
    initiative_table.update(current)


#def add_character(name:int):
#    window.extend_layout([[sg.Text(name),sg.Input(size=(3,1), pad=(0,0))]],[[1]])


#add_character("epic")
#add_character("steve")

layout = [  [title],
            [initiative_table],
            [add_button,delete_button,change_button] ]

window = sg.Window('Window Title', layout=layout, size=(1000,800) )

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == "Add":
        try:
            add_char_sheet(sg.popup_get_file("Please select a character sheet pdf."))
        except Exception as e:
            sg.popup_error("Something went wrong",title="Oops")
            print("error: ",e)
    
    if event == "Change":
        try:
            change_initative(sg.popup_get_text("Please type the roll"))
        except Exception as e:
            print("error: ", e)
        

window.close()