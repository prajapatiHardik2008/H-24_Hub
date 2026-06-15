from rich.console import Console,Group
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

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

    def show_loading(self,message,color,spinner_type,duration=2):
        spinner = Spinner(spinner_type, text=message, style=color)
        with Live(spinner, refresh_per_second=10):
            time.sleep(duration)


console = Console()

def alert_warning(title: str, points: list):
    # Points ko bullet format mein change karna
    formatted_points = [Text(f"• {p}", style="white") for p in points]
    
    # Group ka use karke saare points ko ek saath wrap karna
    content = Group(*formatted_points)
    
    # Panel mein group ko pass karna
    panel = Panel(
        content, 
        border_style="red", 
        title=f"[bold white on red] {title} [/bold white on red]",
        expand=False,
        padding=(1, 2)
    )
    
    console.print(panel)

# # Example Usage:
# my_points = [
#     "Unauthorized access attempt.",
#     "Source: 192.168.1.45",
#     "Action: Connection dropped."
# ]

