from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import flet as ft
import random

wand_sound = {"C":[0,4], "C#":[5,8], "D":[9,12], "D#":[13,15], "E":[16,20], "F":[21,24], "F#":[25, 28], "G":[29,32], "G#":[33,36], "A":[37, 40], "A#":[41,44], "B":[45,48], "C_hi":[49,52], "C#_hi":[53,56], "D_hi":[57,60], "D#_hi":[61,64], "E_hi":[65,68], "F_hi":[69,72], "F#_hi":[73,76], "G_hi":[77,80], "G#_hi":[81,84], "A_hi":[85,88], "A#_hi":[89,92], "B_hi":[93,96], "C_hihi":[97,100]}
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
    C_hi = ft.FilledButton(on_click=insert_bell, text="C_hi")
    C_sharp_hi = ft.FilledButton(on_click=insert_bell, text="C#_hi")
    D_hi = ft.FilledButton(on_click=insert_bell, text="D_hi")
    D_sharp_hi = ft.FilledButton(on_click=insert_bell, text="D#_hi")
    E_hi = ft.FilledButton(on_click=insert_bell, text="E_hi")
    F_hi = ft.FilledButton(on_click=insert_bell, text="F_hi")
    F_sharp_hi = ft.FilledButton(on_click=insert_bell, text="F#_hi")
    G_hi = ft.FilledButton(on_click=insert_bell, text="G_hi")
    G_sharp_hi = ft.FilledButton(on_click=insert_bell, text="G#_hi")
    A_hi = ft.FilledButton(on_click=insert_bell, text="A_hi")
    A_sharp_hi = ft.FilledButton(on_click=insert_bell, text="A#_hi")
    B_hi = ft.FilledButton(on_click=insert_bell, text="B_hi")
    C_hihi = ft.FilledButton(on_click=insert_bell, text="C_hihi")

    page.add(
        ft.Text("えるしおんちゃんプレイヤー"),
        ft.SafeArea(
            song_view,
            expand=True,
        ),
        ft.Row(
        controls=[
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
                ]
        ),
        ft.Row(
        controls=[
                C_hi,
                C_sharp_hi,
                D_hi,
                D_sharp_hi,
                E_hi,
                F_hi,
                F_sharp_hi,
                G_hi,
                G_sharp_hi,
                A_hi,
                A_sharp_hi,
                B_hi,
                C_hihi
                ]
        )
    )
    dispatcher = Dispatcher()
    dispatcher.map("/avatar/parameters/E&L/Ring", next, "wave")
    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 9001), dispatcher)
    server.serve_forever()

ft.app(main)
