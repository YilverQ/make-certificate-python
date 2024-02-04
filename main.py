#Importamos las librerías necesarias para trabajar
import csv #Para trabajar con archivos CSV.
from jinja2 import Environment, FileSystemLoader #Para trabajar con HTML.
import os #Nos servirá para indicar la carpeta donde se guardarán los PDF
from weasyprint import HTML, CSS #Nos permite generar HTML con estilos a PDF.
from weasyprint.text.fonts import FontConfiguration #Nos permite agreagar fuentes al momento de generar un PDF
from pdf2image import convert_from_path, convert_from_bytes #Convierte un PDF a imagen


#Cargamos los archivos de plantilla desde el directorio de plantilla
template_route = "./templates"
env = Environment(loader=FileSystemLoader(template_route))
template = env.get_template('template.html') #Obtenemos el archivo template.
font_config = FontConfiguration() #Configuración para trabajar con fuentes.

#Lee los datos del archivo CSV
with open('Data.csv') as csvfile:
    reader = csv.DictReader(csvfile) #Nos retorna un diccionario con los datos el archivo CSV.
    folder_save = "" #Ruta donde se guardarán los archivos.
    number = 0 #Numero formateado

    #Por cada línea leída nos va a generar un PDF.
    for row in reader:
        # Renderiza el template con los datos de la fila actual
        number = "{0:,}".format(int(row['identification_card'])).replace(",", ".")
        rendered_template = template.render(name=row['name'], 
                                            identification_card=number,
                                            modality=row['modality'],
                                            id=row['id'])
        
        #Indicamos la ruta y el nombre del certificado
        nameFile = f"{row['id']} - {row['identification_card']}.png"
        folder_save = os.path.join("Certificados", nameFile) #Combina nos rutas, en este caso combina una ruta con el nombre del archivo.

        # Abre el archivo en modo de lectura
        file_css = open(template_route + f"/{row['model']}" + f"/{row['modality']}.css", "r")
        # Lee el contenido del archivo
        styles_code = file_css.read()
        # Cierra el archivo
        file_css.close()
        css = CSS(string=styles_code, font_config=font_config)

        #Generamos un PDF a partir de un texto HTML.
        pdf_file = HTML(string=rendered_template).write_pdf(stylesheets=[css], 
                                                            font_config=font_config)

        imagenes = convert_from_bytes(pdf_file)
        imagenes[0].save(folder_save, "PNG")

        #Imprimimos un progreso.
        print(template_route + f"/{row['model']}" + f"/{row['modality']}.css")
        print(f"Certificado: {row['id']} - {row['identification_card']} Está listo")


