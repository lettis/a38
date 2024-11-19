
from store import Store, Ontology, UI

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Header, Footer, Input, Label, Widget
from textual.validation import Regex



store = Store()
onto = Ontology()
ui = UI()


class GenericScreen(Screen):

    BINDINGS = [
        ("escape", "app.pop_screen", "go back")
    ]

    def __init__(self, ref):
        super().__init__()
        self.ref = ref
        self.label = ui.label(self.ref)




    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(self.label)
        yield Footer()




class GenericForm(Widget):

    def __init__(self, ref_entity):
        super().__init__()
        self.ref_entity = ref_entity

    def compose(self) -> ComposeResult:
        pass




class Tui(App):

    BINDINGS = [
        ("escape", "close()", "close"),
    ]

    def action_close(self):
        self.exit()

    def on_mount(self) -> None:
        self.title = "A38"

        for screen in ui.screens():
            label = ui.label(screen)
            self.install_screen(GenericScreen(ref), name=label)
            self.bind(ui.binding(screen), "push_screen('" + label + "')", description=label)


    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("main screen")
        yield Footer()




if __name__ == "__main__":
    app = Tui()
    app.run()

