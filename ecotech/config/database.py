
import sqlite3
from pathlib import Path


class Database:
    def __init__(self):
        carpeta = Path(__file__).resolve().parent.parent
        self.ruta = carpeta / "ecotech.db"

    def conectar(self):
        conexion = sqlite3.connect(self.ruta)
        conexion.row_factory = sqlite3.Row
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    def inicializar(self):
        conexion = self.conectar()

        try:
            conexion.executescript("""
                CREATE TABLE IF NOT EXISTS empleado (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL DEFAULT '',
                    direccion TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    correo TEXT NOT NULL UNIQUE,
                    fecha_inicio TEXT NOT NULL,
                    salario REAL NOT NULL CHECK (salario >= 0)
                );

                CREATE TABLE IF NOT EXISTS departamento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    gerente_id INTEGER,
                    FOREIGN KEY (gerente_id)
                        REFERENCES empleado(id)
                        ON DELETE SET NULL
                );

                CREATE TABLE IF NOT EXISTS empleado_departamento (
                    empleado_id INTEGER PRIMARY KEY,
                    departamento_id INTEGER NOT NULL,
                    FOREIGN KEY (empleado_id)
                        REFERENCES empleado(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (departamento_id)
                        REFERENCES departamento(id)
                        ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS proyecto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    fecha_inicio TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS empleado_proyecto (
                    empleado_id INTEGER NOT NULL,
                    proyecto_id INTEGER NOT NULL,
                    PRIMARY KEY (empleado_id, proyecto_id),
                    FOREIGN KEY (empleado_id)
                        REFERENCES empleado(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (proyecto_id)
                        REFERENCES proyecto(id)
                        ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS registro_tiempo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    empleado_id INTEGER NOT NULL,
                    proyecto_id INTEGER NOT NULL,
                    fecha TEXT NOT NULL,
                    horas REAL NOT NULL CHECK (horas > 0),
                    descripcion TEXT NOT NULL,
                    FOREIGN KEY (empleado_id)
                        REFERENCES empleado(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (proyecto_id)
                        REFERENCES proyecto(id)
                        ON DELETE CASCADE
                );
            """)

            columnas = [
                fila["name"]
                for fila in conexion.execute(
                    "PRAGMA table_info(empleado)"
                ).fetchall()
            ]

            if "apellido" not in columnas:
                conexion.execute("""
                    ALTER TABLE empleado
                    ADD COLUMN apellido TEXT NOT NULL DEFAULT ''
                """)

            conexion.commit()

        except sqlite3.Error:
            conexion.rollback()
            raise
        finally:
            conexion.close()
