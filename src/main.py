from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import flet as ft
import random

wand_sound = {"C":[0,4], "C#":[5,8], "D":[9,12], "D#":[13,15], "E":[16,20], "F":[21,24], "F#":[25, 28], "G":[29,32], "G#":[33,36], "A":[37, 40], "A#":[41,44], "B":[45,48]}
song = []
client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

def next(unused_addr, args, wave_flag):
    global song
    if wave_flag == True and song[-1:] != []:
        client.send_message("/avatar/parameters/E&L/Radial_H", 0.01 * random.randint(*wand_sound[song.pop()]))

def main(page: ft.Page):
    song_view = ft.Text(" ".join(song))
    def insert_bell(e):
        global song
        print(song)
        song.append(str(e.control.text))
        song_view.value = " ".join(song)
        song_view.update()
        page.update()

    C = ft.FilledButton(on_click=insert_bell, text="C")
    C_sharp = ft.FilledButton(on_click=insert_bell, text="C#")
    D = ft.FilledButton(on_click=insert_bell, text="D")
    D_sharp = ft.FilledButton(on_click=insert_bell, text="D#")
    E = ft.FilledButton(on_click=insert_bell, text="E")
    F = ft.FilledButton(on_click=insert_bell, text="F")
    F_sharp = ft.FilledButton(on_click=insert_bell, text="F#")
    G = ft.FilledButton(on_click=insert_bell, text="G")
    G_sharp = ft.FilledButton(on_click=insert_bell, text="G#")
    A = ft.FilledButton(on_click=insert_bell, text="A")
    A_sharp = ft.FilledButton(on_click=insert_bell, text="A#")
    B = ft.FilledButton(on_click=insert_bell, text="B")

    page.add(
        ft.Text("えるしおんちゃんプレイヤー"),
        ft.SafeArea(
            song_view,
            expand=True,
        ),
                C,
                C_sharp,
                D,
                D_sharp,
                E,
                F,
                F_sharp,
                G,
                G_sharp,
                A,
                A_sharp,
                B
    )
    dispatcher = Dispatcher()
    dispatcher.map("/avatar/parameters/E&L/Ring", next, "wave")
    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 9001), dispatcher)
    server.serve_forever()

ft.app(main)
