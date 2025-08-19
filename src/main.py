from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import flet as ft
import random
import argparse
import asyncio
import copy

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="The ip of th OSC Server")
parser.add_argument("--port", type=int, default=9000, help="The port the OSC server is listening on")
parser.add_argument("--send_port", type=int, default=9001, help="The port the OSC server is sending on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)

wand_sound = {"C":[0,4], "C#":[5,8], "D":[9,12], "D#":[13,15], "E":[16,20], "F":[21,24], "F#":[25, 28], "G":[29,32], "G#":[33,36], "A":[37, 40], "A#":[41,44], "B":[45,48], "C_hi":[49,52], "C#_hi":[53,56], "D_hi":[57,60], "D#_hi":[61,64], "E_hi":[65,68], "F_hi":[69,72], "F#_hi":[73,76], "G_hi":[77,80], "G#_hi":[81,84], "A_hi":[85,88], "A#_hi":[89,92], "B_hi":[93,96], "C_hihi":[97,100]}
song = []

def next(unused_addr, args, wave_flag):
    global song
    if len(song) == 0:
        return
    if wave_flag == True and song[-1:][0] in wand_sound:
        client.send_message("/avatar/parameters/E&L/Radial_H", 0.01 * random.randint(*wand_sound[song.pop(0)]))

def main(page: ft.Page):
    page.title = "えるしおんプレイヤー"
    def insert_bell(e):
        global song
        print(song)
        song.append(str(e.control.text))
        song_view.value = " ".join(song)
        song_view.update()
        page.update()

    def song_change(e):
        global song
        print(song)
        song = song_view.value.split(' ')

    song_view = ft.TextField(label='歌詞', border=ft.InputBorder.NONE, filled=True, hint_text='C C G G A A G F F E E D D C ...', min_lines=30, multiline=True, on_change=song_change)

    C = ft.FilledButton(on_click=insert_bell, text="C", color=ft.Colors.CYAN_ACCENT_100)
    C_sharp = ft.FilledButton(on_click=insert_bell, text="C#", color=ft.Colors.CYAN_ACCENT_100)
    D = ft.FilledButton(on_click=insert_bell, text="D", color=ft.Colors.CYAN_ACCENT_100)
    D_sharp = ft.FilledButton(on_click=insert_bell, text="D#", color=ft.Colors.CYAN_ACCENT_100)
    E = ft.FilledButton(on_click=insert_bell, text="E", color=ft.Colors.CYAN_ACCENT_100)
    F = ft.FilledButton(on_click=insert_bell, text="F", color=ft.Colors.CYAN_ACCENT_100)
    F_sharp = ft.FilledButton(on_click=insert_bell, text="F#", color=ft.Colors.CYAN_ACCENT_100)
    G = ft.FilledButton(on_click=insert_bell, text="G", color=ft.Colors.CYAN_ACCENT_100)
    G_sharp = ft.FilledButton(on_click=insert_bell, text="G#", color=ft.Colors.CYAN_ACCENT_100)
    A = ft.FilledButton(on_click=insert_bell, text="A", color=ft.Colors.CYAN_ACCENT_100)
    A_sharp = ft.FilledButton(on_click=insert_bell, text="A#", color=ft.Colors.CYAN_ACCENT_100)
    B = ft.FilledButton(on_click=insert_bell, text="B", color=ft.Colors.CYAN_ACCENT_100)
    C_hi = ft.FilledButton(on_click=insert_bell, text="C_hi", color=ft.Colors.CYAN_ACCENT_100)
    C_sharp_hi = ft.FilledButton(on_click=insert_bell, text="C#_hi", color=ft.Colors.CYAN_ACCENT_100)
    D_hi = ft.FilledButton(on_click=insert_bell, text="D_hi", color=ft.Colors.CYAN_ACCENT_100)
    D_sharp_hi = ft.FilledButton(on_click=insert_bell, text="D#_hi", color=ft.Colors.CYAN_ACCENT_100)
    E_hi = ft.FilledButton(on_click=insert_bell, text="E_hi", color=ft.Colors.CYAN_ACCENT_100)
    F_hi = ft.FilledButton(on_click=insert_bell, text="F_hi", color=ft.Colors.CYAN_ACCENT_100)
    F_sharp_hi = ft.FilledButton(on_click=insert_bell, text="F#_hi", color=ft.Colors.CYAN_ACCENT_100)
    G_hi = ft.FilledButton(on_click=insert_bell, text="G_hi", color=ft.Colors.CYAN_ACCENT_100)
    G_sharp_hi = ft.FilledButton(on_click=insert_bell, text="G#_hi", color=ft.Colors.CYAN_ACCENT_100)
    A_hi = ft.FilledButton(on_click=insert_bell, text="A_hi", color=ft.Colors.CYAN_ACCENT_100)
    A_sharp_hi = ft.FilledButton(on_click=insert_bell, text="A#_hi", color=ft.Colors.CYAN_ACCENT_100)
    B_hi = ft.FilledButton(on_click=insert_bell, text="B_hi", color=ft.Colors.CYAN_ACCENT_100)
    C_hihi = ft.FilledButton(on_click=insert_bell, text="C_hihi", color=ft.Colors.CYAN_ACCENT_100)

    def read_song(e: ft.FilePickerResultEvent):
        global song
        with open(e.files[0].path, "r") as f:
            song = f.read().split(' ')
            song_view.value = " ".join(song)
            page.update()

    save_file_pick = ft.FilePicker(on_result=lambda e: (f:=open(e.path, "w")) and f.write(" ".join(song)) and f.close())
    read_file_pick = ft.FilePicker(on_result=read_song)

    async def play(e):
        global song
        temp = copy.deepcopy(song)
        for sound in temp:
            await asyncio.sleep(0.5)
            client.send_message("/avatar/parameters/E&L/Ring", 1)
            await asyncio.sleep(0.015)
            client.send_message("/avatar/parameters/E&L/Ring", 0)
            print(sound)
        song = temp

    page.overlay.append(save_file_pick)
    page.overlay.append(read_file_pick)
    page.add(
        ft.Text("えるしおんちゃんプレイヤー"),
        ft.Row(
        controls=[
        ft.ElevatedButton(
            "Save",
            icon=ft.Icons.SAVE,
            on_click=lambda _: save_file_pick.save_file(file_name="sample.txt")),
        ft.ElevatedButton(
            "Load",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=lambda _: read_file_pick.pick_files()),
        ft.ElevatedButton(
            "AutoPlay",
            icon=ft.Icons.SURROUND_SOUND,
            on_click=play),
        ]),
        ft.Row(
        	controls=[ft.Image(src=f"header.png", width=600, fit=ft.ImageFit.CONTAIN)],
        	alignment=ft.MainAxisAlignment.CENTER,

        ),
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
                ],
            alignment=ft.MainAxisAlignment.CENTER,
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
                ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    dispatcher = Dispatcher()
    dispatcher.map("/avatar/parameters/E&L/Ring", next, "wave")
    server = osc_server.BlockingOSCUDPServer((args.ip, args.send_port), dispatcher)
    server.serve_forever()

ft.app(main)
