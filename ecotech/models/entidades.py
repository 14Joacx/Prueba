
class Empleado:
    def __init__(self, nombre, apellido, direccion, telefono,
                 correo, fecha_inicio, salario):
        self._nombre = self._validar_texto(nombre, "nombre")
        self._apellido = self._validar_texto(apellido, "apellido")
        self._direccion = self._validar_texto(direccion, "dirección")
        self._telefono = self._validar_texto(telefono, "teléfono")
        self._correo = self._validar_texto(correo, "correo")
        self._fecha_inicio = self._validar_texto(fecha_inicio, "fecha de inicio")

        if "@" not in self._correo or "." not in self._correo:
            raise ValueError("El correo no tiene un formato válido.")

        try:
            self._salario = float(salario)
        except (ValueError, TypeError):
            raise ValueError("El salario debe ser numérico.")

        if self._salario < 0:
            raise ValueError("El salario no puede ser negativo.")

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"El campo {campo} es obligatorio.")
        return valor.strip()

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido

    @property
    def direccion(self):
        return self._direccion

    @property
    def telefono(self):
        return self._telefono

    @property
    def correo(self):
        return self._correo

    @property
    def fecha_inicio(self):
        return self._fecha_inicio

    @property
    def salario(self):
        return self._salario

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.correo}"


class Departamento:
    def __init__(self, nombre, gerente_id=None):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del departamento es obligatorio.")
        self.nombre = nombre.strip()
        self.gerente_id = gerente_id


class Proyecto:
    def __init__(self, nombre, descripcion, fecha_inicio):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del proyecto es obligatorio.")
        if not descripcion or not descripcion.strip():
            raise ValueError("La descripción es obligatoria.")
        if not fecha_inicio or not fecha_inicio.strip():
            raise ValueError("La fecha de inicio es obligatoria.")

        self.nombre = nombre.strip()
        self.descripcion = descripcion.strip()
        self.fecha_inicio = fecha_inicio.strip()


class RegistroTiempo:
    def __init__(self, empleado_id, proyecto_id, fecha, horas, descripcion):
        self.empleado_id = int(empleado_id)
        self.proyecto_id = int(proyecto_id)

        if not fecha or not fecha.strip():
            raise ValueError("La fecha es obligatoria.")
        if not descripcion or not descripcion.strip():
            raise ValueError("La descripción es obligatoria.")

        try:
            self.horas = float(horas)
        except (ValueError, TypeError):
            raise ValueError("Las horas deben ser numéricas.")

        if self.horas <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")

        self.fecha = fecha.strip()
        self.descripcion = descripcion.strip()
