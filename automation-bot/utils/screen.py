import time

from config import UI_READY_DELAY_SECONDS


def wait_for_ui_ready() -> bool:
    """
    Espera una fraccion de segundo para dar tiempo a que cargue la UI.
    En escenarios reales podrias validar pixeles/imagenes antes de continuar.
    """
    time.sleep(UI_READY_DELAY_SECONDS)
    return True
