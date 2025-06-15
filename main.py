import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
from typing import List, Dict, Any

class GestorTareasGUI:
    def __init__(self):
        self.pendientes: List[str] = []
        self.completados: List[str] = []
        self.nombre_lista: str = ""
        self.tipo_elemento: str = ""
        self.archivo_datos: str = "tareas.json"
        
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("Gestor de Tareas - Interfaz Gráfica")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colores personalizados
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#34495e'
        }
        
        self.configurar_estilos()
        self.crear_interfaz()
        self.cargar_datos()
        
        # Si no hay configuración previa, mostrar diálogo de configuración
        if not self.nombre_lista or not self.tipo_elemento:
            self.root.after(100, self.configurar_lista_inicial)
    
    def configurar_lista_inicial(self):
        """Configuración inicial obligatoria."""
        while not self.nombre_lista or not self.tipo_elemento:
            if not self.configurar_lista():
                # Si el usuario cancela, cerrar la aplicación
                respuesta = messagebox.askyesno(
                    "Configuración requerida", 
                    "La configuración es obligatoria para usar la aplicación.\n¿Desea intentar de nuevo?"
                )
                if not respuesta:
                    self.root.destroy()
                    return
    
    def configurar_estilos(self):
        """Configura los estilos personalizados."""
        try:
            # Configurar estilos para botones
            self.style.configure('Primary.TButton', 
                               font=('Arial', 9, 'bold'))
            
            self.style.configure('Success.TButton', 
                               font=('Arial', 9, 'bold'))
            
            self.style.configure('Warning.TButton', 
                               font=('Arial', 9, 'bold'))
            
            self.style.configure('Danger.TButton', 
                               font=('Arial', 9, 'bold'))
        except Exception as e:
            print(f"Error configurando estilos: {e}")
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica principal."""
        try:
            # Frame principal
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Configurar grid
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(0, weight=1)
            main_frame.rowconfigure(2, weight=1)
            
            # Título
            self.titulo_label = tk.Label(main_frame, 
                                       text="GESTOR DE TAREAS", 
                                       font=('Arial', 20, 'bold'),
                                       fg=self.colors['primary'],
                                       bg='#f0f0f0')
            self.titulo_label.grid(row=0, column=0, pady=(0, 20))
            
            # Frame de configuración
            config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="10")
            config_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            config_frame.columnconfigure(0, weight=1)
            
            # Información de la lista actual
            self.info_frame = ttk.Frame(config_frame)
            self.info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
            
            self.lista_info = tk.Label(self.info_frame, 
                                     text="Lista: No configurada", 
                                     font=('Arial', 12, 'bold'),
                                     fg=self.colors['secondary'],
                                     bg='#f0f0f0')
            self.lista_info.grid(row=0, column=0, sticky=tk.W)
            
            self.tipo_info = tk.Label(self.info_frame, 
                                    text="Tipo: No configurado", 
                                    font=('Arial', 10),
                                    fg=self.colors['dark'],
                                    bg='#f0f0f0')
            self.tipo_info.grid(row=1, column=0, sticky=tk.W)
            
            # Botón configurar
            ttk.Button(config_frame, 
                      text="Configurar Lista", 
                      command=self.configurar_lista).grid(row=0, column=1, padx=(10, 0))
            
            # Frame principal con dos columnas
            content_frame = ttk.Frame(main_frame)
            content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
            content_frame.columnconfigure(0, weight=1)
            content_frame.columnconfigure(1, weight=1)
            content_frame.rowconfigure(0, weight=1)
            
            # Panel izquierdo - Tareas pendientes
            self.crear_panel_pendientes(content_frame)
            
            # Panel derecho - Tareas completadas
            self.crear_panel_completadas(content_frame)
            
            # Panel de botones de acción
            self.crear_panel_botones(main_frame)
            
            # Barra de estado
            self.crear_barra_estado(main_frame)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creando interfaz: {str(e)}")
    
    def crear_panel_pendientes(self, parent):
        """Crea el panel de tareas pendientes."""
        try:
            # Frame pendientes
            pendientes_frame = ttk.LabelFrame(parent, text="📝 Tareas Pendientes", padding="10")
            pendientes_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
            pendientes_frame.columnconfigure(0, weight=1)
            pendientes_frame.rowconfigure(0, weight=1)
            
            # Listbox con scrollbar
            listbox_frame = ttk.Frame(pendientes_frame)
            listbox_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            listbox_frame.columnconfigure(0, weight=1)
            listbox_frame.rowconfigure(0, weight=1)
            
            self.pendientes_listbox = tk.Listbox(listbox_frame, 
                                               font=('Arial', 10),
                                               selectmode=tk.SINGLE,
                                               bg='white',
                                               fg=self.colors['dark'])
            self.pendientes_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            scrollbar1 = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.pendientes_listbox.yview)
            scrollbar1.grid(row=0, column=1, sticky=(tk.N, tk.S))
            self.pendientes_listbox.configure(yscrollcommand=scrollbar1.set)
            
            # Botones para pendientes
            btn_frame1 = ttk.Frame(pendientes_frame)
            btn_frame1.grid(row=1, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
            
            ttk.Button(btn_frame1, text="➕ Agregar", 
                      command=self.agregar_elemento).grid(row=0, column=0, padx=(0, 5))
            
            ttk.Button(btn_frame1, text="🗑️ Eliminar", 
                      command=self.eliminar_elemento).grid(row=0, column=1, padx=5)
            
            ttk.Button(btn_frame1, text="✏️ Editar", 
                      command=self.editar_elemento).grid(row=0, column=2, padx=5)
            
            ttk.Button(btn_frame1, text="✅ Completar", 
                      command=self.marcar_completado).grid(row=0, column=3, padx=(5, 0))
        except Exception as e:
            print(f"Error creando panel pendientes: {e}")
    
    def crear_panel_completadas(self, parent):
        """Crea el panel de tareas completadas."""
        try:
            # Frame completadas
            completadas_frame = ttk.LabelFrame(parent, text="✅ Tareas Completadas", padding="10")
            completadas_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
            completadas_frame.columnconfigure(0, weight=1)
            completadas_frame.rowconfigure(0, weight=1)
            
            # Listbox con scrollbar
            listbox_frame = ttk.Frame(completadas_frame)
            listbox_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            listbox_frame.columnconfigure(0, weight=1)
            listbox_frame.rowconfigure(0, weight=1)
            
            self.completadas_listbox = tk.Listbox(listbox_frame, 
                                                font=('Arial', 10),
                                                selectmode=tk.SINGLE,
                                                bg='#f8f9fa',
                                                fg=self.colors['success'])
            self.completadas_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            scrollbar2 = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.completadas_listbox.yview)
            scrollbar2.grid(row=0, column=1, sticky=(tk.N, tk.S))
            self.completadas_listbox.configure(yscrollcommand=scrollbar2.set)
            
            # Botones para completadas
            btn_frame2 = ttk.Frame(completadas_frame)
            btn_frame2.grid(row=1, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
            
            ttk.Button(btn_frame2, text="↩️ Desmarcar", 
                      command=self.desmarcar_completado).grid(row=0, column=0, padx=(0, 5))
            
            ttk.Button(btn_frame2, text="🗑️ Eliminar", 
                      command=self.eliminar_completado).grid(row=0, column=1, padx=5)
        except Exception as e:
            print(f"Error creando panel completadas: {e}")
    
    def crear_panel_botones(self, parent):
        """Crea el panel de botones de acción."""
        try:
            botones_frame = ttk.LabelFrame(parent, text="Acciones", padding="10")
            botones_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
            
            # Primera fila de botones
            fila1 = ttk.Frame(botones_frame)
            fila1.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
            
            ttk.Button(fila1, text="🔍 Buscar", 
                      command=self.buscar_elemento).grid(row=0, column=0, padx=(0, 5))
            
            ttk.Button(fila1, text="📊 Estadísticas", 
                      command=self.mostrar_estadisticas).grid(row=0, column=1, padx=5)
            
            ttk.Button(fila1, text="💾 Guardar", 
                      command=self.guardar_datos).grid(row=0, column=2, padx=5)
            
            ttk.Button(fila1, text="🔄 Actualizar", 
                      command=self.actualizar_listas).grid(row=0, column=3, padx=5)
            
            # Segunda fila de botones
            fila2 = ttk.Frame(botones_frame)
            fila2.grid(row=1, column=0, sticky=(tk.W, tk.E))
            
            ttk.Button(fila2, text="📤 Exportar", 
                      command=self.exportar_datos).grid(row=0, column=0, padx=(0, 5))
            
            ttk.Button(fila2, text="📥 Importar", 
                      command=self.importar_datos).grid(row=0, column=1, padx=5)
            
            ttk.Button(fila2, text="🧹 Limpiar Todo", 
                      command=self.limpiar_todo).grid(row=0, column=2, padx=5)
        except Exception as e:
            print(f"Error creando panel botones: {e}")
    
    def crear_barra_estado(self, parent):
        """Crea la barra de estado."""
        try:
            self.status_frame = ttk.Frame(parent)
            self.status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
            
            self.status_label = tk.Label(self.status_frame, 
                                       text="Listo", 
                                       font=('Arial', 9),
                                       fg=self.colors['dark'],
                                       bg='#f0f0f0',
                                       relief=tk.SUNKEN,
                                       anchor=tk.W)
            self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
            
            self.contador_label = tk.Label(self.status_frame, 
                                         text="Pendientes: 0 | Completadas: 0", 
                                         font=('Arial', 9),
                                         fg=self.colors['secondary'],
                                         bg='#f0f0f0',
                                         relief=tk.SUNKEN)
            self.contador_label.grid(row=0, column=1, sticky=tk.E)
            
            self.status_frame.columnconfigure(0, weight=1)
        except Exception as e:
            print(f"Error creando barra estado: {e}")
    
    def actualizar_info_lista(self):
        """Actualiza la información de la lista en la interfaz."""
        try:
            if self.nombre_lista:
                self.lista_info.config(text=f"Lista: {self.nombre_lista}")
                self.tipo_info.config(text=f"Tipo: {self.tipo_elemento}")
                self.titulo_label.config(text=f"GESTOR DE {self.nombre_lista.upper()}")
            else:
                self.lista_info.config(text="Lista: No configurada")
                self.tipo_info.config(text="Tipo: No configurado")
        except Exception as e:
            print(f"Error actualizando info: {e}")
    
    def actualizar_listas(self):
        """Actualiza las listas en la interfaz."""
        try:
            # Limpiar listas
            self.pendientes_listbox.delete(0, tk.END)
            self.completadas_listbox.delete(0, tk.END)
            
            # Agregar elementos pendientes
            for elemento in self.pendientes:
                self.pendientes_listbox.insert(tk.END, elemento)
            
            # Agregar elementos completados
            for elemento in self.completados:
                self.completadas_listbox.insert(tk.END, elemento)
            
            # Actualizar contador
            self.contador_label.config(
                text=f"Pendientes: {len(self.pendientes)} | Completadas: {len(self.completados)}"
            )
        except Exception as e:
            print(f"Error actualizando listas: {e}")
    
    def actualizar_status(self, mensaje: str):
        """Actualiza la barra de estado."""
        try:
            self.status_label.config(text=mensaje)
            self.root.after(3000, lambda: self.status_label.config(text="Listo"))
        except Exception as e:
            print(f"Error actualizando status: {e}")
    
    def configurar_lista(self) -> bool:
        """Abre diálogo para configurar la lista."""
        try:
            # Usar diálogos simples en lugar de ventana personalizada
            nombre = simpledialog.askstring(
                "Configurar Lista", 
                "Ingrese el nombre de su lista:",
                initialvalue=self.nombre_lista,
                parent=self.root
            )
            
            if not nombre or not nombre.strip():
                return False
            
            tipo = simpledialog.askstring(
                "Configurar Lista", 
                "Ingrese el tipo de elemento (ej: tarea, producto, etc.):",
                initialvalue=self.tipo_elemento,
                parent=self.root
            )
            
            if not tipo or not tipo.strip():
                return False
            
            # Guardar configuración
            self.nombre_lista = nombre.strip().title()
            self.tipo_elemento = tipo.strip().lower()
            
            # Actualizar interfaz
            self.actualizar_info_lista()
            self.actualizar_status("Lista configurada exitosamente")
            
            # Guardar automáticamente
            self.guardar_datos()
            
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error configurando lista: {str(e)}")
            return False
    
    def agregar_elemento(self):
        """Agrega un nuevo elemento."""
        try:
            if not self.nombre_lista or not self.tipo_elemento:
                messagebox.showwarning("Configuración requerida", 
                                     "Primero debe configurar el nombre de la lista y tipo de elemento.")
                self.configurar_lista()
                return
            
            elemento = simpledialog.askstring("Agregar Elemento", 
                                            f"Ingrese el {self.tipo_elemento}:",
                                            parent=self.root)
            if elemento and elemento.strip():
                elemento = elemento.strip().title()
                if elemento not in self.pendientes:
                    self.pendientes.append(elemento)
                    self.actualizar_listas()
                    self.actualizar_status(f"'{elemento}' agregado exitosamente")
                    # Guardar automáticamente después de agregar
                    self.guardar_datos()
                else:
                    messagebox.showwarning("Elemento duplicado", 
                                         f"'{elemento}' ya existe en la lista.")
        except Exception as e:
            messagebox.showerror("Error", f"Error agregando elemento: {str(e)}")
    
    def eliminar_elemento(self):
        """Elimina el elemento seleccionado de pendientes."""
        try:
            seleccion = self.pendientes_listbox.curselection()
            if seleccion:
                indice = seleccion[0]
                elemento = self.pendientes[indice]
                if messagebox.askyesno("Confirmar eliminación", 
                                     f"¿Está seguro de eliminar '{elemento}'?"):
                    self.pendientes.pop(indice)
                    self.actualizar_listas()
                    self.actualizar_status(f"'{elemento}' eliminado exitosamente")
                    self.guardar_datos()
            else:
                messagebox.showwarning("Selección requerida", 
                                     "Seleccione un elemento para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Error eliminando elemento: {str(e)}")
    
    def editar_elemento(self):
        """Edita el elemento seleccionado."""
        try:
            seleccion = self.pendientes_listbox.curselection()
            if seleccion:
                indice = seleccion[0]
                elemento_actual = self.pendientes[indice]
                nuevo_elemento = simpledialog.askstring("Editar Elemento", 
                                                       f"Edite el {self.tipo_elemento}:",
                                                       initialvalue=elemento_actual,
                                                       parent=self.root)
                if nuevo_elemento and nuevo_elemento.strip():
                    nuevo_elemento = nuevo_elemento.strip().title()
                    self.pendientes[indice] = nuevo_elemento
                    self.actualizar_listas()
                    self.actualizar_status(f"Elemento editado exitosamente")
                    self.guardar_datos()
            else:
                messagebox.showwarning("Selección requerida", 
                                     "Seleccione un elemento para editar.")
        except Exception as e:
            messagebox.showerror("Error", f"Error editando elemento: {str(e)}")
    
    def marcar_completado(self):
        """Marca el elemento seleccionado como completado."""
        try:
            seleccion = self.pendientes_listbox.curselection()
            if seleccion:
                indice = seleccion[0]
                elemento = self.pendientes.pop(indice)
                self.completados.append(elemento)
                self.actualizar_listas()
                self.actualizar_status(f"'{elemento}' marcado como completado")
                self.guardar_datos()
            else:
                messagebox.showwarning("Selección requerida", 
                                     "Seleccione un elemento para marcar como completado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error marcando completado: {str(e)}")
    
    def desmarcar_completado(self):
        """Desmarca el elemento seleccionado como completado."""
        try:
            seleccion = self.completadas_listbox.curselection()
            if seleccion:
                indice = seleccion[0]
                elemento = self.completados.pop(indice)
                self.pendientes.append(elemento)
                self.actualizar_listas()
                self.actualizar_status(f"'{elemento}' desmarcado como completado")
                self.guardar_datos()
            else:
                messagebox.showwarning("Selección requerida", 
                                     "Seleccione un elemento para desmarcar.")
        except Exception as e:
            messagebox.showerror("Error", f"Error desmarcando completado: {str(e)}")
    
    def eliminar_completado(self):
        """Elimina el elemento seleccionado de completados."""
        try:
            seleccion = self.completadas_listbox.curselection()
            if seleccion:
                indice = seleccion[0]
                elemento = self.completados[indice]
                if messagebox.askyesno("Confirmar eliminación", 
                                     f"¿Está seguro de eliminar '{elemento}'?"):
                    self.completados.pop(indice)
                    self.actualizar_listas()
                    self.actualizar_status(f"'{elemento}' eliminado exitosamente")
                    self.guardar_datos()
            else:
                messagebox.showwarning("Selección requerida", 
                                     "Seleccione un elemento para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Error eliminando completado: {str(e)}")
    
    def buscar_elemento(self):
        """Busca un elemento en las listas."""
        try:
            termino = simpledialog.askstring("Buscar Elemento", 
                                            "Ingrese el término a buscar:",
                                            parent=self.root)
            if termino:
                termino = termino.strip().lower()
                encontrados_pendientes = [i for i, item in enumerate(self.pendientes) 
                                        if termino in item.lower()]
                encontrados_completados = [i for i, item in enumerate(self.completados) 
                                         if termino in item.lower()]
                
                resultado = f"Búsqueda: '{termino}'\n\n"
                resultado += f"Encontrado en pendientes: {len(encontrados_pendientes)} elemento(s)\n"
                resultado += f"Encontrado en completados: {len(encontrados_completados)} elemento(s)"
                
                messagebox.showinfo("Resultados de búsqueda", resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Error buscando elemento: {str(e)}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas detalladas."""
        try:
            total_pendientes = len(self.pendientes)
            total_completados = len(self.completados)
            total = total_pendientes + total_completados
            
            if total > 0:
                porcentaje_completado = (total_completados / total) * 100
            else:
                porcentaje_completado = 0
            
            estado = ('¡Excelente progreso!' if porcentaje_completado >= 70 else 
                     '¡Buen progreso!' if porcentaje_completado >= 40 else 
                     '¡Continúa así!')
            
            estadisticas = f"""📊 ESTADÍSTICAS DE {self.nombre_lista.upper() if self.nombre_lista else 'TAREAS'}

📝 Elementos pendientes: {total_pendientes}
✅ Elementos completados: {total_completados}
📋 Total de elementos: {total}
📈 Porcentaje completado: {porcentaje_completado:.1f}%

🎯 Estado: {estado}"""
            
            messagebox.showinfo("Estadísticas", estadisticas)
        except Exception as e:
            messagebox.showerror("Error", f"Error mostrando estadísticas: {str(e)}")
    
    def exportar_datos(self):
        """Exporta los datos a un archivo de texto."""
        try:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                title="Exportar datos"
            )
            
            if archivo:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(f"=== {self.nombre_lista.upper() if self.nombre_lista else 'TAREAS'} ===\n\n")
                    f.write("📝 ELEMENTOS PENDIENTES:\n")
                    for i, elemento in enumerate(self.pendientes, 1):
                        f.write(f"{i}. {elemento}\n")
                    
                    f.write(f"\n✅ ELEMENTOS COMPLETADOS:\n")
                    for i, elemento in enumerate(self.completados, 1):
                        f.write(f"{i}. {elemento}\n")
                
                self.actualizar_status("Datos exportados exitosamente")
                messagebox.showinfo("Exportación exitosa", f"Datos exportados a: {archivo}")
        except Exception as e:
            messagebox.showerror("Error de exportación", f"Error al exportar: {str(e)}")
    
    def importar_datos(self):
        """Importa datos desde un archivo JSON."""
        try:
            archivo = filedialog.askopenfilename(
                filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
                title="Importar datos"
            )
            
            if archivo:
                with open(archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.pendientes = datos.get('pendientes', [])
                    self.completados = datos.get('completados', [])
                    self.nombre_lista = datos.get('nombre_lista', '')
                    self.tipo_elemento = datos.get('tipo_elemento', '')
                
                self.actualizar_info_lista()
                self.actualizar_listas()
                self.actualizar_status("Datos importados exitosamente")
                messagebox.showinfo("Importación exitosa", "Datos importados correctamente")
        except Exception as e:
            messagebox.showerror("Error de importación", f"Error al importar: {str(e)}")
    
    def limpiar_todo(self):
        """Limpia todas las listas."""
        try:
            if messagebox.askyesno("Confirmar limpieza", 
                                 "¿Está seguro de eliminar todos los elementos?"):
                self.pendientes.clear()
                self.completados.clear()
                self.actualizar_listas()
                self.actualizar_status("Todas las listas han sido limpiadas")
                self.guardar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"Error limpiando listas: {str(e)}")
    
    def cargar_datos(self) -> bool:
        """Carga los datos desde un archivo JSON si existe."""
        try:
            if os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    self.pendientes = datos.get('pendientes', [])
                    self.completados = datos.get('completados', [])
                    self.nombre_lista = datos.get('nombre_lista', '')
                    self.tipo_elemento = datos.get('tipo_elemento', '')
                self.actualizar_info_lista()
                self.actualizar_listas()
                return True
            return True
        except Exception as e:
            print(f"Error cargando datos: {e}")
            return False
    
    def guardar_datos(self) -> bool:
        """Guarda los datos en un archivo JSON."""
        try:
            datos = {
                'pendientes': self.pendientes,
                'completados': self.completados,
                'nombre_lista': self.nombre_lista,
                'tipo_elemento': self.tipo_elemento
            }
            with open(self.archivo_datos, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando datos: {e}")
            return False
    
    def al_cerrar(self):
        """Maneja el evento de cierre de la ventana."""
        try:
            if messagebox.askyesno("Confirmar salida", "¿Desea guardar antes de salir?"):
                self.guardar_datos()
            self.root.destroy()
        except Exception as e:
            print(f"Error al cerrar: {e}")
            self.root.destroy()
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.al_cerrar)
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error crítico", f"Error ejecutando aplicación: {str(e)}")


def main():
    """Función principal."""
    try:
        app = GestorTareasGUI()
        app.ejecutar()
    except Exception as e:
        print(f"Error crítico en main: {e}")
        if tk._default_root:
            messagebox.showerror("Error Crítico", f"Error iniciando aplicación: {str(e)}")


if __name__ == "__main__":
    main()