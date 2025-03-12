from docx import Document

# Paso 1: Generar el contenido con el LLM (esto es un ejemplo)
contenido = """
# Escrito Simple

**H. JUZGADO QUINTO FAMILIAR**  
**CON RESIDENCIA EN CD. ALTAMIRA, TAMAULIPAS**  

**ASUNTO:** Solicitud de autorización para acceso al expediente y medios electrónicos del tribunal.  

**EXPEDIENTE:** [Número de expediente, si aplica]  

**C. JUEZ(A) EN TURNO:**  

Por medio del presente escrito y en mi carácter de abogado patrocinante, con cédula profesional número **10761923**, me permito solicitar de manera respetuosa lo siguiente:  

1. **Autorización para acceso al expediente:**  
   Con fundamento en el **Artículo 495** del Código Civil para el Estado de Tamaulipas, que establece la necesidad de autorización judicial para actos que legalmente no pueden realizarse sin ella, solicito se autorice al **Lic. Jorge Ricardo Cruz Reyes**, quien forma parte del equipo legal que atiende el presente asunto, para que tenga acceso al expediente correspondiente al presente caso.  

2. **Autorización para uso de medios electrónicos del tribunal:**  
   Asimismo, con base en el **Artículo 42**, que regula el acceso a medios electrónicos y la expedición de copias certificadas, solicito se autorice al **Lic. Jorge Ricardo Cruz Reyes** para que pueda realizar trámites y consultas a través de los medios electrónicos del tribunal, conforme a lo establecido en las normas aplicables.  

El correo electrónico para recibir notificaciones es **rickardocr10287@gmail.com**, el cual ya se encuentra registrado en el tribunal.  

Lo anterior, con la finalidad de agilizar los trámites correspondientes y garantizar una adecuada defensa de los intereses de mi representado(a).  

Agradezco de antemano la atención que se sirva dar al presente escrito, quedando a sus órdenes para cualquier aclaración o documentación adicional que se requiera.  

**Atentamente,**  
[Su nombre completo]  
[Su firma, si aplica]  
**Cédula Profesional:** 10761923  
**Correo electrónico:** rickardocr10287@gmail.com  

**C. C. P.**  
- Lic. Jorge Ricardo Cruz Reyes  
- [Otras partes interesadas, si aplica]  

**LUGAR Y FECHA:**  
[Ciudad], a [día] de [mes] de [año].  
"""

doc = Document()

for linea in contenido.split('\n'):
    if linea.startswith('# '):
        doc.add_heading(linea[2:], level=1)
    elif linea.startswith('## '):
        doc.add_heading(linea[3:], level=2)
    elif linea.startswith('- '):
        # Procesar listas con negritas
        p = doc.add_paragraph(style='List Bullet')
        texto = linea[2:]
        while '**' in texto:
            antes, texto = texto.split('**', 1)
            p.add_run(antes)
            negrita, texto = texto.split('**', 1)
            p.add_run(negrita).bold = True
        p.add_run(texto)
    else:
        # Procesar párrafos con negritas
        p = doc.add_paragraph()
        texto = linea
        while '**' in texto:
            antes, texto = texto.split('**', 1)
            p.add_run(antes)
            negrita, texto = texto.split('**', 1)
            p.add_run(negrita).bold = True
        p.add_run(texto)

doc.save('documento_generado.docx')
print("Archivo Word generado con éxito.")