"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma

Minimalistic GUI for the Python bitcoin library mix.

Supports Python3 only.
"""

from tkinter import Tk, OptionMenu, StringVar, Button, ttk, VERTICAL, \
    Text, END, DISABLED, NORMAL, N, messagebox, Entry, E, W, CHAR
from websocket import WebSocketBadStatusException, \
    WebSocketConnectionClosedException

from sparkl_cli.main import sparkl

# The alias used for the connection with SPARKL.
ALIAS = 'btc_alias'

# The Python module that provides the implementation of the SPARKL mix.
IMPL_MODULE = 'bitcoin'

START_INDEX = 1.0

# List of fiat and crypto currencies the drop-down menus use.
FIAT_LIST = ['CHF', 'EUR', 'GBP', 'HKD', 'RUB', 'USD']
CRYPTO_LIST = ['BCH', 'DASH', 'ETC', 'ETH', 'LTC', 'XRP']

# On exit protocols for the main GUI window.
EXIT = 'Quit'
EXIT_PROMPT = 'Do you want to quit?'
EXIT_PROTOCOL = 'WM_DELETE_WINDOW'


def open_socket(service_path):
    """
    Tries to open a websocket using the specified
    path. The path must be the full path to the service
    in the SPARKL user tree prepended by the user name.

    E.g.: admin@sparkl.com/Scratch/lib_bitcoin_python/Bitcoin.
    """
    try:
        service = sparkl('service',
                         service_path,
                         IMPL_MODULE,
                         alias=ALIAS)
        return True, service

    except WebSocketBadStatusException as error:
        return False, ', '.join(error.args)

    except WebSocketConnectionClosedException as error:
        return False, ', '.join(error.args)


def write_response(service, solicit_dict, msg_box, max_digits=3):
    """
    Uses the provided service instance's 'solicit' method
    to send the provided solicit to SPARKL and writes the
    response to the supplied tkinter message panel.
    """
    start_fields = solicit_dict['data']

    def callback(response):
        """
        Writes a message to the message panel based on the SPARKL response.
        """
        resp_fields = response['data']
        if 'error' in resp_fields:
            message = resp_fields['error']

        elif 'crypto_price' in resp_fields:
            message = 'The price of {} is {} {}.'.format(
                start_fields['crypto_currency'],
                start_fields['currency'],
                round(resp_fields['crypto_price'], max_digits))

        else:
            message = 'The price of {} is {} {}.'.format(
                'bitcoin',
                start_fields['currency'],
                round(resp_fields['btc_price'], max_digits))

        msg_box.write_message(message)

    service.solicit(solicit_dict, callback=callback)


def split_text(width, text, text_list=None):
    """
    Splits the message of the GUI message panel
    if the message is too long.
    """
    if not text_list:
        text_list = []

    txt_length = len(text)

    if txt_length <= width and text_list:
        result = '\n'.join(text_list) + '\n' + text
        return result

    elif txt_length <= width:
        return text

    text_list.append(text[0:width])
    rem_text = text[width:]
    return split_text(width, rem_text, text_list=text_list)


def validate_string(string, min_len=5):
    """
    Validates a string. Returns False if the string
    is less than 'min_len' long.
    """
    string = string.strip()

    if len(string) < min_len:
        return False

    return True


def set_frame_state(state, *frames):
    """
    Iterates through the child widgets of the supplied
    frame elements trying to set the children's state
    the provided state (e.g. to DISABLED).
    """
    for frame in frames:
        for child in frame.winfo_children():

            if hasattr(child, 'configure'):
                child.configure(state=state)


def create_menus(parent, *menus, start_col=0, start_row=0):
    """
    Creates a new MyMenu instance per provided menu and
    adds them to a dictonary.

    The provided menus must be tuples of menu options and SPARKL
    field names. The selected menu option will be used to populate
    the SPARKL field.

    The menus are placed in the same row, next to each other.
    """
    menu_dict = {}

    for menu in menus:
        options, field_key = menu
        new_menu = MyMenu(parent, options)
        new_menu.grid(column=start_col, row=start_row)
        menu_dict[field_key] = new_menu
        start_col += 1

    return menu_dict


def position_button(button, *menus, padx=40):
    """
    Makes sure the button is in the middle in case
    of two menus.
    """
    if len(menus) == 2:
        button.grid(sticky=W+E, columnspan=2, padx=padx)

    else:
        button.grid()


class MyMenu(OptionMenu):
    """
    Basic drop-down menu class inheriting from OptionMenu.
    """
    def __init__(self, master, options):
        """
        Initialise drop-down using supplied options.
        """
        self.options = options
        self.selected = StringVar()
        OptionMenu.__init__(self, master, self.selected, *self.options)
        self.grid(padx=10, pady=10)
        self._width_match_longest()

    def get_selected(self):
        """
        Return value of selected drop-down element.
        """
        return self.selected.get()

    def _width_match_longest(self):
        """
        Width of menu list must match longest menu item.
        """

        if self.options:
            lengths = [len(x) for x in self.options]
            self.config(width=max(lengths) + 3)


class CryptoFrame(ttk.LabelFrame):
    """
    LabelFrame instance for Bitcoin values. Contains a drop-down
    and a button associated with it.
    """
    def __init__(self, master, text, solicit,  *menus):
        """
        Initilaise frame element and its children.
        """
        ttk.LabelFrame.__init__(self, master, text=text, width=100)
        self.master = master
        self.solicit = solicit
        self.menus = create_menus(self, *menus)
        self.button = Button(self, text='Get')
        self.button.bind('<Button-1>', self.send_solicit)

        position_button(self.button, *menus)

    def send_solicit(self, *_args):
        """
        Uses SPARKL to get the value of Bitcoin in the selected currency
        and write it to the message panel.
        """
        solicit_data = {}

        for key, value in self.menus.items():
            selected = self.menus[key].get_selected()

            if not selected:
                self.master.messages.write_message('Select a currency!')
                return

            solicit_data[key] = selected

        solicit_dict = {
            'solicit': self.solicit,
            'data': solicit_data
        }
        write_response(self.master.service, solicit_dict, self.master.messages)


class GuiMessage(Text):
    """
    Class for the main message panel.
    """
    def __init__(self, master):
        """
        Initialise main message panel.
        Its master must be the root element.
        """
        Text.__init__(self, master, width=50, wrap=CHAR)
        self.insert(END, '')
        self._set_state(DISABLED)

    def _set_state(self, state):
        """
        Sets the state of the text box and saves the
        state into the state attribute.
        Possible states:
            - NORMAL (editable)
            - DISABLED (read-only)
        """
        self.config(state=state)
        self.state = state

    def delete_message(self):
        """
        Deletes the current content
        of the text box.
        """
        if self.state == DISABLED:
            self._set_state(NORMAL)

        self.delete(START_INDEX, END)

    def write_message(self, text):
        """
        Overrides the content of the text box
        with the provided text.
        """
        width = self.cget('width') - 10  # padding
        text = split_text(width, text)

        self.delete_message()
        self.insert(END, text)
        self._set_state(DISABLED)


class ServiceFrame(ttk.LabelFrame):
    """
    LabelFrame instance that contains the service path entry field
    and the related button.
    """
    def __init__(self, master):
        """
        Initialise frame.
        """
        ttk.LabelFrame.__init__(self, master, text='Service path')
        self.master = master
        self.is_reset = False

        # Create entry field with variable.
        self.service_path = StringVar()
        self.service_path_fld = Entry(self, textvariable=self.service_path, width=30)

        # Bind reset and copy-paste functions to entry field.
        self.service_path_fld.bind('<Control-V>', self.paste)
        self.service_path_fld.bind('<Button-1>', self.reset)
        self.service_path_fld.grid(sticky=W, padx=10, pady=10)

        # Add hint to entry field.
        self.set_placeholder()

        # Create button to start entered service.
        self.start_button = Button(self, text='Connect')
        self.start_button.bind('<Button-1>', self.start_service)
        self.start_button.grid()

    def set_placeholder(self):
        """
        Fills the entry field with a faded-grey hint.
        """
        self.service_path.set('e.g. user@sparkl.com/Scratch/Folder/REST')
        self.service_path_fld.configure(foreground='grey')

    def paste(self, *_args):
        """
        Pastes the last value captured with Cmd-C.
        """
        text = self.service_path_fld.selection_get(selection='CLIPBOARD')
        self.service_path_fld.insert('insert', text)

    def reset(self, *_args):
        """
        Removes the placeholder value from the entry field.
        Called only once when the field is first clicked.
        """
        if not self.is_reset:
            self.service_path.set('')
            self.service_path_fld.configure(foreground='black')
            self.is_reset = True

    def start_service(self, *_args):
        """
        Gets the service path entered into the entry field
        and tries to connect to it using the Rest extension.

        Writes a success/error message to the message panel.
        """
        service = self.service_path.get()

        is_valid = validate_string(service)

        if not is_valid:
            self.master.messages.write_message('Enter a valid service path.')
            return

        success, result = open_socket(service)

        if not success:
            self.master.messages.write_message(result)
            return

        # If the websocket opens successfully, enable all other input frames,
        # but disable to service input frame.
        # Also assign the returned service instance to the master and write
        # success message.
        set_frame_state(NORMAL, *self.master.frames)
        set_frame_state(DISABLED, self)
        self.master.service = result
        self.master.messages.write_message('{} is open.'.format(service))


class CryptoGUI(Tk):
    """
    Master GUI element inheriting from Tk.
    In total contains three frames:
        - service_frame:
            A frame where the path to the SPARKL rest service
            can be entered.
        - bitcoin_frame:
            A frame where you can choose a FIAT currency and get
            the price of bitcoin in the selected currency.
        - crypto_frame:
            A frame where you can choose a FIAT currency and and
            a crypto currency and get the latter's price in the
            selected FIAT currency.
    """
    def __init__(self):
        """
        Initialise main GUI element.
        """
        Tk.__init__(self)
        self.maxsize(width=600, height=340)
        self.minsize(width=300, height=200)
        self.title('Cryptocurrency GUI')

        # Specify protocol for exitting the GUI.
        self.protocol(EXIT_PROTOCOL, self.on_close)

        # Attribute set by the start_service method of
        # the service frame.
        self.service = None

        # Main message panel element.
        self.messages = GuiMessage(self)
        self.messages.grid(column=7, columnspan=5)

        # Create frames of the GUI on a vertical pane.
        self.frames = self.create_frames()

        # Disable all but the first frame (the service entry frame).
        # They can only be used if a correct service path was specified.
        set_frame_state(DISABLED, *self.frames[1:])

        # Establish connection to SPARKL on startup.
        self.is_connected = False
        self.login_to_sparkl()

    def login_to_sparkl(self):
        """
        Creates a connection to SPARKL.
        """
        sparkl('connect', 'http://localhost:8000', alias=ALIAS)
        self.is_connected = True
        print('Connected to SPARKL.')

    def logout_from_sparkl(self):
        """
        Closes connection to SPARKL.
        """

        # Gets only called if login was successful.
        if self.is_connected:
            sparkl('close', alias=ALIAS)

            self.is_connected = False
            print('Closed connection.')

    def on_close(self):
        """
        Called when user exits from interface.
        It logs out of SPARKL and ends the mainloop of
        the interface.
        """
        if messagebox.askokcancel(EXIT, EXIT_PROMPT):
            self.logout_from_sparkl()
            self.destroy()

    def create_frames(self):
        """
        Creates the three main frames of the main GUI element
        and positions them vertically on a panel.
        """
        panel = ttk.PanedWindow(self, orient=VERTICAL, height=340)
        btc_frame = CryptoFrame(self, 'Bitcoin', 'Mix/GetBTC',
                                (FIAT_LIST, 'currency'))
        crypto_frame = CryptoFrame(self, 'Other crypto coins', 'Mix/GetCrypto',
                                   (FIAT_LIST, 'currency'),
                                   (CRYPTO_LIST, 'crypto_currency'))
        service_frame = ServiceFrame(self)
        panel.add(service_frame)
        panel.add(btc_frame)
        panel.add(crypto_frame)

        panel.grid(column=0, row=0, sticky=N, columnspan=5)
        return service_frame, btc_frame, crypto_frame
