from win10toast import ToastNotifier

def change_mod_notifier(mode):
    toaster = ToastNotifier()
    toaster.show_toast("Mode", f"Mode changed to {mode}", duration = 0)
