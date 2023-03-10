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

def create_menu():
    name_text = sg.Text("Name:")
    name_input = sg.Input()

    str_text = sg.Text("Str: ",expand_x=True)
    str_input = sg.Spin([-5,-4,-3,-2,-1,0,1,2,3,4,5],initial_value=0,expand_x=True)
    dex_text = sg.Text("Dex: ",expand_x=True)
    dex_input = sg.Spin([-5,-4,-3,-2,-1,0,1,2,3,4,5],initial_value=0,expand_x=True)
    con_text = sg.Text("Con: ",expand_x=True)
    con_input = sg.Spin([-5,-4,-3,-2,-1,0,1,2,3,4,5],initial_value=0,expand_x=True)
    int_text = sg.Text("Int: ",expand_x=True)
    int_input = sg.Spin([-5,-4,-3,-2,-1,0,1,2,3,4,5],initial_value=0,expand_x=True)
    wis_text = sg.Text("Wis: ",expand_x=True)
    wis_input = sg.Spin([-5,-4,-3,-2,-1,0,1,2,3,4,5],initial_value=0,expand_x=True)
    cha_text = sg.Text("Cha: ",expand_x=True)
    cha_input = sg.Spin([-5,-4,-3,-2,-1,0,1,2,3,4,5],initial_value=0,expand_x=True)
    stats_frame = sg.Frame("Stats",[[str_text,str_input],[dex_text,dex_input],[con_text,con_input],[int_text,int_input],[wis_text,wis_input],[cha_text,cha_input]])

    ac_text = sg.Text("AC: ",expand_x=True)
    ac_input = sg.Spin(list(range(101)),initial_value=0,expand_x=True)

    initiative_text = sg.Text("Initiative bonus: ",expand_x=True)
    initiative_input = sg.Spin(list(range(-100,101)),initial_value=0,expand_x=True)

    other_stats_frame = sg.Frame("Other Stats",[[ac_text,ac_input],[initiative_text,initiative_input]])

    pasive_perception_text = sg.Text("Pas Perception: ",expand_x=True)
    pasive_perception_input = sg.Spin(list(range(31)),initial_value=10,expand_x=True)
    pasive_insight_text = sg.Text("Pas Insight: ",expand_x=True)
    pasive_insight_input = sg.Spin(list(range(31)),initial_value=10,expand_x=True)
    pasive_investigation_text = sg.Text("Pas Investigation: ",expand_x=True)
    pasive_investigation_input = sg.Spin(list(range(31)),initial_value=10,expand_x=True)
    pasive_stats_frame = sg.Frame("Pasive Stats",[[pasive_perception_text,pasive_perception_input],[pasive_insight_text,pasive_insight_input],[pasive_investigation_text,pasive_investigation_input]])

    create_button = sg.Button("Create")

    create_window = sg.Window("Stats",[[sg.Text("Create Creature",justification="center")],[name_text,name_input],[stats_frame,other_stats_frame,pasive_stats_frame],[create_button]], size=(440,300))

    while True:
        event,values = create_window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "Create":
            stats = {"Str":values[1],"Dex":values[2],"Con":values[3],"Int":values[2],"Wis":values[3],"Cha":values[4]}
            pas_stats = {"Pasive Perception":values[9],"Pasive Insight":values[10],"Pasive Investigation":values[11]}
            StatHandler.add_to_file("SavedCreatures.txt",[values[0],stats,[],[],pas_stats,"",values[8],values[7],""])
            break
    
    create_window.close()
    



def add_custom():
    #Creates a new menu to handle addin custom creatures
    load_button = sg.Button("Load",expand_x=True)
    delete_button = sg.Button("Delete",expand_x=True)
    new_button = sg.Button("New",expand_x=True)

    #Gets avalible creatures from the SavedCreatures text file and sorts by assending id
    creatures = StatHandler.get_from_text("SavedCreatures.txt")
    #Extracts the avalible id's and names
    names = []
    i = 0
    for x in creatures:
        names.append([i,x["Name"]])
        i +=1

    #Creates a table of id's and names
    creatures_table = sg.Table(names,["Id","Name"],expand_x=True)

    #Creates and opens the custom creatures window
    custom_window = sg.Window("Stats",[[sg.Text("Custom Creatures")],[creatures_table],[load_button,delete_button,new_button]], size=(250,250))

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

        if event == "New":
            create_menu()
            creatures = StatHandler.get_from_text("SavedCreatures.txt")
            #Extracts the avalible id's and names
            names = []
            i = 0
            for x in creatures:
                names.append([i,x["Name"]])
                i +=1
            creatures_table.update(names)

        print(event)

#Changes the initative of the selected entry and sorts the list
def change_initiative(raw):
    selection = initiative_table.SelectedRows[0]
    current = initiative_table.get()
    selection_id = current[selection][0]
    if raw == "Yes":
        roll = int(sg.popup_get_text("Please type the roll")) + int(entry_stats[selection_id]["Initiative"])
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
    print(initiative_table.get()[selection][0])
    selection_stats = entry_stats[initiative_table.get()[selection][0]]
    
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
            display_info_window(initiative_table.SelectedRows[0])
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