import os
import psycopg2
import psycopg2.extras


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "SistemasDistribuidos"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "1253"),
    )


def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS vehicles (
                    matricula VARCHAR(20) PRIMARY KEY,
                    vin VARCHAR(40) UNIQUE NOT NULL,
                    modelo VARCHAR(60) NOT NULL,
                    marca VARCHAR(60) NOT NULL,
                    tipo VARCHAR(60) NOT NULL
                );
                """
            )
            conn.commit()


def create_vehicle(v):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO vehicles (matricula, vin, modelo, marca, tipo)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (v["matricula"], v["vin"], v["modelo"], v["marca"], v["tipo"]),
            )
            conn.commit()


def get_vehicle(matricula):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT matricula, vin, modelo, marca, tipo FROM vehicles WHERE matricula = %s",
                (matricula,),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def list_vehicles():
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT matricula, vin, modelo, marca, tipo FROM vehicles ORDER BY matricula")
            rows = cur.fetchall()
            return [dict(r) for r in rows]


def delete_vehicle(matricula):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM vehicles WHERE matricula = %s", (matricula,))
            deleted = cur.rowcount
            conn.commit()
            return deleted > 0
