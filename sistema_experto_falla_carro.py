import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import clips 

# ---- Configuración del Motor de Inferencia de CLIPS ----
def setup_clips_environment():
    env = clips.Environment()

    env.build("(deftemplate sintoma (slot nombre))")

    env.build("""
    (deftemplate diagnostico
       (slot titulo)
       (slot solucion)
       (slot explicacion)
    )""")

    env.build("""
    (defrule problema-de-encendido-completo
       (sintoma (nombre "No enciende"))
       (sintoma (nombre "Batería descargada"))
       =>
       (assert (diagnostico
          (titulo "Problema de encendido (confirmado)")
          (solucion "Problema eléctrico: Revise la batería.")
          (explicacion "El carro no enciende y se ha identificado que la batería está descargada. Esto es la causa principal del fallo, impidiendo que el motor de arranque funcione. Es crucial recargar o reemplazar la batería.")
       ))
    )
    """)

    env.build("""
    (defrule problema-de-encendido-basico
       (sintoma (nombre "No enciende"))
       =>
       (assert (diagnostico
          (titulo "Problema de encendido")
          (solucion "Problema eléctrico: Revise la batería o el motor de arranque.")
          (explicacion "El carro no enciende. Aunque la causa más común es la batería, podría haber otras fallas en el sistema eléctrico, como el motor de arranque o el alternador.")
       ))
    )
    """)

    env.build("""
    (defrule problema-en-motor-completo
       (sintoma (nombre "Ruido metálico"))
       (sintoma (nombre "Pierde potencia"))
       =>
       (assert (diagnostico
          (titulo "Problema en el motor (grave)")
          (solucion "Posible problema interno en el motor.")
          (explicacion "Se ha detectado un 'ruido metálico' y el carro 'pierde potencia'. Esta combinación de síntomas indica un posible desgaste severo en los componentes internos del motor (pistones, bielas). Requiere atención mecánica inmediata.")
       ))
    )
    """)
    
    env.build("""
    (defrule problema-en-motor-basico
       (sintoma (nombre "Ruido metálico"))
       =>
       (assert (diagnostico
          (titulo "Problema en el motor")
          (solucion "Posible problema en el motor.")
          (explicacion "Un 'ruido metálico' es una señal de alerta. Puede ser un indicio de desgaste interno o una pieza suelta. Es necesario un diagnóstico profesional para determinar la causa exacta y evitar daños mayores.")
       ))
    )
    """)
    
    env.build("""
    (defrule problema-en-escape-completo
       (sintoma (nombre "Sale humo"))
       (sintoma (nombre "Olor extraño"))
       =>
       (assert (diagnostico
          (titulo "Problema en el escape (confirmado)")
          (solucion "Posible problema en el sistema de escape o motor.")
          (explicacion "El carro emite 'humo' y se percibe un 'olor extraño'. Esto sugiere una combustión incompleta o que fluidos (aceite, refrigerante) se están quemando. La revisión del sistema de escape y del motor es fundamental.")
       ))
    )
    """)

    env.build("""
    (defrule problema-en-escape-basico
       (sintoma (nombre "Sale humo"))
       =>
       (assert (diagnostico
          (titulo "Problema en el escape")
          (solucion "Posible problema en el sistema de escape.")
          (explicacion "La salida de humo del escape puede deberse a diversas razones, desde un empaque de culata defectuoso hasta problemas en el convertidor catalítico. Se recomienda una revisión profesional.")
       ))
    )
    """)

    env.build("""
    (defrule problema-en-frenos-completo
       (sintoma (nombre "Dificultad al frenar"))
       (sintoma (nombre "Chirrido en frenos"))
       =>
       (assert (diagnostico
          (titulo "Problema en los frenos (desgaste)")
          (solucion "Revisar sistema de frenos: posible desgaste de pastillas.")
          (explicacion "Se ha detectado 'dificultad al frenar' junto con un 'chirrido'. Esta combinación es un fuerte indicio de que las pastillas de freno están desgastadas y necesitan ser reemplazadas para garantizar la seguridad.")
       ))
    )
    """)
    
    env.build("""
    (defrule problema-en-frenos-basico
       (sintoma (nombre "Dificultad al frenar"))
       =>
       (assert (diagnostico
          (titulo "Problema en los frenos")
          (solucion "Revisar sistema de frenos.")
          (explicacion "Sentir 'dificultad al frenar' es un riesgo para la seguridad. Puede ser causado por un bajo nivel de líquido de frenos o aire en el sistema. Se debe revisar urgentemente el sistema de frenos.")
       ))
    )
    """)
    
    env.build("""
    (defrule problema-en-suspension-alineacion-completo
       (sintoma (nombre "Vibración al conducir"))
       (sintoma (nombre "Desgaste irregular de llantas"))
       =>
       (assert (diagnostico
          (titulo "Problema de suspensión y alineación")
          (solucion "Posible problema de alineación o suspensión.")
          (explicacion "La 'vibración al conducir' y el 'desgaste irregular de las llantas' son síntomas directos de una mala alineación o de problemas en la suspensión. Esto afecta la seguridad y el rendimiento del vehículo.")
       ))
    )
    """)

    env.build("""
    (defrule problema-en-suspension-alineacion-basico
       (sintoma (nombre "Vibración al conducir"))
       =>
       (assert (diagnostico
          (titulo "Problema de suspensión/alineación")
          (solucion "Posible problema de alineación o suspensión.")
          (explicacion "La 'vibración al conducir' puede ser causada por un desbalanceo de las llantas o problemas en los amortiguadores. Se recomienda una revisión de la suspensión.")
       ))
    )
    """)
    
    env.build("""
    (defrule problema-en-transmision-basico
       (sintoma (nombre "Ruido extraño al hacer cambiar"))
       =>
       (assert (diagnostico
          (titulo "Problema en transmisión")
          (solucion "Revisar la caja de cambios.")
          (explicacion "Un 'ruido extraño al hacer cambiar' es un síntoma de una falla en la caja de cambios. Se debe inspeccionar el nivel y el estado del fluido de transmisión para descartar problemas.")
       ))
    )
    """)

    env.build("""
    (defrule problema-bateria-descargada
       (sintoma (nombre "Batería descargada"))
       =>
       (assert (diagnostico
          (titulo "Falla en la batería")
          (solucion "Recargue o reemplace la batería.")
          (explicacion "La batería está descargada y no puede proveer la energía necesaria para encender el carro. Esto puede ser por un alternador defectuoso, una luz dejada encendida, o simplemente por el fin de su vida útil.")
       ))
    )
    """)

    env.build("""
    (defrule problema-de-potencia-basico
       (sintoma (nombre "Pierde potencia"))
       =>
       (assert (diagnostico
          (titulo "Problema de potencia")
          (solucion "Revisar sistema de combustible, filtros o bujías.")
          (explicacion "La pérdida de potencia puede ser causada por una variedad de problemas, como un filtro de aire sucio, bujías defectuosas, o problemas en el sistema de inyección de combustible. Se recomienda una revisión del motor.")
       ))
    )
    """)
    
    env.build("""
    (defrule problema-de-olor-extranao
       (sintoma (nombre "Olor extraño"))
       =>
       (assert (diagnostico
          (titulo "Posible fuga o problema de combustión")
          (solucion "Revisar si hay fugas de fluidos o un problema de combustión.")
          (explicacion "Un 'olor extraño' puede ser indicativo de fugas de fluidos como aceite, refrigerante o gasolina, o de una combustión incompleta. Es una señal de alerta que requiere una inspección profesional.")
       ))
    )
    """)
    
    env.build("""
    (defrule problema-frenos-desgaste-basico
       (sintoma (nombre "Chirrido en frenos"))
       =>
       (assert (diagnostico
          (titulo "Desgaste de pastillas de freno")
          (solucion "Reemplazar las pastillas de freno.")
          (explicacion "El 'chirrido en los frenos' es un claro indicio de que las pastillas están desgastadas. Se recomienda su reemplazo inmediato para evitar daños mayores en los discos y garantizar la seguridad.")
       ))
    )
    """)
    
    env.build("""
    (defrule problema-llantas-desgaste-basico
       (sintoma (nombre "Desgaste irregular de llantas"))
       =>
       (assert (diagnostico
          (titulo "Problema de alineación o suspensión")
          (solucion "Revisar la alineación y el balanceo de las llantas.")
          (explicacion "El 'desgaste irregular de las llantas' es una señal de que el carro tiene un problema de alineación, balanceo o en el sistema de suspensión, lo que puede afectar la estabilidad y la vida útil de los neumáticos.")
       ))
    )
    """)

    env.build("""
    (defrule problema-motor-combustion-completo
       (sintoma (nombre "Pierde potencia"))
       (sintoma (nombre "Olor extraño"))
       =>
       (assert (diagnostico
          (titulo "Problema en el sistema de combustible")
          (solucion "Revisar inyectores, bomba de combustible y bujías.")
          (explicacion "La combinación de 'pérdida de potencia' y un 'olor extraño' sugiere un problema en la combustión. Podría haber fallas en la entrega de combustible, una mezcla de aire y gasolina incorrecta, o problemas con las bujías.")
       ))
    )
    """)

    return env

symptoms = [
    "No enciende",
    "Ruido metálico",
    "Sale humo",
    "Dificultad al frenar",
    "Vibración al conducir",
    "Ruido extraño al hacer cambiar",
    "Batería descargada",
    "Pierde potencia",
    "Olor extraño",
    "Chirrido en frenos",
    "Desgaste irregular de llantas"
]

def diagnose():

    selected_symptoms = [symptom for symptom, var in symptom_vars.items() if var.get()]
    
    if not selected_symptoms:
        messagebox.showwarning("Atención", "Por favor seleccione al menos un síntoma.")
        return

    for widget in result_inner_frame.winfo_children():
        widget.destroy()

    env = setup_clips_environment()
    
    for symptom in selected_symptoms:
        env.assert_string(f'(sintoma (nombre "{symptom}"))')
        
    env.run()

    results = []
    for fact in env.facts():
        if fact.template.name == "diagnostico":
            results.append({
                "title": fact["titulo"],
                "diagnosis": fact["solucion"],
                "explanation": fact["explicacion"],
                "matched": selected_symptoms 
            })
    
    if not results:
        create_diagnosis_cards([{"title": "Sin diagnóstico", "diagnosis": "Pruebe seleccionando otros síntomas o consulte a un mecánico especializado.", "explanation": "", "matched": []}], "")
    else:
        create_diagnosis_cards(results, "Resultados del diagnóstico.")

def create_diagnosis_cards(diagnoses, explanation):
    """
    Crea y muestra las tarjetas de diagnóstico en la interfaz.
    """
    for diag in diagnoses:
        card = tk.Frame(result_inner_frame, bg="#ffffff", bd=1, relief="solid")
        card.pack(pady=10, padx=60, fill="x")

        title = tk.Label(card, text=f"{diag['title']}", font=("Segoe UI", 15, "bold"), bg="#ffffff", fg="#2c3e50", anchor="center", wraplength=500)
        title.pack(fill="x", padx=10, pady=8)

        explanation_frame = tk.Frame(card, bg="#f8f9fa")
        explanation_label = tk.Label(explanation_frame, text=diag["diagnosis"], font=("Segoe UI", 12), bg="#f8f9fa", fg="#555555", wraplength=500, justify="left")
        explanation_label.pack(padx=15, pady=5)
        
        detail_explanation_label = tk.Label(explanation_frame, text=f"¿Por qué se llegó a esta conclusión?\n\n{diag['explanation']}", font=("Segoe UI", 11, "italic"), bg="#f8f9fa", fg="#888888", wraplength=500, justify="left")
        detail_explanation_label.pack(padx=15, pady=(5, 10))

        explanation_frame.pack_forget()

        def toggle(frame=explanation_frame):
            if frame.winfo_ismapped():
                frame.pack_forget()
            else:
                frame.pack(fill="x")
        
        title.bind("<Button-1>", lambda e, f=explanation_frame: toggle(f))

def create_switch(frame, text, variable):
    """
    Crea los botones de switch para los síntomas.
    """
    def toggle():
        variable.set(not variable.get())
        draw_switch()
        
    switch_frame = tk.Frame(frame, bg="#ffffff")
    switch_frame.pack(fill="x", pady=6)
    
    label = tk.Label(switch_frame, text=text, font=("Segoe UI", 12), bg="#ffffff", fg="#2c3e50")
    label.pack(side="left", padx=10)
    
    canvas = tk.Canvas(switch_frame, width=55, height=26, bg="#ffffff", highlightthickness=0)
    canvas.pack(side="right", padx=10)
    
    def draw_switch():
        canvas.delete("all")
        if variable.get():
            canvas.create_oval(28, 3, 52, 23, fill="#2980b9", outline="#2980b9")
            canvas.create_oval(3, 3, 28, 23, fill="#ffffff", outline="#cccccc")
        else:
            canvas.create_oval(3, 3, 28, 23, fill="#cccccc", outline="#cccccc")
            canvas.create_oval(28, 3, 52, 23, fill="#ffffff", outline="#cccccc")
    
    canvas.bind("<Button-1>", lambda e: toggle())
    draw_switch()

root = tk.Tk()
root.title("Sistema Experto: Falla de un carro")
root.geometry("700x780")
root.configure(bg="#f0f2f5")

try:
    root.iconphoto(False, tk.PhotoImage(file="icons/car_icon.png"))
except:
    pass

header_frame = tk.Frame(root, bg="#2980b9")
header_frame.pack(fill="x")
try:
    header_img = Image.open("icons/header_car.png").resize((50, 50))
    header_icon = ImageTk.PhotoImage(header_img)
    header_label_img = tk.Label(header_frame, image=header_icon, bg="#2980b9")
    header_label_img.pack(side="left", padx=15, pady=10)
except:
    pass
title_label = tk.Label(header_frame, text="Diagnóstico de fallas en el carro",
                        font=("Segoe UI", 20, "bold"), bg="#2980b9", fg="white")
title_label.pack(side="left", pady=15)

label = tk.Label(root, text="Seleccione los síntomas que presenta el carro:",
                 font=("Segoe UI", 13), bg="#f0f2f5", fg="#2c3e50")
label.pack(pady=12)

frame = tk.Frame(root, bg="#f0f2f5")
frame.pack(pady=5)
canvas = tk.Canvas(frame, width=640, height=250, bg="#ffffff", highlightthickness=0)
scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#ffffff")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

symptom_vars = {}
for symptom in symptoms:
    var = tk.BooleanVar()
    symptom_vars[symptom] = var
    create_switch(scrollable_frame, symptom, var)

def on_enter(e): diagnose_button.config(bg="#1f5e7a")
def on_leave(e): diagnose_button.config(bg="#2980b9")

button_frame = tk.Frame(root, bg="#f0f2f5")
button_frame.pack()
try:
    btn_img = Image.open("icons/diagnose_icon.png").resize((24, 24))
    btn_icon = ImageTk.PhotoImage(btn_img)
except:
    btn_icon = None
diagnose_button = tk.Button(button_frame, text="  Diagnosticar", image=btn_icon, compound="left",
                            command=diagnose, font=("Segoe UI", 14, "bold"),
                            bg="#2980b9", fg="white", activebackground="#1f5e7a",
                            relief="flat", bd=0, padx=20, pady=10)
diagnose_button.pack(pady=20)
diagnose_button.bind("<Enter>", on_enter)
diagnose_button.bind("<Leave>", on_leave)

result_frame = tk.Frame(root, bg="#ffffff", bd=0, relief="flat")
result_frame.pack(pady=10, padx=20, fill="both", expand=True)
result_frame.configure(highlightbackground="#dcdde1", highlightthickness=1)

result_canvas = tk.Canvas(result_frame, bg="#ffffff", highlightthickness=0)
result_scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=result_canvas.yview)
result_inner_frame = tk.Frame(result_canvas, bg="#ffffff")
result_inner_frame.bind("<Configure>", lambda e: result_canvas.configure(scrollregion=result_canvas.bbox("all")))
result_canvas.create_window((0, 0), window=result_inner_frame, anchor="nw", width=640)
result_canvas.configure(yscrollcommand=result_scrollbar.set)
result_canvas.pack(side="left", fill="both", expand=True)
result_scrollbar.pack(side="right", fill="y")

root.mainloop()
