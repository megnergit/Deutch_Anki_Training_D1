import flet as ft
from pathlib import Path
import pandas as pd

PRIMARY_COLOR=ft.colors.TEAL_ACCENT_700
SECOND_COLOR=ft.colors.AMBER
THIRD_COLOR=ft.colors.PINK_500
VOCABULARY_FILE = './assets/verben.csv'

#======================================================================
class AnkiCard(ft.Column):
    def __init__(self, Q:object, A:object, answer_mode: bool):
        super().__init__()
        self.Q=Q
        if answer_mode: 
            self.A=A
        else: 
            self.A=" "

        self.answer_mode = answer_mode

        question_line = ft.Text(
            value = self.Q,
            style = ft.TextStyle(
                size = 80,
            )

        )
        answer_line = ft.Text(
            value = self.A,
            style = ft.TextStyle(
                size = 32,
            ),
            color = THIRD_COLOR
        )
        self.card_view = ft.Container(
            content =  ft.Column(
            controls = [question_line, answer_line],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
            ), 
            margin = ft.margin.only(top=800, bottom=128),
            alignment=ft.alignment.center
        )

        self.controls = [self.card_view]

#======================================================================
class AnkiApp(ft.Column):
#----------------------------------------------------------------------

    def __init__(self, card_data):
        super().__init__()
        self.ni = 0
        self.answer_mode = False # False: question True: answer
#-----------------
        self.card_data = card_data
        self.new_card = self.card_data.iloc[self.ni].to_dict()

        self.Q, self.A, = self.new_card['Q'], self.new_card['A']
        self.R, self.F, = self.new_card['R'], self.new_card['F']

# initial card view
        self.card_view = ft.Column()
        self.card_view.controls = [AnkiCard(Q=self.Q,A=self.A, 
                                            answer_mode=self.answer_mode)]

#---------------------------------------------------
# buttom view
# I know button
        self.positive_button = ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="しっとる", 
                                size=64, 
                                weight=ft.FontWeight.W_900,
                                font_family = "mplus1",
                                ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=ft.padding.all(16),
            ),

            color=PRIMARY_COLOR,
            bgcolor=SECOND_COLOR,
            on_click = self.show_answer,
        )

        self.negative_button = ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="しらん", 
                                size=64, 
                                weight=ft.FontWeight.W_900,
                                font_family = "mplus1",
                                ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=ft.padding.all(16),
            ),
            bgcolor=PRIMARY_COLOR,
            color=SECOND_COLOR,
            on_click = self.show_answer,
        )

#---------------------------------------------------
# next button
        self.next_button = ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="つぎ", 
                                size=64, 
                                weight=ft.FontWeight.W_900,
                                font_family = "mplus1",
                                ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=ft.padding.all(16),
            ),

            color=PRIMARY_COLOR,
            bgcolor=SECOND_COLOR,
            on_click = self.next_card,
        )

#-----------------
# put them all together

        self.buttons_view = ft.Column()

        self.buttons_view.controls = [ft.Row([
                    ft.Container(self.positive_button,
                                expand = 1,
                    ),
                    ft.Container(self.negative_button,
                                expand = 1, 
                    ),
                ]) 
        ]

#-----------------
# put them all together

        self.controls = [
            ft.Column([
                self.card_view,
                self.buttons_view,
            ], 
            width=1024)
        ]

#----------------------------------------------------------------------
    def next_card(self, e):

        self.ni += 1
        self.answer_mode = False
        self.new_card = self.card_data.iloc[self.ni].to_dict()


        self.Q, self.A, = self.new_card['Q'], self.new_card['A']
        self.R, self.F, = self.new_card['R'], self.new_card['F']


# card view
        self.card_view.controls = [AnkiCard(Q=self.Q,A=self.A, 
                                            answer_mode=self.answer_mode)]


        self.buttons_view.controls = [ft.Row([
                    ft.Container(self.positive_button,
                                expand = 1,
                    ),
                    ft.Container(self.negative_button,
                                expand = 1, 
                    ),
                ]) 
        ]

        self.update()

#----------------------------------------------------------------------
    def show_answer(self, e):

        self.answer_mode = True

        self.card_view.controls = [AnkiCard(Q=self.Q,A=self.A, 
                                            answer_mode = self.answer_mode)]

        self.buttons_view.controls = [ft.Row([
                    ft.Container(self.next_button,
                                expand = 1,
                    ),
                ]) 
        ]

        self.update()

#======================================================================
    # handy functions

def load_card_data(file_path):

    file_path.exists()
    df = pd.read_csv(file_path,
        dtype={'Q': object, 'A': object, 'R': 'Int64', 'F': 'Int64'},
                                comment="#", 
                                header=0,
                                on_bad_lines='warn',
        )

    return df.sample(n=len(df))

#======================================================================
def main(page: ft.Page):

    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "fonts/OpenSans-VariableFont_wdth,wght.ttf",
        "mplus1": "fonts/MPLUS1Code-VariableFont_wght.ttf",
    }

    page.theme_mode = "light"    
    page.theme = ft.Theme(
         color_scheme=ft.ColorScheme(primary=PRIMARY_COLOR,
                                     secondary=SECOND_COLOR),
         font_family="Kanit",

    )
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    card_data = load_card_data(Path(VOCABULARY_FILE))
    page.update()
    app = AnkiApp(card_data)

    page.add(app)

ft.app(target=main)
#======================================================================
# scratch
#======================================================================
