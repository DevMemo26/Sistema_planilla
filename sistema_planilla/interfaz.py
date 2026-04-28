import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:8000"

class AplicacionRRHH:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Planilla - RRHH")
        self.root.geometry("650x850")

        self.frame_login = tk.Frame(self.root, padx=50, pady=50)
        self.frame_principal = tk.Frame(self.root)

        self.setup_login()
        self.setup_principal()

        self.frame_login.pack(expand=True)

    def setup_login(self):
        self.root.configure(bg="#f0fdfa") 
        self.frame_login.configure(bg="#f0fdfa")

        header = tk.Frame(self.frame_login, bg="white", height=70)
        header.pack(fill=tk.X, side=tk.TOP, pady=(0, 20))
        header.pack_propagate(False)
        
        tk.Label(header, text="Sistema de Planilla", font=("Segoe UI", 16, "bold"), fg="#059669", bg="white").pack(side=tk.LEFT, padx=60)
        
        nav_frame = tk.Frame(header, bg="white")
        nav_frame.pack(side=tk.RIGHT, padx=60)
        
        for text in ["Soporte", "Seguridad", "Contacto"]:
            tk.Label(nav_frame, text=text, font=("Segoe UI", 10), fg="#64748b", bg="white", cursor="hand2").pack(side=tk.LEFT, padx=15)
        
        tk.Label(nav_frame, text="Ayuda", font=("Segoe UI", 10, "bold"), fg="#059669", bg="white", cursor="hand2").pack(side=tk.LEFT, padx=15)

        container = tk.Frame(self.frame_login, bg="#f0fdfa")
        container.pack(expand=True)

        card = tk.Frame(container, bg="white", padx=60, pady=50, highlightbackground="#e2e8f0", highlightthickness=1)
        card.pack(pady=20)

        lock_canvas = tk.Canvas(card, width=80, height=80, bg="white", highlightthickness=0)
        lock_canvas.pack(pady=(0, 25))
        lock_canvas.create_oval(10, 10, 70, 70, fill="#ecfdf5", outline="")
        lock_canvas.create_text(40, 40, text="🔒", font=("Segoe UI", 28), fill="#059669")

        tk.Label(card, text="Acceso Restringido", font=("Segoe UI", 20, "bold"), bg="white", fg="#1e293b").pack(pady=(0, 5))
        tk.Label(card, text="Ingrese sus credenciales corporativas para\ncontinuar", font=("Segoe UI", 11), bg="white", fg="#64748b", justify="center").pack(pady=(0, 35))

        tk.Label(card, text="USUARIO", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w")
        
        user_frame = tk.Frame(card, bg="#f8fafc", highlightbackground="#e2e8f0", highlightthickness=1)
        user_frame.pack(fill=tk.X, pady=(5, 20))
        
        tk.Label(user_frame, text="👤", font=("Segoe UI", 12), bg="#f8fafc", fg="#94a3b8").pack(side=tk.LEFT, padx=12)
        self.entry_usuario = tk.Entry(user_frame, font=("Segoe UI", 12), bg="#f8fafc", relief="flat", borderwidth=0, fg="#64748b")
        self.entry_usuario.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12)
        self.entry_usuario.insert(0, "Ingrese su usuario")
        self.entry_usuario.bind("<FocusIn>", lambda e: self.on_entry_click(self.entry_usuario, "Ingrese su usuario"))
        self.entry_usuario.bind("<FocusOut>", lambda e: self.on_focusout(self.entry_usuario, "Ingrese su usuario"))

        tk.Label(card, text="CONTRASEÑA", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w")
        
        pass_frame = tk.Frame(card, bg="#f8fafc", highlightbackground="#e2e8f0", highlightthickness=1)
        pass_frame.pack(fill=tk.X, pady=(5, 5))
        
        tk.Label(pass_frame, text="🔑", font=("Segoe UI", 12), bg="#f8fafc", fg="#94a3b8").pack(side=tk.LEFT, padx=12)
        self.entry_password = tk.Entry(pass_frame, font=("Segoe UI", 12), bg="#f8fafc", relief="flat", borderwidth=0, fg="#64748b")
        self.entry_password.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12)
        self.entry_password.insert(0, "........")
        self.entry_password.bind("<FocusIn>", lambda e: self.on_entry_click(self.entry_password, "........", is_pass=True))
        self.entry_password.bind("<FocusOut>", lambda e: self.on_focusout(self.entry_password, "........", is_pass=True))

        btn_ingresar = tk.Button(card, text="Ingresar al Sistema  ➔", command=self.intentar_login, bg="#10b981", fg="white", font=("Segoe UI", 12, "bold"), relief="flat", activebackground="#059669", activeforeground="white", cursor="hand2")
        btn_ingresar.pack(fill=tk.X, ipady=12)

    def on_entry_click(self, entry, placeholder, is_pass=False):
        """Maneja el efecto de placeholder al hacer click"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#1e293b")
            if is_pass:
                entry.config(show="*")

    def on_focusout(self, entry, placeholder, is_pass=False):
        """Restaura el placeholder si el campo queda vacío"""
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="#64748b")
            if is_pass:
                entry.config(show="")

    def intentar_login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        if not usuario or usuario == "Ingrese su usuario" or not password or password == "........":
            messagebox.showwarning("Advertencia", "Por favor ingrese usuario y contraseña.")
            return

        try:
            respuesta = requests.post(f"{API_URL}/login", json={"username": usuario, "password": password})

            if respuesta.status_code == 200:
                datos = respuesta.json()
                
                self.frame_login.pack_forget()

                self.root.geometry("1200x900")
                
                self.root.configure(bg="#f0f0f0") 
                self.frame_principal.pack(fill=tk.BOTH, expand=True)

                self.cargar_datos()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

        except Exception:
            messagebox.showerror("Error", "No se pudo conectar con el servidor backend.")
            messagebox.showerror("Error", "No se pudo conectar con el servidor backend.")


    def setup_principal(self):
        # 1. Contenedor para el contenido dinámico (Scrollable)
        self.main_scroll_canvas = tk.Canvas(self.frame_principal, bg="#f8fafc", highlightthickness=0)
        self.main_scroll_bar = ttk.Scrollbar(self.frame_principal, orient="vertical", command=self.main_scroll_canvas.yview)
        
        self.scrollable_content = tk.Frame(self.main_scroll_canvas, bg="#f8fafc")
        self.scrollable_content.bind("<Configure>", lambda e: self.main_scroll_canvas.configure(scrollregion=self.main_scroll_canvas.bbox("all")))

        self.main_scroll_canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")
        self.main_scroll_canvas.configure(yscrollcommand=self.main_scroll_bar.set)

        self.main_scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.setup_tab_diario()

    def setup_tab_diario(self):
        # 1. Fondo
        container = self.scrollable_content
        
        frame_header = tk.Frame(container, bg="#f8fafc")
        frame_header.pack(fill=tk.X, padx=60, pady=(40, 20))

        left_header = tk.Frame(frame_header, bg="#f8fafc")
        left_header.pack(side=tk.LEFT)
        tk.Label(left_header, text="Registro Histórico de Citas", font=("Segoe UI", 24, "bold"), fg="#1e293b", bg="#f8fafc").pack(anchor="w")
        tk.Label(left_header, text="Gestión detallada y conciliación de comisiones médicas.", font=("Segoe UI", 11), fg="#64748b", bg="#f8fafc").pack(anchor="w", pady=(2, 0))

        right_header = tk.Frame(frame_header, bg="#f8fafc")
        right_header.pack(side=tk.RIGHT, anchor="s")

        btn_tarjetas = tk.Button(right_header, text=" 🗂️ Tarjetas de Personal ", font=("Segoe UI", 10, "bold"), 
                           bg="#059669", fg="white", relief="flat", padx=15, pady=6, cursor="hand2",
                           command=self.mostrar_vista_tarjetas)
        btn_tarjetas.pack(side=tk.LEFT, padx=(0, 10))

        btn_agregar_personal = tk.Button(right_header, text=" ➕ Agregar Personal ", font=("Segoe UI", 10, "bold"), 
                           bg="#3b82f6", fg="white", relief="flat", padx=15, pady=6, cursor="hand2",
                           command=self.mostrar_formulario_personal)
        btn_agregar_personal.pack(side=tk.LEFT)

        card_tabla = tk.Frame(container, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        card_tabla.pack(fill=tk.X, padx=60, pady=(0, 30))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="#334155", rowheight=55, fieldbackground="white", borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="white", foreground="#64748b", font=('Segoe UI', 9, 'bold'), borderwidth=0, relief="flat")
        style.map('Treeview', background=[('selected', '#f1f5f9')], foreground=[('selected', '#1e293b')])

        columnas = ("id", "medico", "concepto", "monto", "estado")
        self.tabla = ttk.Treeview(card_tabla, columns=columnas, show="headings", style="Treeview")

        headers = {"id": "ID", "medico": "MÉDICO", "concepto": "CONCEPTO", "monto": "COMISIÓN", "estado": "ESTADO"}
        for col, text in headers.items():
            self.tabla.heading(col, text=text, anchor=tk.W)

        self.tabla.column("id", width=80, anchor=tk.W)
        self.tabla.column("medico", width=300, anchor=tk.W)
        self.tabla.column("concepto", width=350, anchor=tk.W)
        self.tabla.column("monto", width=150, anchor=tk.W)
        self.tabla.column("estado", width=120, anchor=tk.CENTER)

        self.tabla.pack(fill=tk.X, padx=25, pady=(20, 10))

        self.tabla.tag_configure("pagado", foreground="#059669")
        self.tabla.tag_configure("pendiente", foreground="#d97706")
        self.tabla.tag_configure("anulado", foreground="#dc2626")

        footer_tabla = tk.Frame(card_tabla, bg="white", height=50)
        footer_tabla.pack(fill=tk.X, padx=25, pady=(0, 20))
        
        self.lbl_conteo = tk.Label(footer_tabla, text="Mostrando 0 de 0 registros", font=("Segoe UI", 10), fg="#64748b", bg="#ffffff")
        self.lbl_conteo.pack(side=tk.LEFT)
        
        pag_frame = tk.Frame(footer_tabla, bg="white")
        pag_frame.pack(side=tk.RIGHT)
        
        for p in ["Anterior", "1", "2", "3", "Siguiente"]:
            is_active = p == "1"
            is_text = p in ["Anterior", "Siguiente"]
            btn_p = tk.Label(pag_frame, text=p, font=("Segoe UI", 9, "bold" if is_active else "normal"), 
                            width=8 if is_text else 3, height=1,
                            bg="#059669" if is_active else "white", 
                            fg="white" if is_active else "#64748b", 
                            highlightbackground="#e2e8f0" if not is_active else "#059669",
                            highlightthickness=1,
                            cursor="hand2")
            btn_p.pack(side=tk.LEFT, padx=2)

        frame_actions = tk.Frame(container, bg="#f8fafc")
        frame_actions.pack(fill=tk.X, padx=60, pady=(0, 60))
        
        right_actions = tk.Frame(frame_actions, bg="#f8fafc")
        right_actions.pack(side=tk.RIGHT)

        btn_sync = tk.Button(right_actions, text="🔄 Sincronizar Todo", command=self.cargar_datos, 
                             bg="#059669", fg="white", font=("Segoe UI", 11, "bold"), 
                             relief="flat", activebackground="#047857", activeforeground="white", 
                             cursor="hand2", padx=25, pady=12)
        btn_sync.pack(side=tk.LEFT)


    def cargar_datos(self):
        try:
            # 1. Obtener pagos y médicos del backend
            resp_pagos = requests.get(f"{API_URL}/pagos")
            resp_medicos = requests.get(f"{API_URL}/medicos")
            
            resp_pagos.raise_for_status()
            resp_medicos.raise_for_status()
            
            pagos = resp_pagos.json()
            medicos_db = resp_medicos.json()

            # 2. Limpiar vistas antiguas
            for row in self.tabla.get_children(): self.tabla.delete(row)
            
            # Verificar si el contenedor de tarjetas existe y sigue siendo válido
            if hasattr(self, 'container_tarjetas') and self.container_tarjetas.winfo_exists():
                for widget in self.container_tarjetas.winfo_children(): 
                    widget.destroy()

            # 3. Diccionario para agrupar (para las tarjetas)
            resumen_medicos = {}
            
            # Inicializar con los datos base de los médicos registrados
            for m in medicos_db:
                resumen_medicos[m["codigo"]] = {
                    "nombre": m["nombre"],
                    "profesion": m["profesion"],
                    "sueldo_base": m["sueldo_base"],
                    "comisiones_total": 0,
                    "citas": []
                }

            # 4. Procesar pagos
            for p in pagos:
                # --- Llenar Tabla Historial ---
                medico_display = f"{p['nombre_medico']} ({p['codigo_medico']})"
                estado_raw = p.get("estado", "Pagado").lower()
                estado_display = estado_raw.capitalize()
                
                self.tabla.insert("", tk.END, values=(
                    p['id'], 
                    medico_display, 
                    p['concepto'], 
                    f"${p['monto']:,.2f}", 
                    estado_display
                ), tags=(estado_raw,))

                # --- Agrupar para las Tarjetas ---
                codigo = p["codigo_medico"]
                if codigo not in resumen_medicos:
                    # Si el médico no está registrado en 'medicos', lo agregamos con sueldo base 0
                    resumen_medicos[codigo] = {"nombre": p["nombre_medico"], "profesion": "Médico", "sueldo_base": 0, "comisiones_total": 0, "citas": []}
                
                resumen_medicos[codigo]["comisiones_total"] += p["monto"]
                resumen_medicos[codigo]["citas"].append(f"{p['concepto']} (${p['monto']:,.2f})")

            # 5. Dibujar Tarjetas (si el contenedor existe y es válido)
            if hasattr(self, 'container_tarjetas') and self.container_tarjetas.winfo_exists():
                for codigo, info in resumen_medicos.items():
                    self.crear_tarjeta(codigo, info)

            # Actualizar conteo
            self.lbl_conteo.config(text=f"Mostrando {len(pagos)} de {len(pagos)} registros")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}")

    def mostrar_vista_tarjetas(self):
        # Crear ventana secundaria para las tarjetas
        self.win_tarjetas = tk.Toplevel(self.root)
        self.win_tarjetas.title("Tarjetas de Personal Médicos")
        self.win_tarjetas.geometry("900x800")
        self.win_tarjetas.configure(bg="#f8fafc")

        # Header de la ventana
        header = tk.Frame(self.win_tarjetas, bg="white", height=70, highlightbackground="#e2e8f0", highlightthickness=1)
        header.pack(fill=tk.X)
        tk.Label(header, text="🗂️ Resumen de Personal Médico", font=("Segoe UI", 16, "bold"), fg="#1e293b", bg="white").pack(side=tk.LEFT, padx=30)
        
        # Área Scrollable
        canvas = tk.Canvas(self.win_tarjetas, bg="#f8fafc", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.win_tarjetas, orient="vertical", command=canvas.yview)
        self.container_tarjetas = tk.Frame(canvas, bg="#f8fafc")
        
        self.container_tarjetas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.container_tarjetas, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Cargar los datos para llenar las tarjetas
        self.cargar_datos()

    def crear_tarjeta(self, codigo, info):
        card = tk.Frame(self.container_tarjetas, bg="white", highlightbackground="#e2e8f0", highlightthickness=1, padx=25, pady=25)
        card.pack(fill=tk.X, pady=10)

        top_frame = tk.Frame(card, bg="white")
        top_frame.pack(fill=tk.X)
        
        tk.Label(top_frame, text=info["nombre"], font=("Segoe UI", 14, "bold"), fg="#1e293b", bg="white").pack(side=tk.LEFT)
        tk.Label(top_frame, text=f"ID: {codigo}", font=("Segoe UI", 10), fg="#64748b", bg="white").pack(side=tk.RIGHT)
        
        tk.Label(card, text=info["profesion"], font=("Segoe UI", 10, "italic"), fg="#059669", bg="white").pack(anchor="w", pady=(2, 10))
        
        # Detalles de Sueldo
        frame_sueldos = tk.Frame(card, bg="#f8fafc", padx=15, pady=10)
        frame_sueldos.pack(fill=tk.X, pady=10)
        
        # Sueldo Base
        col1 = tk.Frame(frame_sueldos, bg="#f8fafc")
        col1.pack(side=tk.LEFT, expand=True)
        tk.Label(col1, text="Sueldo Base", font=("Segoe UI", 9), fg="#64748b", bg="#f8fafc").pack()
        tk.Label(col1, text=f"${info['sueldo_base']:,.2f}", font=("Segoe UI", 12, "bold"), fg="#1e293b", bg="#f8fafc").pack()
        
        # Comisiones
        col2 = tk.Frame(frame_sueldos, bg="#f8fafc")
        col2.pack(side=tk.LEFT, expand=True)
        tk.Label(col2, text="Comisiones", font=("Segoe UI", 9), fg="#64748b", bg="#f8fafc").pack()
        tk.Label(col2, text=f"+ ${info['comisiones_total']:,.2f}", font=("Segoe UI", 12, "bold"), fg="#059669", bg="#f8fafc").pack()
        
        # Total
        sueldo_total = info['sueldo_base'] + info['comisiones_total']
        col3 = tk.Frame(frame_sueldos, bg="#f8fafc")
        col3.pack(side=tk.LEFT, expand=True)
        tk.Label(col3, text="Sueldo Total", font=("Segoe UI", 9), fg="#64748b", bg="#f8fafc").pack()
        tk.Label(col3, text=f"${sueldo_total:,.2f}", font=("Segoe UI", 14, "bold"), fg="#10b981", bg="#f8fafc").pack()

        btn_detalle = tk.Button(card, text="Ver Detalle de Citas ➔", font=("Segoe UI", 9, "bold"), 
                              bg="#f1f5f9", fg="#1e293b", relief="flat", padx=15, pady=8, cursor="hand2",
                              command=lambda: self.mostrar_detalle(info))
        btn_detalle.pack(anchor="e", pady=(10, 0))

    def mostrar_detalle(self, info):
        detalle = tk.Toplevel(self.win_tarjetas)
        detalle.title(f"Detalle: {info['nombre']}")
        detalle.geometry("500x450")
        detalle.configure(bg="white")

        tk.Label(detalle, text="Desglose de Comisiones", font=("Segoe UI", 14, "bold"), fg="#1e293b", bg="white").pack(pady=20)

        frame_lista = tk.Frame(detalle, bg="white")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=30)

        if not info["citas"]:
            tk.Label(frame_lista, text="No hay comisiones registradas.", font=("Segoe UI", 10), fg="#94a3b8", bg="white").pack()
        else:
            for cita in info["citas"]:
                item = tk.Frame(frame_lista, bg="white", pady=5)
                item.pack(fill=tk.X)
                tk.Label(item, text="•", font=("Segoe UI", 12), fg="#059669", bg="white").pack(side=tk.LEFT)
                tk.Label(item, text=cita, font=("Segoe UI", 10), fg="#334155", bg="white", justify="left").pack(side=tk.LEFT, padx=10)

        tk.Frame(detalle, height=1, bg="#e2e8f0").pack(fill=tk.X, padx=30, pady=15)
        tk.Label(detalle, text=f"Total Comisiones: ${info['comisiones_total']:,.2f}", font=("Segoe UI", 13, "bold"), fg="#059669", bg="white").pack(pady=(0, 30))

    def mostrar_formulario_personal(self):
        self.win_personal = tk.Toplevel(self.root)
        self.win_personal.title("Agregar Nuevo Personal")
        self.win_personal.geometry("450x550")
        self.win_personal.configure(bg="white")

        tk.Label(self.win_personal, text="Nuevo Miembro del Personal", font=("Segoe UI", 16, "bold"), bg="white", fg="#1e293b").pack(pady=30)

        fields = [
            ("Código de Médico/Empleado", "entry_cod"),
            ("Nombre Completo", "entry_nom"),
            ("Profesión / Especialidad", "entry_prof"),
            ("Sueldo Base ($)", "entry_sueldo")
        ]

        self.form_entries = {}
        for label_text, attr_name in fields:
            frame = tk.Frame(self.win_personal, bg="white", padx=40)
            frame.pack(fill=tk.X, pady=10)
            
            tk.Label(frame, text=label_text, font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w")
            entry = tk.Entry(frame, font=("Segoe UI", 11), bg="#f8fafc", relief="flat", highlightbackground="#e2e8f0", highlightthickness=1)
            entry.pack(fill=tk.X, ipady=8, pady=(5, 0))
            self.form_entries[attr_name] = entry

        btn_guardar = tk.Button(self.win_personal, text="Guardar Personal", command=self.guardar_personal, 
                               bg="#3b82f6", fg="white", font=("Segoe UI", 11, "bold"), 
                               relief="flat", activebackground="#2563eb", cursor="hand2", pady=12)
        btn_guardar.pack(fill=tk.X, padx=40, pady=40)

    def guardar_personal(self):
        try:
            cod = self.form_entries["entry_cod"].get()
            nom = self.form_entries["entry_nom"].get()
            prof = self.form_entries["entry_prof"].get()
            sueldo = self.form_entries["entry_sueldo"].get()

            if not cod or not nom:
                messagebox.showwarning("Advertencia", "Código y Nombre son obligatorios.")
                return

            datos = {
                "codigo": cod,
                "nombre": nom,
                "profesion": prof,
                "sueldo_base": float(sueldo or 0)
            }

            resp = requests.post(f"{API_URL}/medicos", json=datos)
            if resp.status_code == 200:
                messagebox.showinfo("Éxito", "Personal agregado correctamente.")
                self.win_personal.destroy()
                self.cargar_datos()
            else:
                messagebox.showerror("Error", resp.json().get("detail", "No se pudo agregar."))
        except ValueError:
            messagebox.showerror("Error", "El sueldo base debe ser un número válido.")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionRRHH(root)
    root.mainloop()