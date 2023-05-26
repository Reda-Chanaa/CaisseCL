from datetime import datetime
import pandas as pd
from django.http import HttpResponse


def Prepaye(df1):

    df1["res_type"] = df1["res_type"].str.strip()
    df1["armateur"] = df1["armateur"].str.strip()
    df1["reseau"] = df1["reseau"].str.strip()
    df1["code_navire"] = df1["code_navire"].str.strip()
    df1["port_depart"] = df1["port_depart"].str.strip()
    df1["port_arrivee"] = df1["port_arrivee"].str.strip()
    
    Groupe = df1[(df1['res_type'].str.contains('GROUPE', na=False))]      
    print("Groupe",len(Groupe))
    
    MenuGroupe = Groupe[(Groupe["code_addon"].str.contains("MENU GROUPE", na=False))]      
    print("MenuGroupe",len(MenuGroupe))

    # Apply the assign_color function to create the new column
    MenuGroupe['SEUIL'] = MenuGroupe.apply(assign_color, axis=1)
    return MenuGroupe

def assign_color(row):
    nb = row['nb_pax_addon']
    line = row['code_navire']

    if ((line == 'GOTA' and nb < 100 and nb >= 50)
      or (line == 'BABU' and nb < 80 and nb >= 40)
      or (line == 'MORO' and nb < 80 and nb >= 40)
      or (line == 'ORBA' and nb < 80 and nb >= 40)
      or (line == 'NEPI' and nb < 70 and nb >= 35)
      or (line == 'VONA' and nb < 40 and nb >= 20)):
        return 'ORANGE'
    elif ((line == 'GOTA' and nb < 50)
      or (line == 'BABU' and nb < 40)
      or (line == 'MORO' and nb < 40)
      or (line == 'ORBA' and nb < 40)
      or (line == 'NEPI' and nb < 35)
      or (line == 'VONA' and nb < 20)):
        return 'VERT'
    else:
        return 'ROUGE'

def prep(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        
        df1 = pd.read_csv(File1, delimiter=';')

        print(len(df1))

        # Journal
        data = Prepaye(df1)

        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))