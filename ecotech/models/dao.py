
from config.database import Database


class EmpleadoDAO:
    def __init__(self):
        self.db = Database()

    def crear(self, empleado):
        with self.db.conectar() as con:
            cursor = con.execute("""
                INSERT INTO empleado
                (nombre, apellido, direccion, telefono, correo,
                 fecha_inicio, salario)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                empleado.nombre, empleado.apellido, empleado.direccion,
                empleado.telefono, empleado.correo, empleado.fecha_inicio,
                empleado.salario
            ))
            return cursor.lastrowid

    def listar(self):
        with self.db.conectar() as con:
            return con.execute(
                "SELECT * FROM empleado ORDER BY id"
            ).fetchall()

    def buscar(self, empleado_id):
        with self.db.conectar() as con:
            return con.execute(
                "SELECT * FROM empleado WHERE id = ?", (empleado_id,)
            ).fetchone()

    def actualizar(self, empleado_id, empleado):
        with self.db.conectar() as con:
            cursor = con.execute("""
                UPDATE empleado
                SET nombre=?, apellido=?, direccion=?, telefono=?,
                    correo=?, fecha_inicio=?, salario=?
                WHERE id=?
            """, (
                empleado.nombre, empleado.apellido, empleado.direccion,
                empleado.telefono, empleado.correo, empleado.fecha_inicio,
                empleado.salario, empleado_id
            ))
            return cursor.rowcount > 0

    def eliminar(self, empleado_id):
        with self.db.conectar() as con:
            cursor = con.execute(
                "DELETE FROM empleado WHERE id=?", (empleado_id,)
            )
            return cursor.rowcount > 0


class DepartamentoDAO:
    def __init__(self):
        self.db = Database()

    def crear(self, nombre, gerente_id=None):
        with self.db.conectar() as con:
            cursor = con.execute(
                "INSERT INTO departamento (nombre, gerente_id) VALUES (?, ?)",
                (nombre, gerente_id)
            )
            return cursor.lastrowid

    def listar(self):
        with self.db.conectar() as con:
            return con.execute("""
                SELECT d.id, d.nombre, d.gerente_id,
                       e.nombre || ' ' || e.apellido AS gerente
                FROM departamento d
                LEFT JOIN empleado e ON d.gerente_id = e.id
                ORDER BY d.id
            """).fetchall()

    def eliminar(self, departamento_id):
        with self.db.conectar() as con:
            cursor = con.execute(
                "DELETE FROM departamento WHERE id=?", (departamento_id,)
            )
            return cursor.rowcount > 0

    def asignar_empleado(self, empleado_id, departamento_id):
        with self.db.conectar() as con:
            existe = con.execute(
                "SELECT id FROM empleado WHERE id=?", (empleado_id,)
            ).fetchone()
            if not existe:
                raise ValueError("El empleado no existe.")

            existe = con.execute(
                "SELECT id FROM departamento WHERE id=?", (departamento_id,)
            ).fetchone()
            if not existe:
                raise ValueError("El departamento no existe.")

            con.execute("""
                INSERT INTO empleado_departamento
                (empleado_id, departamento_id)
                VALUES (?, ?)
                ON CONFLICT(empleado_id)
                DO UPDATE SET departamento_id=excluded.departamento_id
            """, (empleado_id, departamento_id))
    
    def buscar(self, departamento_id):
        with self.db.conectar() as con:
            return con.execute(
                "SELECT * FROM departamento WHERE id = ?",
                (departamento_id,)
            ).fetchone()

    def listar_empleados(self, departamento_id):
        with self.db.conectar() as con:
            return con.execute("""
                SELECT e.id, e.nombre, e.apellido,
                       e.telefono, e.correo
                FROM empleado e
                INNER JOIN empleado_departamento ed
                    ON e.id = ed.empleado_id
                WHERE ed.departamento_id = ?
                ORDER BY e.apellido, e.nombre
            """, (departamento_id,)).fetchall()



class ProyectoDAO:
    def __init__(self):
        self.db = Database()

    def crear(self, nombre, descripcion, fecha_inicio):
        with self.db.conectar() as con:
            cursor = con.execute("""
                INSERT INTO proyecto (nombre, descripcion, fecha_inicio)
                VALUES (?, ?, ?)
            """, (nombre, descripcion, fecha_inicio))
            return cursor.lastrowid

    def listar(self):
        with self.db.conectar() as con:
            return con.execute(
                "SELECT * FROM proyecto ORDER BY id"
            ).fetchall()

    def eliminar(self, proyecto_id):
        with self.db.conectar() as con:
            cursor = con.execute(
                "DELETE FROM proyecto WHERE id=?", (proyecto_id,)
            )
            return cursor.rowcount > 0

    def asignar_empleado(self, empleado_id, proyecto_id):
        with self.db.conectar() as con:
            empleado = con.execute(
                "SELECT id FROM empleado WHERE id=?", (empleado_id,)
            ).fetchone()
            proyecto = con.execute(
                "SELECT id FROM proyecto WHERE id=?", (proyecto_id,)
            ).fetchone()

            if not empleado:
                raise ValueError("El empleado no existe.")
            if not proyecto:
                raise ValueError("El proyecto no existe.")

            con.execute("""
                INSERT OR IGNORE INTO empleado_proyecto
                (empleado_id, proyecto_id) VALUES (?, ?)
            """, (empleado_id, proyecto_id))

    def listar_asignaciones(self):
        with self.db.conectar() as con:
            return con.execute("""
                SELECT e.id AS empleado_id,
                       e.nombre || ' ' || e.apellido AS empleado,
                       p.id AS proyecto_id, p.nombre AS proyecto
                FROM empleado_proyecto ep
                JOIN empleado e ON ep.empleado_id = e.id
                JOIN proyecto p ON ep.proyecto_id = p.id
                ORDER BY p.nombre, e.apellido
            """).fetchall()


class RegistroTiempoDAO:
    def __init__(self):
        self.db = Database()

    def crear(self, registro):
        with self.db.conectar() as con:
            asignacion = con.execute("""
                SELECT 1 FROM empleado_proyecto
                WHERE empleado_id=? AND proyecto_id=?
            """, (registro.empleado_id, registro.proyecto_id)).fetchone()

            if not asignacion:
                raise ValueError(
                    "Asigna primero al empleado al proyecto correspondiente."
                )

            cursor = con.execute("""
                INSERT INTO registro_tiempo
                (empleado_id, proyecto_id, fecha, horas, descripcion)
                VALUES (?, ?, ?, ?, ?)
            """, (
                registro.empleado_id, registro.proyecto_id,
                registro.fecha, registro.horas, registro.descripcion
            ))
            return cursor.lastrowid

    def listar(self):
        with self.db.conectar() as con:
            return con.execute("""
                SELECT r.id, r.fecha, r.horas, r.descripcion,
                       e.nombre || ' ' || e.apellido AS empleado,
                       p.nombre AS proyecto
                FROM registro_tiempo r
                JOIN empleado e ON r.empleado_id=e.id
                JOIN proyecto p ON r.proyecto_id=p.id
                ORDER BY r.fecha DESC, r.id DESC
            """).fetchall()

    def eliminar(self, registro_id):
        with self.db.conectar() as con:
            cursor = con.execute(
                "DELETE FROM registro_tiempo WHERE id=?", (registro_id,)
            )
            return cursor.rowcount > 0
