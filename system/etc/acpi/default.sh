#!/bin/sh
# /etc/acpi/default.sh
# Default acpi script that takes an entry for all actions

set "$@"

group=${1%%/*}
action=${1#*/}
# device=$2
id=$3
value=$4

# None of that shit works in POSIX sh
# read -r XUSER DISPLAY <<< "$(ps au | grep -m1 xinit | awk '{print $1" "$15}')"
# user_vars=("$(pgrep -a xinit | sed -r 's/.*(\/home\/(\w*)).*(:[0-9]).*/\1 \2 \3/')")
get_xuser () {
    xinit_cmd=$(pgrep -a xinit)
    DISPLAY="$(echo "$xinit_cmd" | grep -o ':[0-9]')"
    XUSER="$(echo "$xinit_cmd" | sed -E 's/.*\/home\/(.*)\/.*/\1/')"
    XAUTHORITY="/home/$XUSER/.Xauthority"
    export DISPLAY XAUTHORITY XUSER
}

debug_log () {
    echo "[$(date '+%d.%m.%Y %H:%M:%S')] $*" >> /tmp/acpi.log
}

log_unhandled() {
	logger "ACPI event unhandled: $*"
}

# debug_log "-----"
# debug_log "Group: $group; Action: $action; Id: $id"

case "$group" in
	button)
		case "$action" in
			power)
				# /etc/acpi/actions/powerbtn.sh
                                case "$value" in
                                        "00000000")  # Power off
                                                echo mem > /sys/power/state
                                                ;;
                                        *)  # Power on
                                                pkill -HUP -f eyeskeeper
                                                /usr/local/bin/pick-peripheral
                                                ;;
                                esac
                                ;;

			# if your laptop doesnt turn on/off the display via hardware
			# switch and instead just generates an acpi event, you can force
			# X to turn off the display via dpms.  note you will have to run
			# 'xhost +local:0' so root can access the X DISPLAY.
			lid)
                                case "$id" in
                                        open) /usr/local/bin/pick-peripheral ;;
                                        close) /usr/local/bin/pick-peripheral monitor ;;
                                esac
				;;

			*)	log_unhandled "$@" ;;
		esac
		;;

	ac_adapter)
                get_xuser
		case "$value" in
			# Add code here to handle when the system is unplugged
			# (maybe change cpu scaling to powersave mode).  For
			# multicore systems, make sure you set powersave mode
			# for each core!
			*0)
			#	cpufreq-set -g powersave
                                su - "$XUSER" -c "/usr/bin/notify-send -i remove 'ACPI EVENT' 'AC adapter unplugged'"
				;;

			# Add code here to handle when the system is plugged in
			# (maybe change cpu scaling to performance mode).  For
			# multicore systems, make sure you set performance mode
			# for each core!
			*1)
			#	cpufreq-set -g performance
                                su - "$XUSER" -c "/usr/bin/notify-send -i add 'ACPI EVENT' 'AC adapter plugged'"
				;;

			*)	log_unhandled "$@" ;;
		esac
		;;

	*)	log_unhandled "$@" ;;
esac

# debug "group: $group, action: $action, id: $id, value: $value"
# debug "DISPLAY: $DISPLAY, XAUTHORITY: $XAUTHORITY, XUSER: $XUSER"
