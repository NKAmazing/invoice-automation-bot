import logging
import time

import pandas as pd

from config import CSV_PATH, PREPARE_DELAY_SECONDS, ROW_DELAY_SECONDS
from utils.actions import submit_invoice_form
from utils.screen import wait_for_ui_ready


def configure_logging() -> None:
    # Configura el logging para que se imprima en la consola
    # level=logging.INFO: Imprime solo mensajes de nivel INFO y superiores
    # format="%(asctime)s | %(levelname)s | %(message)s": Formato de los mensajes
    # datefmt="%H:%M:%S": Formato de la fecha y hora
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def main() -> None:
    # Configura el logging para que se imprima en la consola (llamada a la funcion)
    configure_logging()

    # Imprime un mensaje de INFO con el nombre del CSV que se esta leyendo
    logging.info("Leyendo CSV desde %s", CSV_PATH)

    # Lee el CSV y lo guarda en la variable data
    data = pd.read_csv(CSV_PATH)

    # Define las columnas requeridas para el CSV
    required_columns = {"name", "amount", "description"}

    # Verifica si las columnas requeridas estan en el CSV
    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(
            # Imprime un mensaje de ERROR con las columnas faltantes
            f"Faltan columnas requeridas en el CSV: {', '.join(sorted(missing_columns))}"
        )

    print(
        f"Tenes {PREPARE_DELAY_SECONDS} segundos para posicionarte en el formulario..."
    )
    time.sleep(PREPARE_DELAY_SECONDS)

    # Inicializa el contador de filas exitosas
    success_count = 0

    # Itera sobre cada fila del CSV
    for index, row in data.iterrows():
        row_number = index + 1
        logging.info("Procesando fila %s de %s", row_number, len(data))

        if not wait_for_ui_ready():
            logging.error("UI no lista. Se omite fila %s", row_number)
            continue

        try:
            submit_invoice_form(
                name=row["name"],
                amount=row["amount"],
                description=row["description"],
            )
            success_count += 1
            logging.info("Fila %s cargada correctamente", row_number)
        except Exception as exc:  # pragma: no cover
            logging.exception("Error cargando fila %s: %s", row_number, exc)

        time.sleep(ROW_DELAY_SECONDS)

    logging.info(
        "Proceso finalizado. Exitos: %s | Errores: %s",
        success_count,
        len(data) - success_count,
    )


if __name__ == "__main__":
    main()
