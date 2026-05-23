import flet
from flet import Page, ElevatedButton

def main (page:Page):
    def on_click_btn (e):
        print ("i was clicked!")
    def on_hover_btn (e):
        print ("why you hovering on me!")
    def on_longpress_btn (e):
        print ("you pressed me so long!")                

    btn = ElevatedButton (
        text="Click Me", 
        on_click = on_click_btn,
        on_hover = on_hover_btn,
        on_long_press = on_longpress_btn 
    )
    page.add (btn)

flet.app (target=main)