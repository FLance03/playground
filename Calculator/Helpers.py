from PyQt5.QtWidgets import QLayout

def get_recursive_children(widget:QLayout):
    if widget is not None:
        for i in range(widget.count()):
            item = widget.itemAt(i)
            if item.widget() is not None:
                print(item.widget())
            elif item.layout() is not None:
                get_recursive_children(item)