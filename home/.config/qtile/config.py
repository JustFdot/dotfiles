# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile.config import (
    Key, Screen, Group, Drag, Click)
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
# from plasma import Plasma

import customwidget

from libqtile.log_utils import logger
from pprint import pformat

try:
    from typing import List  # noqa: F401
except ImportError:
    pass


def DEBUG_MODE(callback):
    def wrapper(*args, **kwargs):
        try:
            return callback(*args, **kwargs)
        except Exception as e:
            logger.error(f'Something wrong: {e} [{type(e)}]')
    return wrapper


mod = 'mod4'
alt = 'mod1'
home = os.path.expanduser('~')


def update_widget(qtile, widget):
    try:
        qtile.widgets_map[widget].update()
    except KeyError:
        logger.exception(f'Wrong widget name: {widget}')
    except AttributeError:
        logger.exception(f'Widget {widget} has no method update')


@DEBUG_MODE
def terminal(qtile=None, execute=None):
    cmd = 'st'
    with open('/tmp/active-monitor', 'r') as f:
        if 'VGA1' in f.read():
            cmd = f'{cmd} -f "Hack:pixelsize=20"'
    if execute:
        cmd = f'{cmd} -e {execute}'

    # logger.error(pformat(dir(qtile)))
    return qtile.cmd_spawn(cmd) if qtile is not None else cmd


@DEBUG_MODE
def custom_focus(qtile, direction):
    # logger.error(pformat(dir(qtile.current_layout)))
    if qtile.current_layout.name == 'ranger-terminals':
        if qtile.current_window.name == 'ranger-window':
            qtile.current_group.cmd_focus_back()
        else:
            qtile.current_group.cmd_focus_by_name('ranger-window')
    elif qtile.current_layout.name == 'columns':
        if direction == 'left':
            qtile.current_layout.cmd_left()
        elif direction == 'right':
            qtile.current_layout.cmd_right()
    else:
        qtile.current_layout.cmd_next()


keys = [

    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "h", lazy.function(custom_focus, 'left')),
    Key([mod], "l", lazy.function(custom_focus, 'right')),
    # Key([mod], "l", lazy.layout.right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod], "Return", lazy.layout.toggle_split()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        lazy.function(update_widget, 'stackitems')),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        lazy.function(update_widget, 'stackitems')),
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        lazy.function(update_widget, 'stackitems')),
    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        lazy.function(update_widget, 'stackitems')),


    Key([mod, 'control'], 'f', lazy.window.toggle_maximize()),
    Key([alt], 'space', lazy.window.toggle_floating()),


    Key([alt, 'control'], 'Up',
        lazy.spawn('amixer set PCM 5%+'),
        lazy.function(update_widget, 'volume')),
    Key([alt, 'control'], 'Down',
        lazy.spawn('amixer set PCM 5%-'),
        lazy.function(update_widget, 'volume')),


    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, 'shift'], 'Return', lazy.layout.toggle_split()),

    # Toggle between different layouts as defined below
    Key([mod, 'shift'], 'Tab', lazy.next_layout()),

    Key([mod], 'Tab', lazy.screen.toggle_group()),
    Key([mod, 'shift'], 'w', lazy.window.kill()),

    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'q', lazy.shutdown()),

    # Run programs
    Key([mod], 'Return', lazy.function(terminal)),
    Key([mod], 'r', lazy.spawn('zsh -c "rofi -show run"')),

    Key([mod], 'Print', lazy.spawn(
        f'scrot "qtile.png" -e "mv $f {home}/img/shots/"')),
    # Key([mod], 'Print', lazy.spawn(
    #     f'scrot "%d.%m.%Y[$wx$h]%T.png" -e "mv $f {home}/img/shots/"')),
    Key([mod], 'Escape', lazy.spawn(f'/usr/local/bin/screensaver')),
    Key(['control'], 'space',
        lazy.spawn('xkblayout-state set +1'),
        lazy.function(update_widget, 'keyboard')),
]

for num in range(1, 10):
    keys.append(
        Key([alt, 'control'], f'{num}',
            lazy.spawn(f'amixer set PCM {num}0%'),
            lazy.function(update_widget, 'volume')))


groups = [
    Group(name='a', label='', layout='stack'),
    Group(name='s', label='', layout='ranger-terminals',
          spawn=['st -t ranger-window -e ranger',
                 'st -e sudo -i',
                 'st']),
    Group(name='d', label='', layout='stack',
          spawn=['emacs']),
    Group(name='f', label='', layout='stack',
          spawn=['st -e ncmpcpp']),
    Group(name='u', label='', layout='stack'),
    Group(name='i', label='', layout='stack'),
    Group(name='o', label='', layout='stack'),
    Group(name='p', label='', layout='stack')
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.screen.toggle_group(i.name)),
        Key([mod, 'shift'], i.name, lazy.window.togroup(i.name)),
    ])


layout_theme = {
    'border_width': 3,
    'margin': 14,
    'insert_position': 1,
    'border_focus': '#C5C8C6',
    'border_focus_stack': '#C5C8C6',
    'border_normal': '#151617',
    'border_normal_stack': '#151617'}


layouts = [
    layout.Stack(num_stacks=1, border_width=0),
    layout.Columns(split=False, **layout_theme),
    layout.Slice(
        fallback=layout.Stack(num_stacks=1, name='term-stack', **layout_theme),
        name='ranger-terminals', width=600, wname='ranger-window')
]


widget_defaults = dict(
    font='Hack',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

background = '0d0e0f'
foreground = '969896'
black = '1d1f21'
red = 'cc6666'
green = 'b5bd68'
yellow = 'f0c674'
blue = '81a2be'
magenta = 'b294bb'
cyan = '8abeb7'
white = 'c5c8c6'
gray = '4a4f4f'

group_box_properties = {
    'active': '797b7a',
    'rounded': False,
    'borderwidth': 0,
    'disable_drag': True,
    'font': 'Font Awesome 5 Free Solid',
    'fontsize': 16,
    'hide_unused': True,
    'highlight_color': background,
    'highlight_method': 'block',
    'margin': 1,
    'margin_x': 0,
    'padding': 7,
    'padding_x': 14,
    'this_current_screen_border': '2d2e2e',
    'urgent_alert_method': 'block',
    'urgent_border': '3d321e',
    'use_mouse_wheel': False,
}

screens = [
    Screen(
        bottom=bar.Bar([
            customwidget.Groups(**group_box_properties),
            widget.sep.Sep(foreground='#444545'),
            customwidget._spacer(length=10),
            customwidget.StackItems(),
            customwidget._spacer(length=bar.STRETCH),

            widget.Systray(),

            customwidget.Temperature(),
            customwidget._spacer(),
            customwidget.CPU(),
            customwidget._spacer(),
            customwidget.Memory(),
            customwidget._spacer(),
            customwidget.Disk(),
            customwidget._spacer(),
            customwidget.Keyboard(),
            customwidget._spacer(),
            customwidget.Network(),
            customwidget._spacer(),
            customwidget.DAC(),
            customwidget.Volume(),
            customwidget._spacer(),
            customwidget.Battery(),
            customwidget._spacer(),
            customwidget.Clock(),
            customwidget._spacer(length=10),
        ], 32, background=background))]


# Drag floating layouts.
mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front())
]


def get_window_size(screen_width):
    return (1496, 875) if screen_width == 1920 else (1096, 604)


@DEBUG_MODE
@hook.subscribe.client_new
def floating_windows(window):
    # if window.window.get_wm_class() == ('float-window-wide', 'URxvt'):
    if window.name in ['ncmpcpp', 'tag-update']:
        window.floating = True
        window.width, window.height = get_window_size(screens[0].width)

    if window.name == 'tag-update':
        window.togroup('p')


@hook.subscribe.startup_once
def autostart():
    subprocess.call(['/usr/local/bin/pick-peripheral'])


@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    # Think about using that hook for ~pick-peripheral monitor~ things
    qtile.cmd_restart()


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = 'smart'

floating_layout = layout.Floating(
    border_focus=black,
    border_width=4,
    float_rules=[
        {'wmclass': 'confirm'},
        {'wmclass': 'dialog'},
        {'wmclass': 'download'},
        {'wmclass': 'error'},
        {'wmclass': 'file_progress'},
        {'wmclass': 'notification'},
        {'wmclass': 'splash'},
        {'wmclass': 'toolbar'},
        {'wmclass': 'confirmreset'},  # gitk
        {'wmclass': 'makebranch'},  # gitk
        {'wmclass': 'maketag'},  # gitk
        {'wname': 'branchdialog'},  # gitk
        {'wname': 'pinentry'},  # GPG key password entry
        {'wmclass': 'ssh-askpass'},  # ssh-askpass
        {'wmclass': 'float-window'},
    ])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = 'LG3D'
