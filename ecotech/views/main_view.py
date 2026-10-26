
class MainView:
    def menu_principal(self):
        print("\n===== ECOTECH SOLUTIONS =====")
        print("1. Gestionar empleados")
        print("2. Gestionar departamentos")
        print("3. Gestionar proyectos")
        print("4. Gestionar registros de tiempo")
        print("0. Salir")
        return self.numero("Seleccione una opción: ")

    def menu_crud(self, nombre):
        print(f"\n--- {nombre.upper()} ---")
        print("1. Registrar")
        print("2. Listar")
        print("3. Buscar por ID (solo empleados)")
        print("4. Actualizar (solo empleados)")
        print("5. Eliminar")
        print("0. Volver")
        return self.numero("Seleccione una opción: ")

    def numero(self, mensaje):
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print("Error: ingrese un número entero.")

    def decimal(self, mensaje):
        while True:
            try:
                return float(input(mensaje).replace(",", "."))
            except ValueError:
                print("Error: ingrese un número válido.")

    def texto(self, mensaje):
        return input(mensaje).strip()

    def mostrar_empleados(self, empleados):
        if not empleados:
            print("No hay empleados registrados.")
            return
        for e in empleados:
            print(
                f"ID: {e['id']} | {e['nombre']} {e['apellido']} | "
                f"Correo: {e['correo']} | Teléfono: {e['telefono']} | "
                f"Salario: ${e['salario']:.2f}"
            )

    def mostrar_departamentos(self, departamentos):
        if not departamentos:
            print("No hay departamentos registrados.")
            return
        for d in departamentos:
            gerente = d["gerente"] or "Sin gerente asignado"
            print(f"ID: {d['id']} | {d['nombre']} | Gerente: {gerente}")

    def mostrar_proyectos(self, proyectos):
        if not proyectos:
            print("No hay proyectos registrados.")
            return
        for p in proyectos:
            print(
                f"ID: {p['id']} | {p['nombre']} | "
                f"Inicio: {p['fecha_inicio']} | {p['descripcion']}"
            )

    def mostrar_registros(self, registros):
        if not registros:
            print("No hay registros de tiempo.")
            return
        for r in registros:
            print(
                f"ID: {r['id']} | Fecha: {r['fecha']} | "
                f"Empleado: {r['empleado']} | Proyecto: {r['proyecto']} | "
                f"Horas: {r['horas']} | {r['descripcion']}"
            )

    def mensaje(self, texto):
        print(f"[SISTEMA] {texto}")
