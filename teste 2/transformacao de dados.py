import tabula, os
import pandas as pd
from zipfile import ZipFile,ZIP_DEFLATED

def get_data_from_PDF(file_path:str):
    tabelas = tabula.read_pdf(
        file_path, 
        lattice = True, 
        pages = "3-180", 
        area = (64.89, 41.895, 555.03, 966.735)
    )
    
    return tabelas

def concatenate_data_frames(data_frames):
    data_frame1 = data_frames[0]
    data_frame2 = data_frames[1]

    final_data_frame = pd.concat([data_frame1, data_frame2])

    for data_frame in data_frames[2:]:
        final_data_frame = pd.concat([final_data_frame, data_frame])

    final_data_frame.drop(
        final_data_frame.columns[len(final_data_frame.columns)-1], 
        axis=1, 
        inplace=True
    )

    return final_data_frame

def replace_data_frame_columns_name(data_frame):
    data_frame.rename(columns = {"OD":"Seg. Odontológica"}, inplace = True)
    data_frame.rename(columns = {"AMB":"Seg. Ambulatorial"}, inplace = True)
    data_frame.replace("OD", "Seg. Odontológica", inplace = True)
    data_frame.replace("AMB", "Seg. Ambulatorial", inplace = True)

def data_frame_to_csv(data_frame):
    data_frame.to_csv(f"csv/tabelas.csv", index = False)

def zip_folder(zip_name, zipped_folder):
    with ZipFile(zip_name, "w", ZIP_DEFLATED) as zip_object:
        for folder_name, sub_folders, file_names in os.walk(zipped_folder):
            for filename in file_names:
                file_path = os.path.join(folder_name, filename)
                zip_object.write(file_path, os.path.basename(file_path))
    

dados_do_pdf = get_data_from_PDF("anexo/Anexo_I_Rol_2021RN_465.2021_RN592.pdf")
tabelas_do_pdf = concatenate_data_frames(dados_do_pdf)
replace_data_frame_columns_name(tabelas_do_pdf)
data_frame_to_csv(tabelas_do_pdf)
zip_folder(os.getcwd() + "/Teste_Henrique_Loureiro_de_Faria.zip", os.getcwd() + "/csv")