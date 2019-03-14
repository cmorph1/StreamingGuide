from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from StreamGuideProgram import Netflix, NowTV, Amazon

class BaseScreen(Screen):

    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        global screen_frame
        screen_frame = BoxLayout(orientation='vertical')
        self.app_logo = Image(source='StreamGuideLogo.jpg', pos_hint=self._get_position_hint(), size_hint=self._get_size_hint())

    def screen_navigation(self, *args):
        pass

    def _get_position_hint(self):
        pass

    def _get_size_hint(self):
        pass

class WelcomeScreen(BaseScreen):

    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        intro_label = Label(text='Welcome to Stream Guide! \n'
                                 'Your personal search engine for the major streaming services.\n'
                                 'Simply enter your username and password for the sites you have a subscription too,\n'
                                 'along with what you want to watch and Stream Guide will do the leg work for you.', halign='center')
        start_button = Button(text='Start', font_size='20sp', pos_hint={'x': .4, 'top': 1}, size_hint=(.2, .15))
        start_button.background_color = [0, 0, 9, 1]
        start_button.bind(on_press=self.screen_navigation)
        space_label = Label(text='')
        screen_frame.add_widget(self.app_logo)
        screen_frame.add_widget(intro_label)
        screen_frame.add_widget(start_button)
        screen_frame.add_widget(space_label)
        self.add_widget(screen_frame)

    def screen_navigation(self, *args):
        self.manager.current = 'user details screen'

    def _get_position_hint(self):
        return{'y': 1, 'x': 0}

    def _get_size_hint(self):
        return(.6, .5)


class UserDetailsScreen(BaseScreen):

    def __init__(self, **kwargs):
        super(UserDetailsScreen, self).__init__(**kwargs)
        input_frame = GridLayout(cols=3, rows=3, padding=10, spacing=10, row_force_default=True, row_default_height=30)
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
        submit_button.background_color = [0, 0, 9, 1]
        submit_button.bind(on_press=self.screen_navigation)
        space_label = Label(text='')
        screen_frame.add_widget(self.app_logo)
        screen_frame.add_widget(enter_details)
        screen_frame.add_widget(input_frame)
        screen_frame.add_widget(submit_button)
        screen_frame.add_widget(space_label)
        self.add_widget(screen_frame)

    def screen_navigation(self, *args):
        self.manager.current = 'search screen'

    def _get_position_hint(self):
        return{'y': 1, 'x': 0.25}

    def _get_size_hint(self):
        return(.5, .45)

class SearchScreen(BaseScreen):

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        search_bar_frame = FloatLayout()
        self.search_input = TextInput(text='Your search', width=400, height=30, size_hint=(None, None), pos_hint={'x': .25, 'y': 0.8})
        self._setup_search_button()
        back_button = Button(text='Back', font_size='20sp', pos_hint={'x': 0.5, 'y': 0.5}, size_hint=(.2, .25))
        back_button.background_color = [0, 0, 9, 1]
        back_button.bind(on_press=self.screen_navigation)
        search_bar_frame.add_widget(self.search_input)
        search_bar_frame.add_widget(self.search_button)
        search_bar_frame.add_widget(back_button)
        self.netf_results = Label(text=('Netflix: '), font_size='20sp')
        amap_results = Label(text='Amazon Prime:', font_size='20sp')
        nowt_results = Label(text='Now TV:', font_size='20sp')
        screen_frame.add_widget(self.app_logo)
        screen_frame.add_widget(search_bar_frame)
        screen_frame.add_widget(self.netf_results)
        screen_frame.add_widget(amap_results)
        screen_frame.add_widget(nowt_results)
        self.add_widget(screen_frame)

    def screen_navigation(self, *args):
        self.manager.current = 'user details screen'

    def _setup_search_button(self):
        self.search_button = Button(text='Search', font_size='20sp', pos_hint={'x': 0.3, 'y': 0.5}, size_hint=(.2, .25))
        self.search_button.background_color = [0, 0, 9, 1]
        self.search_button.bind(on_press=self.search_streamers)
        self.search_button.bind(on_press=self.assign_input_text)

    def search_streamers(self, *args):
        netflix_search = Netflix()
        self.nf_results = netflix_search.search(self._search_string)
        self.netf_results.text = 'Netflix: {}'.format(self.nf_results)

    def assign_input_text(self, *args):
        self._search_string = self.search_input.text

    def _get_position_hint(self):
        return{'y': 1, 'x': 0.2}

    def _get_size_hint(self):
        return(.6, .5)


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
