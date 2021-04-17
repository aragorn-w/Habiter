# Background Python script for repeating work timer
import time
from os import path, environ
from typing import Dict
from msvcrt import getwche

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame  # type: ignore


def valid_number(string_prompt: str, number_type):
    while True:
        response = input(string_prompt)
        try:
            return number_type(response)
        except ValueError:
            print('Response was not numerical, try again.')
            continue


valid_bool_prompt = 'Press \'y\' or \'n\''
def valid_bool(string_prompt: str) -> bool:
    bool_response = None
    while True:
        print(string_prompt, end='', flush=True)
        response = getwche().lower()
        if response == 'y':
            bool_response = True
            break
        if response == 'n':
            bool_response = False
            break
        print('\n\nResponse was not a boolean. try again.')
    print()
    return bool_response


def exercises_dict_input(string_prompt: str) -> Dict[str, int]:
    workouts_list = list(map(str.lstrip, input(string_prompt).split(',')))
    return dict.fromkeys(workouts_list, n_work_minutes)


def seperator_box_msg(message: str, sep_char: str='=', vertical_seperators=True, print_msg=True) -> str:
    seperator = sep_char*len(message)
    prompt_padder = '-'*len(message)
    if vertical_seperators:
        formatted_msg = f'{seperator*3}\n{prompt_padder+message+prompt_padder}\n{seperator*3}'
    else:
        formatted_msg = prompt_padder+message+prompt_padder
    if print_msg:
        print(formatted_msg)
    return formatted_msg


def multi_line_seperator_msg(message: str, sep_char: str ='=', print_msg=True) -> str:
    max_len = 0
    for line in message.split('\n'):
        if len(line) > max_len:
            max_len = len(line)
    seperator = sep_char*max_len
    formatted_msg = f'{seperator}\n{message}\n{seperator}'
    if print_msg:
        print(formatted_msg)
    return formatted_msg


def generate_workout_regimen_str(workout_rep_dict: Dict[str, int]) -> str:
    regiment_str = 'Workout Regimen:'
    for workout in workout_rep_dict:
        regiment_str += f'\n{" "*8}{workout_rep_dict[workout]} {workout}'
    return regiment_str


filepath = path.abspath(__file__)
filedir = path.dirname(filepath)
alarm_sound_path = path.join(filedir, 'loud_alarm.mp3')
n_work_sessions = -1        # -1 means infinite
n_work_minutes = 20.0       # float cuz I love being pedantic about types
workout_exercises = {'ab crunches': 20, 'push-ups': 20}
resume_time = -1.0          # DO NOT CHANGE
unfinished_seconds = -1.0   # DO NOT CHANGE. Default value to mark no previous unfinished session
custom_settings_set = False


multi_line_seperator_msg(seperator_box_msg('<<HABITER - A repeating work-workout alarm>>', print_msg=False))
print('\n\nPress \'ctrl-c\' to exit work sessions. -1 means infinite.\n')

print(f'DEFAULT SETTINGS:\n\tWork sessions: {n_work_sessions}\n\tMinutes per work session: {n_work_minutes}')
for line in generate_workout_regimen_str(workout_exercises).split('\n'):
    print('\t' + line)

pygame.mixer.init()
print('\n\n')
while True:
    choose_default = valid_bool(valid_bool_prompt + ' to use default settings:   ')
    if not choose_default:
        if custom_settings_set:
            use_saved_custom_settings = valid_bool(
                valid_bool_prompt + ' to restore previous custom settings:   ')
        else:
            use_saved_custom_settings = False

        if not use_saved_custom_settings:
            n_work_sessions = valid_number('Number of work sessions:   ', int)
            n_work_minutes = valid_number('Minutes per work session:   ', float)
            workout_exercises = exercises_dict_input('Comma-seperated workout exercises:   ')
            for workout in workout_exercises:
                workout_exercises[workout] = valid_number(f'{workout} per work session:   ', int)
            custom_settings_set = True
    print()

    workout_regimen_str = generate_workout_regimen_str(workout_exercises)
    
    if unfinished_seconds > 0.0:
        complete_prev_session = valid_bool(valid_bool_prompt + ' to finish previous session:   ')
    else:
        complete_prev_session = False
    if not complete_prev_session:
        unfinished_seconds = 0.0
    try:
        session_index = 1   # indexing starts at 1
        while True:
        # for session_n in range(int(complete_prev_session) + n_work_sessions):
            resume_time = time.time()
            if session_index != 1 or not complete_prev_session:
                seperator_box_msg(f'WORK SESSION {session_index} STARTED')
                time.sleep(n_work_minutes * 60.0)
            else:
                seperator_box_msg('PREVIOUS WORK SESSION RESUMED')
                print(f'\n{round(unfinished_seconds/60.0, 2)} minutes remaining...')
                time.sleep(unfinished_seconds)
            print('\n')

            multi_line_seperator_msg(workout_regimen_str)
            pygame.mixer.music.load(alarm_sound_path)
            pygame.mixer.music.play(-1)
            print('\n')

            print('Press any key to stop workout alarm:   ', end='', flush=True)
            getwche()
            pygame.mixer.music.pause()

            print('\nPress enter to begin next work session:   ', end='', flush=True)
            getwche()
            print('\n\n\n')

            if n_work_sessions != -1 and session_index >= n_work_sessions:
                break
            if session_index != 0 or not complete_prev_session:
                session_index += 1
    except KeyboardInterrupt:
        pygame.mixer.music.pause()
        print('\n\n')
        seperator_box_msg('Work sessions canceled', vertical_seperators=False)
        print('\n')
        if unfinished_seconds > 0.0:
            unfinished_seconds -= time.time() - resume_time
        else:
            unfinished_seconds = n_work_minutes*60.0 - (time.time() - resume_time)
        if unfinished_seconds >= n_work_minutes*60.0:    # user canceled before next work session, while finishing a previous incomplete session, or after finishing a previous incomplete session
            unfinished_seconds = -1.0
        continue
    unfinished_seconds = -1.0
