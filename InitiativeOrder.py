import StatHandler
import PySimpleGUI as sg

sg.theme('DarkAmber') 

title = sg.Text('Initiative Tracker',expand_x=True, justification="center")
current_initiative_display = sg.Text("Current initiative: {}".format(0))
next_initiative = sg.Button("Next Initiative")
prev_initiative = sg.Button("Previous Initiative")
initiative_table = sg.Table([],["Id","Name","Initiative"],num_rows=1,expand_x=True,expand_y=True, justification="center", enable_click_events=True)
add_button = sg.Button("Add",expand_x=True)
change_button = sg.Button('Change',expand_x=True)
check_button = sg.Button("Check" ,expand_x=True)
delete_button = sg.Button('Delete',expand_x=True)

entry_stats = [] 
avalible_initiatives = []
current_initiative = 0

def make_id():
    id = 0
    for x in initiative_table.get():
        if x[0] == id:
            id += 1
    return id

def update_initiatives():
    avalible_initiatives.clear()
    for x in initiative_table.get():
        avalible_initiatives.append(x[2])

#Adds a charater to the table
def add_char_sheet(file_path):
    current = initiative_table.get()
    
    id = make_id()
    current.append([id,StatHandler.get_char_from_pdf(file_path)["Name"],0])
    initiative_table.update(current)

    entry_stats.insert(id,StatHandler.get_char_from_pdf(file_path))
    update_initiatives()

def get_initiative(e):
    return e[2]

def add_custom():
    #Creates a new menu to handle addin custom creatures
    load_button = sg.Button("Load")
    delete_button = sg.Button("Delete")
    new_button = sg.Button("New")

    #Gets avalible creatures from the SavedCreatures text file and sorts by assending id
    creatures = StatHandler.get_from_text("SavedCreatures.txt")
    #Extracts the avalible id's and names
    names = []
    i = 0
    for x in creatures:
        names.append([i,x["Name"]])
        i +=1

    #Creates a table of id's and names
    creatures_table = sg.Table(names,["Id","Name"])

    #Creates and opens the custom creatures window
    custom_window = sg.Window("Stats",[[sg.Text("Custom Creatures")],[creatures_table],[load_button,delete_button,new_button]], size=(1000,250))

    #Handles the avalible inputs
    while True:
        event,values = custom_window.read()
        if event == sg.WIN_CLOSED:
            return
        if event == "Load":
            selected_creature = creatures[int(creatures_table.get()[creatures_table.SelectedRows[0]][0])]
            id = make_id()

            init_contents = initiative_table.get()

            init_contents.append([id,selected_creature["Name"],0])
            initiative_table.update(init_contents)
            print(id)
            entry_stats.insert(id,selected_creature)
            update_initiatives()

        if event == "Delete":
            selected_id = int(creatures_table.get()[creatures_table.SelectedRows[0]][0])
            StatHandler.delete_from_file("SavedCreatures.txt",[selected_id])

            creatures_table_data = creatures_table.get()

            creatures_table_data.pop(selected_id)
            creatures_table.update(creatures_table_data)
            creatures.pop(selected_id)


        print(event)

#Changes the initative of the selected entry and sorts the list
def change_initiative(raw):
    selection = initiative_table.SelectedRows[0]
    current = initiative_table.get()
    selection_id = current[selection][0]

    if raw == "Yes":
        roll = int(sg.popup_get_text("Please type the roll")) + entry_stats[selection_id]["Initiative"]
    else:
        roll = int(sg.popup_get_text("Please enter the initative"))

    current[selection][2]= roll
    current.sort(reverse=True,key=get_initiative)
    initiative_table.update(current)
    update_initiatives()

#Removes entries from both initative table and entry stats
def delete_entry(confirm):
    if confirm == "No":
        return
    selection = initiative_table.SelectedRows[0]
    current = initiative_table.get()
    selection_id = current[selection][0]

    current.pop(selection)
    entry_stats.pop(selection_id)

    initiative_table.update(current)
    update_initiatives()

#Displays the stats of the selected unit
def display_info_window(selection):
    selection_stats = entry_stats[selection[0]]
    
    stats_table_values = []
    for x in selection_stats["Stats"]:
        stats_table_values.append([x.replace("'",""),selection_stats["Stats"][x]])

    stats_table = sg.Table(stats_table_values,["Name","Value"],num_rows=10,expand_x=True,expand_y=True, justification="center", enable_click_events=True)

    skills_table_values = []
    for x in selection_stats["Skills"]:
        skills_table_values.append([x.replace("'",""),selection_stats["Skills"][x]])

    skills_table = sg.Table(skills_table_values,["Name","Value"],num_rows=10,expand_x=True,expand_y=True, justification="center", enable_click_events=True)

    pasives_table_values = []
    for x in selection_stats["Pasive Stats"]:
        pasives_table_values.append([x.replace("'",""),selection_stats["Pasive Stats"][x]])

    pasives_table_values = sg.Table(pasives_table_values,["Name","Value"],num_rows=10,expand_x=True,expand_y=True, justification="center", enable_click_events=True)

    other_stats = sg.Frame("Other", [[sg.Text("Initiative: {}".format(selection_stats["Initiative"]))],[sg.Text("AC: {}".format(selection_stats["AC"]))],[sg.Text("Speed: {}".format(selection_stats["Speed"]))]])

    info_window = sg.Window("Stats",[[sg.Text("{} Stats".format(selection_stats["Name"]))],[stats_table,skills_table,pasives_table_values,other_stats]], size=(1000,250))
    info_window.read()

    

layout = [  [title],
            [current_initiative_display,next_initiative,prev_initiative],
            [initiative_table],
            [add_button,delete_button,check_button,change_button] ]

window = sg.Window('Initiative Tracker', layout=layout, size=(1000,500) )

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

    if event == "Add":
        try:
            option = sg.popup_yes_no("Add from dnd beyond pdf?")
            if option == "Yes":
                add_char_sheet(sg.popup_get_file("Please select a character sheet pdf."))
            else:
                add_custom()
        except Exception as e:
            sg.popup_error("Something went wrong",title="Oops")
            print("error: ",e)
    
    if event == "Delete":
        try:
            delete_entry(sg.popup_yes_no("Are you sure you want to delete {}?".format(initiative_table.get()[initiative_table.SelectedRows[0]][1])))
        except Exception as e:
            print("Error : ", e)

    if event == "Change":
        try:
            change_initiative(sg.popup_yes_no("Would you like to add initiative bonus?"))
        except Exception as e:
            print("error: ", e)
    
    if event == "Check":
        try:
            display_info_window(initiative_table.SelectedRows)
        except Exception as e:
            print("Error: ",e)
    
    if event == "Next Initiative":
        if len(avalible_initiatives) < 1:
            continue
        current_initiative = (current_initiative+1)%len(avalible_initiatives)
        try:
            current_initiative_display.update("Current initiative: {}".format(avalible_initiatives[current_initiative]))
        except:
            print("Error")
    
    if event == "Previous Initiative":
        if len(avalible_initiatives) < 1:
            continue
        current_initiative = (current_initiative-1)%len(avalible_initiatives)
        try:
            current_initiative_display.update("Current initiative: {}".format(avalible_initiatives[current_initiative]))
        except:
            print("Error")

        

window.close()