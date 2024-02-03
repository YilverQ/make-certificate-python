#Importamos las librerías necesarias para trabajar
import csv #Para trabajar con archivos CSV.
from jinja2 import Environment, FileSystemLoader #Para trabajar con HTML.
import os #Nos servirá para indicar la carpeta donde se guardarán los PDF
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


#Cargamos los archivos de plantilla desde el directorio de plantilla
template_route = "./templates"
env = Environment(loader=FileSystemLoader(template_route))
template = env.get_template('template.html') #Obtenemos el archivo template.


#Lee los datos del archivo CSV y genera un certificado PDF para cada fila:
with open('Data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    number = 0 #Limite de generación
    folder_save = "" #Ruta donde se guardarán los archivos.
    font_config = FontConfiguration() #Configuración para trabajar con fuentes.


    for row in reader:
        #Este código es para prevenir que se ejecute varias veces el convertidor de pdf.
        if number == 1:
            break

        # Renderiza el template con los datos de la fila actual
        rendered_template = template.render(name=row['name'], 
                                            identification_card=row['identification_card'],
                                            modality=row['modality'],
                                            id=row['id'])
        
        #Indicamos la ruta y el nombre del certificado
        folder_save = os.path.join("Certificados", 
                                    f"{row['id']} - {row['identification_card']}.pdf")


        # Abre el archivo en modo de lectura
        file_css = open(template_route + f"/{row['modality']}.css", "r")
        # Lee el contenido del archivo
        styles_code = file_css.read()
        # Cierra el archivo
        file_css.close()
        css = CSS(string=styles_code, font_config=font_config)

        #Generamos un PDF a partir de un texto HTML.
        HTML(string=rendered_template).write_pdf(folder_save, 
                                                stylesheets=[css], 
                                                font_config=font_config)

        print(f"Documento: {row['identification_card']} Está listo")
        number += 1