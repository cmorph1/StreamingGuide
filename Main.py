from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager


class WelcomeScreen(Screen):

    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        welcome_screen_frame = BoxLayout(orientation='vertical')
        app_logo = Image(source='StreamGuideLogo.jpg', pos_hint={'y': 1, 'bottom': 0}, size_hint=(.6, .5))
        intro_label = Label(text='Welcome to Stream Guide! \n'
                                 'Your personal search engine for the major streaming services.\n'
                                 'Simply enter your username and password for the sites you have a subscription too,\n'
                                 'along with what you want to watch and Stream Guide will do the leg work for you.', halign='center')
        start_button = Button(text='Start', font_size='20sp', pos_hint={'x': .4, 'top': 1}, size_hint=(.2, .15))
        start_button.background_color = [0, 0, 128, 0.2]
        start_button.bind(on_press=self.go_to_user_details)
        space_label = Label(text='')
        welcome_screen_frame.add_widget(app_logo)
        welcome_screen_frame.add_widget(intro_label)
        welcome_screen_frame.add_widget(start_button)
        welcome_screen_frame.add_widget(space_label)
        self.add_widget(welcome_screen_frame)

    def go_to_user_details(self,*args):
        self.manager.current = 'user details screen'


class UserDetailsScreen(Screen):

    def __init__(self, **kwargs):
        super(UserDetailsScreen, self).__init__(**kwargs)
        search_screen_frame = BoxLayout(orientation='vertical')
        input_frame = GridLayout(cols=3, rows=3, padding=10, spacing=10, row_force_default=True, row_default_height=30)
        app_logo = Image(source='StreamGuideLogo.jpg', pos_hint={'y': 1, 'bottom': 0}, size_hint=(.6, .5))
        enter_details = Label(text='Please enter your username and password for the sites you are registered with')
        streamer_name_nf = Label(text="Netflix:", font_size='20sp', halign='left', size_hint_x=None, width=150)
        username_input_nf = TextInput(text='Username')
        password_input_nf = TextInput(text='Password', width=100, password=True)
        streamer_name_ap = Label(text="Amazon Prime:", font_size='20sp', halign='left', size_hint_x=None, width=150)
        username_input_ap = TextInput(text='Username')
        password_input_ap = TextInput(text='Password', width=100, password=True)
        streamer_name_nt = Label(text="Now TV:", font_size='20sp', halign='left', size_hint_x=None, width=150)
        username_input_nt = TextInput(text='Username')
        password_input_nt = TextInput(text='Password', width=100, password=True)
        input_frame.add_widget(streamer_name_nf)
        input_frame.add_widget(username_input_nf)
        input_frame.add_widget(password_input_nf)
        input_frame.add_widget(streamer_name_ap)
        input_frame.add_widget(username_input_ap)
        input_frame.add_widget(password_input_ap)
        input_frame.add_widget(streamer_name_nt)
        input_frame.add_widget(username_input_nt)
        input_frame.add_widget(password_input_nt)
        submit_button = Button(text='Submit', font_size='20sp', pos_hint={'x': .4, 'top': 1}, size_hint=(.2, .2))
        submit_button.background_color = [0, 0, 128, 0.2]
        submit_button.bind(on_press=self.go_to_search)
        space_label = Label(text='')
        search_screen_frame.add_widget(app_logo)
        search_screen_frame.add_widget(enter_details)
        search_screen_frame.add_widget(input_frame)
        search_screen_frame.add_widget(submit_button)
        search_screen_frame.add_widget(space_label)
        self.add_widget(search_screen_frame)

    def go_to_search(self,*args):
        self.manager.current = 'search screen'


class SearchScreen(Screen):

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        search_screen_frame = BoxLayout(orientation='vertical')
        search_bar_frame = BoxLayout(orientation='vertical')
        button_frame = BoxLayout(orientation='horizontal')
        app_logo = Image(source='StreamGuideLogo.jpg', pos_hint={'y': 1, 'bottom': 0}, size_hint=(.6, .5))
        search_input = TextInput(text='Your search', width=400, height=30, size_hint=(None, None), pos_hint={'x': .25, 'y': 0.1})
        search_button = Button(text='Search', font_size='20sp', pos_hint={'x': 1, 'top': .9}, size_hint=(None, .2))
        search_button.background_color = [0, 0, 128, 0.2]
        back_button = Button(text='Back', font_size='20sp', pos_hint={'x': 1, 'top': .9}, size_hint=(None, .2))
        back_button.background_color = [0, 0, 128, 0.2]
        back_button.bind(on_press=self.go_to_user_details)
        button_frame.add_widget(search_button)
        button_frame.add_widget(back_button)
        search_bar_frame.add_widget(search_input)
        search_bar_frame.add_widget(button_frame)
        nf_results = Label(text='Netflix:', font_size='20sp')
        ap_results = Label(text='Amazon Prime:', font_size='20sp')
        nt_results = Label(text='Now TV:', font_size='20sp')
        search_screen_frame.add_widget(app_logo)
        search_screen_frame.add_widget(search_bar_frame)
        search_screen_frame.add_widget(nf_results)
        search_screen_frame.add_widget(ap_results)
        search_screen_frame.add_widget(nt_results)
        self.add_widget(search_screen_frame)

    def go_to_user_details(self,*args):
        self.manager.current = 'user details screen'


class MyApp(App):

    def build(self):
        app_manager = ScreenManager()
        welcome_screen = WelcomeScreen(name='welcome screen')
        user_details_screen = UserDetailsScreen(name='user details screen')
        search_screen = SearchScreen(name='search screen')
        app_manager.add_widget(welcome_screen)
        app_manager.add_widget(user_details_screen)
        app_manager.add_widget(search_screen)
        return app_manager


if __name__ == '__main__':
    MyApp().run()
