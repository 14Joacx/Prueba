
import sqlite3

from config.database import Database
from models.entidades import (
    Empleado, Departamento, Proyecto, RegistroTiempo
)
from models.dao import (
    EmpleadoDAO, DepartamentoDAO, ProyectoDAO, RegistroTiempoDAO
)
from views.main_view import MainView


class MainController:
    def __init__(self):
        self.view = MainView()
        self.empleados = EmpleadoDAO()
        self.departamentos = DepartamentoDAO()
        self.proyectos = ProyectoDAO()
        self.registros = RegistroTiempoDAO()
        Database().inicializar()

    def ejecutar(self):
        while True:
            try:
                opcion = self.view.menu_principal()

                if opcion == 0:
                    self.view.mensaje("Programa finalizado.")
                    break
                elif opcion == 1:
                    self.menu_empleados()
                elif opcion == 2:
                    self.menu_departamentos()
                elif opcion == 3:
                    self.menu_proyectos()
                elif opcion == 4:
                    self.menu_registros()
                else:
                    self.view.mensaje("Opción no válida.")

            except sqlite3.IntegrityError:
                self.view.mensaje(
                    "No se pudo guardar. Puede que el dato ya exista "
                    "o que falte una relación válida."
                )
            except (ValueError, TypeError) as error:
                self.view.mensaje(str(error))
            except sqlite3.Error as error:
                self.view.mensaje(f"Error de base de datos: {error}")

    def pedir_empleado(self):
        nombre = self.view.texto("Nombre: ")
        apellido = self.view.texto("Apellido: ")
        direccion = self.view.texto("Dirección: ")
        telefono = self.view.texto("Teléfono: ")
        correo = self.view.texto("Correo: ")
        fecha = self.view.texto("Fecha de inicio (AAAA-MM-DD): ")
        salario = self.view.decimal("Salario: ")

        return Empleado(
            nombre, apellido, direccion, telefono,
            correo, fecha, salario
        )

    def menu_empleados(self):
        while True:
            opcion = self.view.menu_crud("Empleados")

            if opcion == 0:
                break
            elif opcion == 1:
                empleado = self.pedir_empleado()
                nuevo_id = self.empleados.crear(empleado)
                self.view.mensaje(f"Empleado registrado con ID {nuevo_id}.")
            elif opcion == 2:
                self.view.mostrar_empleados(self.empleados.listar())
            elif opcion == 3:
                empleado_id = self.view.numero("ID del empleado: ")
                empleado = self.empleados.buscar(empleado_id)
                if empleado:
                    self.view.mostrar_empleados([empleado])
                else:
                    self.view.mensaje("No se encontró el empleado.")
            elif opcion == 4:
                empleado_id = self.view.numero("ID a actualizar: ")
                if not self.empleados.buscar(empleado_id):
                    self.view.mensaje("No se encontró el empleado.")
                    continue
                empleado = self.pedir_empleado()
                if self.empleados.actualizar(empleado_id, empleado):
                    self.view.mensaje("Empleado actualizado.")
            elif opcion == 5:
                empleado_id = self.view.numero("ID a eliminar: ")
                if self.empleados.eliminar(empleado_id):
                    self.view.mensaje("Empleado eliminado.")
                else:
                    self.view.mensaje("No se encontró el empleado.")
            else:
                self.view.mensaje("Opción no válida.")

    def menu_departamentos(self):
        while True:
            print("\n--- DEPARTAMENTOS ---")
            print("1. Registrar departamento")
            print("2. Listar departamentos")
            print("3. Asignar empleado a departamento")
            print("4. Eliminar departamento")
            print("5. Buscar empleados por ID de departamento")
            print("0. Volver")
            opcion = self.view.numero("Seleccione: ")

            if opcion == 0:
                break
            elif opcion == 1:
                nombre = self.view.texto("Nombre del departamento: ")
                gerente = self.view.texto(
                    "ID del gerente (Enter si no tiene): "
                )
                gerente_id = int(gerente) if gerente else None
                departamento = Departamento(nombre, gerente_id)
                nuevo_id = self.departamentos.crear(
                    departamento.nombre, departamento.gerente_id
                )
                self.view.mensaje(
                    f"Departamento creado con ID {nuevo_id}."
                )
            elif opcion == 2:
                self.view.mostrar_departamentos(
                    self.departamentos.listar()
                )
            elif opcion == 3:
                empleado_id = self.view.numero("ID del empleado: ")
                departamento_id = self.view.numero("ID del departamento: ")
                self.departamentos.asignar_empleado(
                    empleado_id, departamento_id
                )
                self.view.mensaje("Empleado asignado al departamento.")
            elif opcion == 4:
                departamento_id = self.view.numero(
                    "ID del departamento a eliminar: "
                )
                if self.departamentos.eliminar(departamento_id):
                    self.view.mensaje("Departamento eliminado.")
                else:
                    self.view.mensaje("No se encontró el departamento.")
            elif opcion == 5:
                departamento_id = self.view.numero(
                    "ID del departamento: "
                )

                departamento = self.departamentos.buscar(departamento_id)

                if not departamento:
                    self.view.mensaje("No se encontró el departamento.")
                    continue

                empleados = self.departamentos.listar_empleados(
                    departamento_id
                )

                print(
                    f"\nEmpleados del departamento "
                    f"{departamento['nombre']} "
                    f"(ID {departamento_id}):"
                )

                if not empleados:
                    self.view.mensaje(
                        "No hay empleados asignados a este departamento."
                    )
                else:
                    for empleado in empleados:
                        print(
                            f"ID: {empleado['id']} | "
                            f"Nombre: {empleado['nombre']} "
                            f"{empleado['apellido']} | "
                            f"Teléfono: {empleado['telefono']} | "
                            f"Correo: {empleado['correo']}"
                        )


    def menu_proyectos(self):
        while True:
            print("\n--- PROYECTOS ---")
            print("1. Registrar proyecto")
            print("2. Listar proyectos")
            print("3. Asignar empleado a proyecto")
            print("4. Ver asignaciones")
            print("5. Eliminar proyecto")
            print("0. Volver")
            opcion = self.view.numero("Seleccione: ")

            if opcion == 0:
                break
            elif opcion == 1:
                nombre = self.view.texto("Nombre: ")
                descripcion = self.view.texto("Descripción: ")
                fecha = self.view.texto("Fecha de inicio (AAAA-MM-DD): ")
                proyecto = Proyecto(nombre, descripcion, fecha)
                nuevo_id = self.proyectos.crear(
                    proyecto.nombre, proyecto.descripcion,
                    proyecto.fecha_inicio
                )
                self.view.mensaje(f"Proyecto creado con ID {nuevo_id}.")
            elif opcion == 2:
                self.view.mostrar_proyectos(self.proyectos.listar())
            elif opcion == 3:
                empleado_id = self.view.numero("ID del empleado: ")
                proyecto_id = self.view.numero("ID del proyecto: ")
                self.proyectos.asignar_empleado(empleado_id, proyecto_id)
                self.view.mensaje("Empleado asignado al proyecto.")
            elif opcion == 4:
                asignaciones = self.proyectos.listar_asignaciones()
                if not asignaciones:
                    self.view.mensaje("No hay asignaciones.")
                for a in asignaciones:
                    print(
                        f"Empleado: {a['empleado']} (ID {a['empleado_id']}) "
                        f"| Proyecto: {a['proyecto']} (ID {a['proyecto_id']})"
                    )
            elif opcion == 5:
                proyecto_id = self.view.numero("ID del proyecto: ")
                if self.proyectos.eliminar(proyecto_id):
                    self.view.mensaje("Proyecto eliminado.")
                else:
                    self.view.mensaje("No se encontró el proyecto.")
            else:
                self.view.mensaje("Opción no válida.")

    def menu_registros(self):
        while True:
            print("\n--- REGISTROS DE TIEMPO ---")
            print("1. Registrar horas")
            print("2. Listar registros")
            print("3. Eliminar registro")
            print("0. Volver")
            opcion = self.view.numero("Seleccione: ")

            if opcion == 0:
                break
            elif opcion == 1:
                empleado_id = self.view.numero("ID del empleado: ")
                proyecto_id = self.view.numero("ID del proyecto: ")
                fecha = self.view.texto("Fecha (AAAA-MM-DD): ")
                horas = self.view.decimal("Cantidad de horas: ")
                descripcion = self.view.texto("Descripción del trabajo: ")

                registro = RegistroTiempo(
                    empleado_id, proyecto_id, fecha, horas, descripcion
                )
                nuevo_id = self.registros.crear(registro)
                self.view.mensaje(
                    f"Registro de tiempo guardado con ID {nuevo_id}."
                )
            elif opcion == 2:
                self.view.mostrar_registros(self.registros.listar())
            elif opcion == 3:
                registro_id = self.view.numero("ID del registro: ")
                if self.registros.eliminar(registro_id):
                    self.view.mensaje("Registro eliminado.")
                else:
                    self.view.mensaje("No se encontró el registro.")
            else:
                self.view.mensaje("Opción no válida.")
