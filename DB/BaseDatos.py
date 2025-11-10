from astroquery.sdss import SDSS
from datetime import datetime
from dl import queryClient as qc
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive
from astroquery.jplhorizons import Horizons
from astroquery.mpc import MPC
import csv, os
import pandas as pd


class BaseDatos:
    def __init__(self, limite=10000):
        self.limite = limite

    def conectar(self, ra=None, dec=None, z_max=None, z_min=None, tipo=None , source = None):
        

        # Valores por defecto si no se dan
        ra = 180.0 if ra is None else float(ra)
        dec = 0.0 if dec is None else float(dec)
        z_max = 0.3 if z_max is None else float(z_max)
        z_min = 0.05 if z_min is None else float(z_min)

        if source.upper() == "SDSS":
            radius = float(input("Ingresa el radio de búsqueda (en grados): "))
            query = f"""
            SELECT TOP {self.limite}
                p.objid, p.ra, p.dec, s.z, s.class
            FROM PhotoObj AS p
            JOIN SpecObj AS s ON s.bestobjid = p.objid
            WHERE s.z BETWEEN {z_min} AND {z_max}
            AND p.ra BETWEEN {ra - radius} AND {ra + radius}
            AND p.dec BETWEEN {dec - radius} AND {dec + radius}
            """

            print("\nEjecutando consulta a SDSS...")
            result = SDSS.query_sql(query)
            print("Consulta completada.")

            return result
        elif source.upper() == "DESI":
            radius = float(input("Ingresa el radio de búsqueda (en grados): "))
            query = f"""
                SELECT TOP {self.limite}
                ra, dec ,type, flux_g, flux_r, flux_z, flux_w1, flux_w2 , flux_ivar_g, flux_ivar_r, flux_ivar_z
                FROM ls_dr9.tractor
                WHERE ra BETWEEN {ra - radius} AND {ra + radius}
                AND dec BETWEEN {dec - radius} AND {dec + radius}
                """
            result = qc.query(sql=query, fmt='pandas')

            print(result)
            return result
        elif source.upper() == "NASA ESI":
            result = NasaExoplanetArchive.query_criteria(
            table="pscomppars",
            select="pl_name,hostname,disc_year,pl_orbper,pl_rade,pl_bmasse, pl_tranmid ,st_teff",
            where="disc_year > 2015 AND pl_rade IS NOT NULL",
            order="disc_year DESC"
            )
            return result
        elif source.upper() == "NEO":
            # Lista manual de cuerpos menores (id: nombre)
            # Puedes ampliar la lista con los objetos que prefieras.
            cuerpos = {
                "1": "Ceres",
                "2": "Pallas",
                "4": "Vesta",
                "433": "Eros",
                "1862": "Apollo",
                "4179": "Toutatis",
                "3200": "Phaethon",
                "1620": "Geographos",
                "25143": "Itokawa",
                "101955": "Bennu",
                "99942": "Apophis",
                "162173": "Ryugu",
                "253": "Mathilde",
                "65803": "Didymos",
                "99907": "2013 VY4"  # ejemplo genérico
            }

            # Mostrar una vista corta (primeras N entradas) para no saturar la terminal
            N = 8
            print("== Lista breve de cuerpos menores (muestra) ==")
            short = list(cuerpos.items())[:N]
            df_short = pd.DataFrame(short, columns=["id", "name"])
            print(df_short.to_string(index=False))
            print("== Para ver la lista completa escribe 'done' o 'list' ==")
            print("== Para salir escribe 'exit' ==")

            while True:
                o = input("\nIngresa el id o nombre del objeto a consultar (ej: 101955 o Bennu): ").strip()
                if o.lower() in ("exit", "salir", "q"):
                    print("Saliendo.")
                    return None

                if o.lower() in ("done", "list"):
                    # Mostrar toda la lista
                    df_all = pd.DataFrame(list(cuerpos.items()), columns=["id", "name"])
                    print("\n== Lista completa de cuerpos menores disponibles ==")
                    print(df_all.to_string(index=False))
                    continue

                # Normalizar entrada: si el usuario ingresó un número que está en la lista usarlo
                key = None
                if o.isdigit() and o in cuerpos:
                    key = o
                    target = cuerpos[key]
                else:
                    # buscar por nombre (coincidencia parcial, case-insensitive)
                    matches = [(k, n) for k, n in cuerpos.items() if o.lower() in n.lower()]
                    if len(matches) == 1:
                        key, target = matches[0]
                    elif len(matches) > 1:
                        print("Se encontraron varias coincidencias:")
                        for k, n in matches:
                            print(f"  {k} : {n}")
                        print("Escribe el id exacto o nombre más específico.")
                        continue
                    else:
                        # No hay coincidencias en la lista manual: intentar usar directamente la entrada como id/nombre
                        key = None
                        target = o  # probar con Horizons directamente

                # Intentar consulta en JPL Horizons
                try:
                    print(f"\nConsultando '{target}' en JPL Horizons...")
                    obj = Horizons(id=target, id_type='smallbody', location='@sun',
                                epochs={'start':'2025-01-01', 'stop':'2025-01-10', 'step':'1d'})
                    result = obj.elements()
                    eph = obj.ephemerides()

                    print("\n=== Elementos orbitales ===")
                    # Algunas columnas pueden no existir para ciertos objetos; comprobamos antes de mostrar
                    cols_elem = [c for c in ['targetname', 'a', 'e', 'incl', 'Omega', 'w', 'M'] if c in result.colnames]
                    print(result[cols_elem])

                    print("\n=== Efemérides (primeras filas) ===")
                    cols_eph = [c for c in ['datetime_str', 'RA', 'DEC', 'delta', 'r', 'V'] if c in eph.colnames]
                    print(eph[cols_eph][:10])  # mostramos hasta 10 filas

                    # Si quieres retornar ambos objetos para uso posterior:
                    return result

                except Exception as exc:
                    print(f"❌ Error al consultar '{o}': {exc}")
                    print("Prueba con otro id/nombre o escribe 'list' para ver la lista disponible.")
                    continue


        else:
            print("Fuente no soportada por el momento.")
            return None
        
   
    def guardardatos(self, result,source):
        os.makedirs("data", exist_ok=True)

        if result is not None:
            print(result[:5])  # muestra las primeras 5 filas
            print("Guardando consulta")
            fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nombre_archivo = os.path.join("data", f"{source}_{fecha}.csv")
            with open(nombre_archivo, "w", newline="") as archivo:
                writer = csv.writer(archivo)
                writer.writerow(result.columns)  # Encabezados
                writer.writerows(result)          # Filas de datos

            print(f"Archivo '{source}_{fecha}.csv' creado con éxito.")


        else:
            print("No se obtuvieron resultados.")
        



# --- PRUEBA ---
if __name__ == "__main__":
    bd = BaseDatos(limite=1000)
    a = input("Seleccione la fuente de sus datos (SDSS, DESI, NASA ESI, NEO ): ")
    ra =float(input("Ingresa Ra deg"))
    dec =float(input("Ingresa Dec deg"))
    z_min =float(input("Ingresa z-min"))
    z_max =float(input("Ingresa z-max"))
    resultado = bd.conectar(ra=ra, dec=dec, z_min=z_min, z_max=z_max, source = a)
    archivos = bd.guardardatos(resultado,source = a)