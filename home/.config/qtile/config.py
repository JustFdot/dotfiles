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
    Key, Screen, Group, Drag, Click, ScratchPad, DropDown, Match, Rule)
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook, scratchpad
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


keys = [

    # Key([mod], 'h', lazy.layout.left()),
    # Key([mod], 'j', lazy.layout.down()),
    # Key([mod], 'k', lazy.layout.up()),
    # Key([mod], 'l', lazy.layout.right()),
    # Key([mod, 'shift'], 'h', lazy.layout.move_left()),
    # Key([mod, 'shift'], 'j', lazy.layout.move_down()),
    # Key([mod, 'shift'], 'k', lazy.layout.move_up()),
    # Key([mod, 'shift'], 'l', lazy.layout.move_right()),
    # Key([mod, alt], 'h', lazy.layout.integrate_left()),
    # Key([mod, alt], 'j', lazy.layout.integrate_down()),
    # Key([mod, alt], 'k', lazy.layout.integrate_up()),
    # Key([mod, alt], 'l', lazy.layout.integrate_right()),
    # Key([mod], 'd', lazy.layout.mode_horizontal()),
    # Key([mod], 'v', lazy.layout.mode_vertical()),
    # Key([mod, 'shift'], 'd', lazy.layout.mode_horizontal_split()),
    # Key([mod, 'shift'], 'v', lazy.layout.mode_vertical_split()),
    # Key([mod], 'a', lazy.layout.grow_width(30)),
    # Key([mod], 'x', lazy.layout.grow_width(-30)),
    # Key([mod, 'shift'], 'a', lazy.layout.grow_height(30)),
    # Key([mod, 'shift'], 'x', lazy.layout.grow_height(-30)),
    # # Key([mod], 'C-5', lazy.layout.size(500)),
    # # Key([mod], 'C-8', lazy.layout.size(800)),
    # Key([mod], 'n', lazy.layout.reset_size()),


    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
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


    Key([mod, 'control'], 'f', lazy.window.toggle_fullscreen()),
    Key([alt], 'space', lazy.window.toggle_floating()),


    Key([alt, 'control'], 'Up',
        lazy.spawn('amixer set PCM 5%+'),
        lazy.function(update_widget, 'volume')),
    Key([alt, 'control'], 'Down',
        lazy.spawn('amixer set PCM 5%-'),
        lazy.function(update_widget, 'volume')),


    # Switch window focus to other pane(s) of stack
    Key([mod], 'space', lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, 'shift'], 'space', lazy.layout.rotate()),

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
    # Key([mod], 'r', lazy.spawncmd()),

    # Run programs
    Key([mod], 'Return', lazy.function(terminal)),
    Key([mod], 'r', lazy.spawn('zsh -c "rofi -show run"')),
    # Need to get new time each execute
    # Key([mod], 't', lazy.spawn(
    #     f"notify-send -i clock -t 700 \"<span
    #     size='30000'>{datetime.now().strftime('%R')}</span>\"")),

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
    Group(name='a', label='', layout='max'),
    Group(name='s', label='', layout='columns',
          spawn=[terminal(execute='ranger'),
                 terminal(execute='sudo -i'),
                 terminal()]),
    Group(name='d', label='', layout='max',
          spawn=['emacs']),
    Group(name='f', label='', layout='max',
          spawn=[terminal(execute='ncmpcpp')]),
    Group(name='u', label='', layout='max'),
    Group(name='i', label='', layout='max'),
    Group(name='o', label='', layout='max'),
    Group(name='p', label='', layout='max')
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.screen.toggle_group(i.name)),
        Key([mod, 'shift'], i.name, lazy.window.togroup(i.name)),
    ])


# groups.append(
#     ScratchPad('scratchpad', [
#         # define a drop down terminal.
#         # it is placed in the upper third of screen by default.
#         # DropDown('todo', f'emacs {home}/.emacs.d/todo.org',
#         #          x=0.25, y=0.1, width=0.5, height=0.8, opacity=0.95),

#         # DropDown('translate',
#         #          ('google-chrome-stable '
#         #           f'--user-data-dir={home}/.config/chrome-empty-profile '
#         #           '--app="https://translate.google.as/?sl=en&tl=ru"'),
#         #          x=0.1, y=0.1, width=0.8, height=0.8, opacity=0.95),

#         # define another terminal exclusively for qshell at different position
#         # DropDown('qshell', 'urxvt -hold -e qshell',
#         #         x=0.05, y=0.4, width=0.9, height=0.6, opacity=0.9,
#         #         on_focus_lost_hide=True) ]),
#     ]))

# keys.extend([
#     Key([alt], 'Escape', lazy.group['scratchpad'].dropdown_toggle('todo')),
#     Key([mod], 't', lazy.group['scratchpad'].dropdown_toggle('translate'))
# ])


layout_theme = {
    'border_width': 3,
    'margin': 14,
    'insert_position': 1,
    'border_focus': '#C5C8C6',
    'border_focus_stack': '#C5C8C6',
    'border_normal': '#151617',
    'border_normal_stack': '#151617'}


layouts = [
    layout.Max(**layout_theme),
    layout.Columns(**layout_theme, split=False),
    # Plasma(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.MonadTall(**layout_theme),
    # layout.Stack(num_stacks=2, **layout_theme)
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
    'borderwidth': 2,
    'disable_drag': True,
    'font': 'Font Awesome 5 Free Solid',
    'fontsize': 16,
    'hide_unused': True,
    'highlight_color': background,
    'highlight_method': 'block',
    'margin': 1,
    'margin_x': 0,
    'padding': 7,
    'padding_x': 10,
    # 'this_current_screen_border': '#444545',
    # 'this_current_screen_border': '#34353c',
    # 'this_current_screen_border': '#1f2020',
    'this_current_screen_border': '#232628',
    'this_screen_border': white,
    'urgent_alert_method': 'line',
    'urgent_border': yellow,
    'urgent_text': yellow,
    'use_mouse_wheel': False,
}

# group_box_properties = {
#     'active': '686a69',
#     'borderwidth': 2,
#     'disable_drag': True,
#     'font': 'Font Awesome 5 Free Solid',
#     'fontsize': 16,
#     'hide_unused': True,
#     'highlight_color': background,
#     'highlight_method': 'line',
#     'margin': 0,
#     'padding': 7,
#     'padding_x': 12,
#     'rounded': False,
#     'this_current_screen_border': white,
#     'this_screen_border': white,
#     'urgent_alert_methon': 'block',
#     'urgent_border': yellow,
#     'urgent_text': black,
#     'use_mouse_wheel': False,
# }

screens = [
    Screen(
        bottom=bar.Bar([
            # widget.GroupBox(**group_box_properties),
            customwidget.Groups(**group_box_properties),
            widget.sep.Sep(foreground='#444545'),
            # widget.CurrentLayoutIcon(
            #     scale=.5,
            #     custom_icon_paths=[f'{home}/.config/qtile/layout-icons']),
            customwidget._spacer(length=10),
            customwidget.StackItems(),
            # customwidget.Test(),
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


def get_window_size(screen_width):
    return (1496, 875) if screen_width == 1920 else (1096, 604)


# SP = ScratchPad('scratchpad', [])
# groups.append(SP)
# logger.error(pformat(SP.dropdowns))


@DEBUG_MODE
@hook.subscribe.client_new
def floating_windows(window):
    # if window.window.get_wm_class() == ('float-window-wide', 'URxvt'):
    if window.name in ['ncmpcpp', 'system-update']:
        window.floating = True
        window.width, window.height = get_window_size(screens[0].width)

    if window.name == 'system-update':
        window.togroup('p')

    # if window.name == 'todo.org':
    #     SP.dropdowns['todo'] = scratchpad.WindowVisibilityToggler(
    #         'todo', window, on_focus_lost_hide=False, warp_pointer=False)
    #     window.togroup('scratchpad')

        # scratchpad.DropDownToggler(window, 'todo', {
        #     'name': 'todo',
        #     'x': 0,
        #     'y': 0,
        #     'width': 1000,
        #     'height': 500,
        #     'opacity': 1,
        #     'on_focus_lost_hide': False,
        #     'warp_pointer': False,
        # })
        # window.togroup('p')


# todo = Rule(Match(title='todo.org'), float=True)
# keys.extend([
#     Key([alt], 'Escape', lazy.function(logger.error, todo)),
#     # Key([alt], 'Escape', lazy.group['scratchpad'].dropdown_toggle('todo')),
# ])


auto_fullscreen = True
focus_on_window_activation = 'smart'

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = 'LG3D'
