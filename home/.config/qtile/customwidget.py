#!/usr/bin/env python

import re
import subprocess
import psutil
import socket
from datetime import datetime
from libqtile import bar, widget, hook

from libqtile.log_utils import logger
from pprint import pformat
import time


attr_icon_font = 'font="Font Awesome 5 Free"'
attr_icon_font_bold = 'font="Font Awesome 5 Free Solid"'
attr_alpha = 'alpha="45%"'
attr_more_alpha = 'alpha="35%"'
attr_color_normal = 'color="#969896"'
attr_color_green = 'color="#b5bd68"'
attr_color_yellow = 'color="#f0c674"'
attr_color_red = 'color="#cc6666"'


BUTTON_LEFT = 1
BUTTON_RIGHT = 3
BUTTON_UP = 4
BUTTON_DOWN = 5


# Debugging methods ###########################################################


def DEBUG_MODE(callback):
    def wrapper(*args, **kwargs):
        try:
            return callback(*args, **kwargs)
        except Exception as e:
            logger.error(f'Something wrong: {e} [{type(e)}]')
    return wrapper


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print(f'{method.__name__}  {(te - ts) * 1000:.6f}ms')
        return result
    return timed


# End of debugging methods ####################################################


def _spacer(length=20):
    return widget.Spacer(length=length)


def get_condition(value, warn=50, crit=85, alt_color=None):
    value = int(value)

    if crit < warn:
        value *= -1
        warn *= -1
        crit *= -1

    if value >= crit:
        return attr_color_red

    if value >= warn:
        return attr_color_yellow

    return alt_color if alt_color else attr_color_normal


# print('straight ------ warn: 30, crit: 70')
# for i in range(10, 100, 10):
#     print(f'{i}:', get_condition(i, warn=30, crit=70))
# print('reversed ------ warn: 70, crit: 30')
# for i in range(10, 100, 10):
#     print(f'{i}:', get_condition(i, warn=70, crit=30))


def humanize_bytes(value):
    byte_suffix = list('BKMGT')
    while value > 1024. and len(byte_suffix) > 1:
        value /= 1024.
        byte_suffix.pop(0)
    precision = 1 if value < 10 else 0
    return f'{value:.{precision}f}{byte_suffix[0]}'


# for i in range(1, 15):
#     num = int('1' * i)
#     print(humanize_bytes(num))


class CustomWidgetText(widget.base._TextBox):

    def __init__(self, width=bar.CALCULATED, **config):
        self.markup = True
        # widget.base._TextBox.__init__(self, text=text, width=width, **config)
        widget.base._TextBox.__init__(self, width=width, **config)
        self.text = self.get_text()

    def update(self, *args, text=None):
        if text is None:
            text = self.get_text()
        if len(text) == len(self.text):
            self.text = text
            self.draw()
        else:
            self.text = text
            self.bar.draw()

    def button_press(self, x, y, button):
        if button == BUTTON_RIGHT:
            self.update()

    # Using from outside, like qshell-cmd
    def cmd_update(self):
        self.update()


class CustomWidgetPoll(widget.base.InLoopPollText):

    def __init__(self, **config):
        self.markup = True
        widget.base.InLoopPollText.__init__(self, **config)
        self.update_interval = 5

    def button_press(self, x, y, button):
        if button == BUTTON_RIGHT:
            self.text = self.poll()
            self.bar.draw()


class Groups(widget.GroupBox):

    def button_press(self, x, y, button):
        self.clicked = None
        group = None

        if button == BUTTON_LEFT:
            group = self.get_clicked_group(x, y)
            if group is self.qtile.current_group:
                group = self.qtile.current_screen.previous_group
            if not self.disable_drag:
                self.clicked = group

        if group:
            self.bar.screen.set_group(group)


class StackItems(CustomWidgetText):

    def __init__(self, width=bar.CALCULATED, **config):
        self.markup = True
        widget.base._TextBox.__init__(self, width=width, **config)

    def _configure(self, qtile, bar):
        widget.base._TextBox._configure(self, qtile, bar)
        hook.subscribe.focus_change(self.update)
        hook.subscribe.float_change(self.update)
        hook.subscribe.layout_change(self.update)

    def get_clients(self, layout, window):
        if layout.name == 'stack':
            return layout.clients
        elif layout.name == 'ranger-terminals':
            if layout._slice.window is window:
                window.side = True
            return layout.fallback.clients
        elif layout.name == 'columns':
            return layout.columns[layout.current].clients
        elif layout.name == 'max':
            return layout.clients.clients

    @DEBUG_MODE
    def get_text(self):

        current_window = self.qtile.current_window

        if current_window is None:
            return ''

        stack = self.get_clients(
            self.qtile.current_layout, current_window)

        if hasattr(current_window, 'side'):
            return f'<span {attr_color_normal} {attr_alpha}>SIDE</span>'

        if current_window.floating:
            return f'<span {attr_color_normal} {attr_alpha}>FLOATING</span>'

        if not stack or len(stack) < 2:
            return f'<span {attr_color_normal} {attr_alpha}>SINGLE</span>'

        item_icon = []
        for item in stack:
            if item is current_window:
                item_icon.append('▣')
            else:
                item_icon.append(f'<span {attr_alpha}>□</span>')

        return (
            f'<span {attr_color_normal} rise="9000">'
            + f'<span {attr_alpha}>STACK: </span>'
            + '<span size="14000">'
            + '<span size="2000"> </span>'.join(item_icon)
            + '</span></span>')

    def button_press(self, x, y, button):
        if button == BUTTON_LEFT:
            self.qtile.current_layout.cmd_down()
            self.update()
        elif button == BUTTON_RIGHT:
            self.qtile.current_layout.cmd_up()
            self.update()


class Temperature(CustomWidgetPoll):

    def __init__(self):
        super().__init__()
        self.update_interval = 1

    def poll(self):
        temp = psutil.sensors_temperatures()['acpitz'][0].current
        if temp < 70:
            icon = ''
        elif 70 <= temp < 90:
            icon = ''
        elif 90 <= temp:
            icon = ''
        condition = get_condition(temp, warn=70, crit=90)

        return (
            f'<span {condition}>'
            f'<span {attr_icon_font} {attr_alpha} size="10500">{icon}</span> '
            f'{temp:.0f}°C</span>')


class CPU(CustomWidgetPoll):

    def __init__(self):
        super().__init__()
        self.update_interval = 1

    def poll(self):
        cpu = psutil.cpu_percent()
        condition = get_condition(cpu, warn=70, crit=90)

        return (
            f'<span {condition}>'
            f'<span {attr_icon_font} {attr_more_alpha} size="10500"></span> '
            f'{cpu:.0f}%</span>')


class Memory(CustomWidgetPoll):

    @DEBUG_MODE
    def poll(self):
        used = psutil.virtual_memory().used
        condition = get_condition(
            used, warn=(5.5 * 1024 * 1024 * 1024), crit=7000000000)

        return (
            f'<span {condition}>'
            f'<span {attr_icon_font_bold} '
            f'{attr_more_alpha} size="10000"></span> '
            f'{humanize_bytes(used)}</span>')


class Disk(CustomWidgetPoll):

    def __init__(self):
        super().__init__()
        self.update_interval = 60

    def poll(self):
        free = psutil.disk_usage('/home').free
        condition = get_condition(free, warn=20000000000, crit=10000000000)

        return (
            f'<span {condition}>'
            f'<span {attr_icon_font} {attr_alpha} size="10500"></span> '
            f'{humanize_bytes(free)}</span>')


class Keyboard(CustomWidgetText):

    def get_text(self):
        try:
            xkblayout_out = self.call_process(
                ['xkblayout-state', 'print', '%s'])

            if xkblayout_out == 'us':
                return (f'<span {attr_color_normal}>'
                        f'<span {attr_alpha} size="10500"></span> ENG</span>')
            elif xkblayout_out == 'ru':
                return (f'<span {attr_color_yellow}>'
                        f'<span {attr_alpha} size="10500"></span> RUS</span>')

        except subprocess.CalledProcessError:
            return

    def button_press(self, x, y, button):
        if button == BUTTON_LEFT:
            try:
                subprocess.call(['xkblayout-state', 'set', '+1'])
                self.update()
            except subprocess.CalledProcessError:
                return


class Network(CustomWidgetText):

    @DEBUG_MODE
    def get_text(self):
        address = None
        for addr in psutil.net_if_addrs()['wlp9s0']:
            if addr.family is socket.AF_INET:
                address = addr.address

        if not address:
            return (f'<span {attr_color_normal} {attr_alpha}>'
                    f'<span {attr_icon_font}></span> NO CARRIER</span>')

        return (f'<span {attr_color_normal}>'
                f'<span {attr_icon_font} {attr_alpha}></span>'
                f' {address}</span>')


class DAC(CustomWidgetPoll):

    hw_params = '/proc/asound/DACE07K/pcm0p/sub0/hw_params'
    dac_regex = re.compile(r'format:\s.(\d{2}).*rate:\s(\d{2})', re.DOTALL)

    def __init__(self):
        super().__init__()
        self.update_interval = 1

    def poll(self):
        try:
            with open(self.hw_params, 'r') as f:
                dac = f.read()

            if dac == 'closed\n':
                return (
                    f'<span {attr_color_normal} {attr_alpha}>'
                    f'<span size="10500"></span> CLOSED</span>')  # 
            else:
                bit, rate = self.dac_regex.search(dac).groups()
                return (f'<span {attr_color_normal}>'
                        f'<span {attr_alpha} size="10500"></span>'
                        f' {bit}bit, {rate}KHz</span>')
        except FileNotFoundError:
            return f'<span {attr_alpha}>DAC UNPLUGGED</span>'


class Volume(CustomWidgetText):

    volume_regex = re.compile(r'\[(\d?\d?\d?)%\]')

    def button_press(self, x, y, button):
        if button == BUTTON_DOWN:
            subprocess.call(['amixer', 'set', 'PCM', '5%-'])
        elif button == BUTTON_UP:
            subprocess.call(['amixer', 'set', 'PCM', '5%+'])

        self.update()

    def get_text(self):
        try:
            mixer_out = self.call_process(['amixer', 'sget', 'PCM'])

            if '[off]' in mixer_out:
                return f'<span {attr_alpha}>[OFF]</span>'

            volume = self.volume_regex.search(mixer_out).groups()[0]
            condition = get_condition(volume, warn=60, crit=85,
                                      alt_color=attr_color_green)

            return f'<span {condition}>[{volume}%]</span>'

        except (subprocess.CalledProcessError, AttributeError):
            return


class Battery(CustomWidgetPoll):

    def __init__(self):
        super().__init__()
        self.update_interval = 30

    def poll(self):
        battery = psutil.sensors_battery()

        if battery.power_plugged:
            return (f'<span {attr_icon_font_bold} {attr_color_normal}'
                    f' {attr_alpha} size="12300"></span>')  # 

        if battery.percent < 20:
            icon = ''
        elif 20 <= battery.percent < 40:
            icon = ''
        elif 40 <= battery.percent < 60:
            icon = ''
        elif 60 <= battery.percent < 80:
            icon = ''
        elif 80 <= battery.percent:
            icon = ''
        condition = get_condition(battery.percent, warn=50, crit=20)

        return f'<span {condition} size="11000">{icon}</span>'


class Clock(CustomWidgetPoll):

    def get_day_suffix(self, day):
        if 3 < day < 21 or 23 < day < 31:
            return 'th'
        else:
            return {1: 'st', 2: 'nd', 3: 'rd'}[day % 10]

    def poll(self):
        now = datetime.now()
        return now.strftime((
            f'<span {attr_color_normal}>%^B %-d<span size="7000"'
            f' rise="3500" underline="low" underline_color="#444545">'
            f'{self.get_day_suffix(now.day)}</span> '
            f'<span {attr_alpha}>%^A</span> %R</span>'))
