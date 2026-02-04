import time
import datetime
import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import pygame

SOUND_FILE = "Memory_Reboot.mp3"


def parse_alarm_time(user_input: str) -> datetime.time:
    """
    Accepts HH:MM or HH:MM:SS and returns a time object.
    """
    try:
        parts = list(map(int, user_input.split(":")))
        if len(parts) == 2:
            h, m = parts
            s = 0
        elif len(parts) == 3:
            h, m, s = parts
        else:
            raise ValueError

        return datetime.time(hour=h, minute=m, second=s)

    except ValueError:
        print("❌ Invalid time format. Use HH:MM or HH:MM:SS")
        sys.exit(1)


def wait_for_alarm(alarm_time: datetime.time):
    print(f"⏰ Alarm set for {alarm_time.strftime('%H:%M:%S')}")

    try:
        while True:
            now = datetime.datetime.now().time()

            if now >= alarm_time:
                trigger_alarm()
                break

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Alarm cancelled")
        sys.exit(0)


def trigger_alarm():
    print("🔔 WAKE UP!")

    pygame.mixer.init()
    pygame.mixer.music.load(SOUND_FILE)
    pygame.mixer.music.play()

    try:
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)
    finally:
        pygame.mixer.quit()


if __name__ == "__main__":
    alarm_input = input("Enter alarm time (HH:MM or HH:MM:SS): ")
    alarm_time = parse_alarm_time(alarm_input)
    wait_for_alarm(alarm_time)
