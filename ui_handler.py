from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner
import time
class UIHandler:
    def __init__(self):
        self.console = Console()
    def show_header(self,title, subtitle):
        self.console.print(Panel.fit(
            f"[bold cyan]{title}[/bold cyan]\n[dim]{subtitle}[/dim]",
            border_style="blue"
        ))
    def custom_print(self,message,style):
        self.console.print(f"[{style}]> {message}[/{style}]")
    # def custom_print(self,message, style="green"):
    #     self.console.print(f"[{style}]> {message}[/{style}]")

    def show_loading(self,message,color,duration=2):
        spinner = Spinner("dots12", text=message, style=color)
        with Live(spinner, refresh_per_second=10):
            time.sleep(duration)

