import pyautogui


def submit_invoice_form(name: str, amount: float, description: str) -> None:
    """
    Completa campos secuencialmente usando TAB para navegar
    y ENTER para enviar.
    """
    pyautogui.write(str(name))
    pyautogui.press("tab")
    pyautogui.write(str(amount))
    pyautogui.press("tab")
    pyautogui.write(str(description))
    pyautogui.press("enter")
