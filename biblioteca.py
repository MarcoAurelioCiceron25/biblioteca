import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk

# Configuración visual
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class SistemaBibliotecaPro(ctk.CTk):

  def __init__(self):
    super().__init__()

    self.title("Sistema de Gestión de Biblioteca - Pro")
    self.geometry("900x700")
    self.resizable(False, False)

    # Datos en memoria
    self.libros = {}
    self.usuarios = {}
    self.prestamos = []

    self.aplicar_estilos_tabla()

    # --- ENCABEZADO ---
    self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
    self.frame_top.pack(fill="x", padx=20, pady=(15, 5))

    self.lbl_titulo = ctk.CTkLabel(
        self.frame_top,
        text="SISTEMA DE GESTIÓN DE BIBLIOTECA",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#3B8ED0",
    )
    self.lbl_titulo.pack(side="left")

    # --- DASHBOARD / ESTADÍSTICAS RÁPIDAS ---
    self.frame_stats = ctk.CTkFrame(self)
    self.frame_stats.pack(fill="x", padx=20, pady=10)

    self.lbl_stat_libros = ctk.CTkLabel(
        self.frame_stats,
        text="Libros Registrados: 0",
        font=ctk.CTkFont(weight="bold"),
    )
    self.lbl_stat_libros.pack(side="left", expand=True, pady=8)

    self.lbl_stat_prestamos = ctk.CTkLabel(
        self.frame_stats,
        text="Préstamos Activos: 0",
        font=ctk.CTkFont(weight="bold"),
        text_color="#E5A000",
    )
    self.lbl_stat_prestamos.pack(side="left", expand=True, pady=8)

    self.lbl_stat_users = ctk.CTkLabel(
        self.frame_stats,
        text="Usuarios Registrados: 0",
        font=ctk.CTkFont(weight="bold"),
    )
    self.lbl_stat_users.pack(side="left", expand=True, pady=8)

    # --- PESTAÑAS ---
    self.tabview = ctk.CTkTabview(self, width=860, height=520)
    self.tabview.pack(padx=20, pady=5, fill="both", expand=True)

    self.tab_libros = self.tabview.add("Libros")
    self.tab_usuarios = self.tabview.add("Usuarios")
    self.tab_prestamos = self.tabview.add("Préstamos y Devoluciones")

    self.setup_tab_libros()
    self.setup_tab_usuarios()
    self.setup_tab_prestamos()

  def aplicar_estilos_tabla(self):
    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "Treeview",
        background="#2A2D2E",
        foreground="white",
        rowheight=30,
        fieldbackground="#2A2D2E",
        bordercolor="#333333",
        borderwidth=0,
        font=("Helvetica", 10),
    )
    style.map("Treeview", background=[("selected", "#1F6AA5")])

    style.configure(
        "Treeview.Heading",
        background="#1F1F1F",
        foreground="#3B8ED0",
        relief="flat",
        font=("Helvetica", 11, "bold"),
    )
    style.map("Treeview.Heading", background=[("active", "#2B2B2B")])

  # ----------------------------------------------------
  # TAB 1: LIBROS
  # ----------------------------------------------------
  def setup_tab_libros(self):
    frame_input = ctk.CTkFrame(self.tab_libros)
    frame_input.pack(fill="x", padx=15, pady=15)

    ctk.CTkLabel(frame_input, text="ID Libro:").grid(
        row=0, column=0, padx=10, pady=10, sticky="e"
    )
    self.ent_libro_id = ctk.CTkEntry(
        frame_input, placeholder_text="L01", width=140
    )
    self.ent_libro_id.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(frame_input, text="Título:").grid(
        row=0, column=2, padx=10, pady=10, sticky="e"
    )
    self.ent_libro_titulo = ctk.CTkEntry(
        frame_input, placeholder_text="Ej. Cien Años de Soledad", width=220
    )
    self.ent_libro_titulo.grid(row=0, column=3, padx=10, pady=10)

    ctk.CTkLabel(frame_input, text="Autor:").grid(
        row=1, column=0, padx=10, pady=10, sticky="e"
    )
    self.ent_libro_autor = ctk.CTkEntry(
        frame_input, placeholder_text="Ej. G. García Márquez", width=140
    )
    self.ent_libro_autor.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(frame_input, text="Copias:").grid(
        row=1, column=2, padx=10, pady=10, sticky="e"
    )
    self.ent_libro_copias = ctk.CTkEntry(
        frame_input, placeholder_text="Ej. 3", width=220
    )
    self.ent_libro_copias.grid(row=1, column=3, padx=10, pady=10)

    btn_guardar = ctk.CTkButton(
        frame_input,
        text="[+] Registrar Libro",
        command=self.guardar_libro,
        fg_color="#2FA572",
        hover_color="#27875D",
        font=ctk.CTkFont(weight="bold"),
    )
    btn_guardar.grid(row=2, column=0, columnspan=4, pady=15)

    self.tree_libros = ttk.Treeview(
        self.tab_libros,
        columns=("ID", "Título", "Autor", "Disponibles"),
        show="headings",
    )
    for col in ("ID", "Título", "Autor", "Disponibles"):
      self.tree_libros.heading(col, text=col)
      self.tree_libros.column(col, anchor="center")
    self.tree_libros.pack(fill="both", expand=True, padx=15, pady=(0, 15))

  def guardar_libro(self):
    id_l = self.ent_libro_id.get().strip()
    titulo = self.ent_libro_titulo.get().strip()
    autor = self.ent_libro_autor.get().strip()
    copias = self.ent_libro_copias.get().strip()

    if not id_l or not titulo or not autor or not copias.isdigit():
      messagebox.showerror(
          "Error de Entrada", "Por favor completa todos los campos correctamente."
      )
      return

    self.libros[id_l] = {"titulo": titulo, "autor": autor, "copias": int(copias)}
    self.actualizar_tablas()
    messagebox.showinfo("Éxito", f"Libro '{titulo}' registrado.")

    self.ent_libro_id.delete(0, "end")
    self.ent_libro_titulo.delete(0, "end")
    self.ent_libro_autor.delete(0, "end")
    self.ent_libro_copias.delete(0, "end")

  # ----------------------------------------------------
  # TAB 2: USUARIOS
  # ----------------------------------------------------
  def setup_tab_usuarios(self):
    frame_input = ctk.CTkFrame(self.tab_usuarios)
    frame_input.pack(fill="x", padx=15, pady=15)

    ctk.CTkLabel(frame_input, text="ID Usuario:").grid(
        row=0, column=0, padx=10, pady=10, sticky="e"
    )
    self.ent_user_id = ctk.CTkEntry(
        frame_input, placeholder_text="U100", width=140
    )
    self.ent_user_id.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(frame_input, text="Nombre Completo:").grid(
        row=0, column=2, padx=10, pady=10, sticky="e"
    )
    self.ent_user_nombre = ctk.CTkEntry(
        frame_input, placeholder_text="Ej. María Gómez", width=220
    )
    self.ent_user_nombre.grid(row=0, column=3, padx=10, pady=10)

    btn_guardar_u = ctk.CTkButton(
        frame_input,
        text="[+] Registrar Usuario",
        command=self.guardar_usuario,
        font=ctk.CTkFont(weight="bold"),
    )
    btn_guardar_u.grid(row=1, column=0, columnspan=4, pady=15)

    self.tree_usuarios = ttk.Treeview(
        self.tab_usuarios, columns=("ID", "Nombre"), show="headings"
    )
    for col in ("ID", "Nombre"):
      self.tree_usuarios.heading(col, text=col)
      self.tree_usuarios.column(col, anchor="center")
    self.tree_usuarios.pack(fill="both", expand=True, padx=15, pady=(0, 15))

  def guardar_usuario(self):
    id_u = self.ent_user_id.get().strip()
    nombre = self.ent_user_nombre.get().strip()

    if not id_u or not nombre:
      messagebox.showerror(
          "Error", "Ingresa el ID y el Nombre completo del usuario."
      )
      return

    self.usuarios[id_u] = {"nombre": nombre}
    self.actualizar_tablas()
    messagebox.showinfo("Éxito", f"Usuario '{nombre}' registrado.")

    self.ent_user_id.delete(0, "end")
    self.ent_user_nombre.delete(0, "end")

  # ----------------------------------------------------
  # TAB 3: PRÉSTAMOS
  # ----------------------------------------------------
  def setup_tab_prestamos(self):
    frame_op = ctk.CTkFrame(self.tab_prestamos)
    frame_op.pack(fill="x", padx=15, pady=15)

    ctk.CTkLabel(frame_op, text="ID Usuario:").grid(
        row=0, column=0, padx=10, pady=10, sticky="e"
    )
    self.ent_p_user = ctk.CTkEntry(
        frame_op, placeholder_text="U100", width=140
    )
    self.ent_p_user.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(frame_op, text="ID Libro:").grid(
        row=0, column=2, padx=10, pady=10, sticky="e"
    )
    self.ent_p_libro = ctk.CTkEntry(
        frame_op, placeholder_text="L01", width=140
    )
    self.ent_p_libro.grid(row=0, column=3, padx=10, pady=10)

    btn_prestar = ctk.CTkButton(
        frame_op,
        text="[->] Prestar Libro",
        command=self.realizar_prestamo,
        fg_color="#1F6AA5",
        hover_color="#144870",
        font=ctk.CTkFont(weight="bold"),
    )
    btn_prestar.grid(row=1, column=1, pady=15)

    btn_devolver = ctk.CTkButton(
        frame_op,
        text="[<-] Devolver Libro",
        command=self.realizar_devolucion,
        fg_color="#D9534F",
        hover_color="#A53B37",
        font=ctk.CTkFont(weight="bold"),
    )
    btn_devolver.grid(row=1, column=2, pady=15)

    self.tree_prestamos = ttk.Treeview(
        self.tab_prestamos,
        columns=("ID Usuario", "Nombre Usuario", "ID Libro", "Título Libro"),
        show="headings",
    )
    for col in ("ID Usuario", "Nombre Usuario", "ID Libro", "Título Libro"):
      self.tree_prestamos.heading(col, text=col)
      self.tree_prestamos.column(col, anchor="center")
    self.tree_prestamos.pack(fill="both", expand=True, padx=15, pady=(0, 15))

  def realizar_prestamo(self):
    u_id = self.ent_p_user.get().strip()
    l_id = self.ent_p_libro.get().strip()

    if u_id not in self.usuarios:
      messagebox.showerror("Error", "ID de usuario no existe.")
      return
    if l_id not in self.libros:
      messagebox.showerror("Error", "ID de libro no existe.")
      return
    if self.libros[l_id]["copias"] <= 0:
      messagebox.showwarning(
          "Agotado", "No hay unidades disponibles de este libro."
      )
      return

    self.libros[l_id]["copias"] -= 1
    self.prestamos.append({"id_usuario": u_id, "id_libro": l_id})
    self.actualizar_tablas()
    messagebox.showinfo("Éxito", "Préstamo realizado.")

  def realizar_devolucion(self):
    u_id = self.ent_p_user.get().strip()
    l_id = self.ent_p_libro.get().strip()

    prestamo = next(
        (
            p
            for p in self.prestamos
            if p["id_usuario"] == u_id and p["id_libro"] == l_id
        ),
        None,
    )

    if not prestamo:
      messagebox.showerror(
          "Error", "No se encontró un préstamo activo coincidente."
      )
      return

    self.libros[l_id]["copias"] += 1
    self.prestamos.remove(prestamo)
    self.actualizar_tablas()
    messagebox.showinfo("Éxito", "Devolución registrada.")

  def actualizar_tablas(self):
    # Actualizar Libros
    for item in self.tree_libros.get_children():
      self.tree_libros.delete(item)
    for k, v in self.libros.items():
      self.tree_libros.insert(
          "", "end", values=(k, v["titulo"], v["autor"], v["copias"])
      )

    # Actualizar Usuarios
    for item in self.tree_usuarios.get_children():
      self.tree_usuarios.delete(item)
    for k, v in self.usuarios.items():
      self.tree_usuarios.insert("", "end", values=(k, v["nombre"]))

    # Actualizar Préstamos
    for item in self.tree_prestamos.get_children():
      self.tree_prestamos.delete(item)
    for p in self.prestamos:
      u_nom = self.usuarios[p["id_usuario"]]["nombre"]
      l_tit = self.libros[p["id_libro"]]["titulo"]
      self.tree_prestamos.insert(
          "", "end", values=(p["id_usuario"], u_nom, p["id_libro"], l_tit)
      )

    # Actualizar Estadísticas
    tot_libros = sum(v["copias"] for v in self.libros.values())
    self.lbl_stat_libros.configure(
        text=f"Libros Disponibles: {tot_libros} ({len(self.libros)} Títulos)"
    )
    self.lbl_stat_prestamos.configure(
        text=f"Préstamos Activos: {len(self.prestamos)}"
    )
    self.lbl_stat_users.configure(
        text=f"Usuarios Registrados: {len(self.usuarios)}"
    )


if __name__ == "__main__":
  app = SistemaBibliotecaPro()
  app.mainloop()