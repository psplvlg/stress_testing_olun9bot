import os

from generate_test import generate_test
from subprocess import run, STDOUT, PIPE, Popen

CONST = 10 ** 4


def find_test(chat_id, test_format, correct_id, bad_id):
    for it in range(CONST):
        if not check_ans(chat_id, test_format, correct_id, bad_id):
            path = f"user_files/{chat_id}/"
            in_file = open(path + "in.txt")
            in_txt = in_file.read()

            cmd = 'python ' + path

            Q1 = (cmd + f'correct/{correct_id}').split()
            cmd_f = Popen(Q1, stdin=PIPE, stdout=PIPE, stderr=STDOUT, text=True)
            correct_out = cmd_f.communicate(input=in_txt)[:-1]

            Q2 = (cmd + f'bad/{bad_id}').split()
            cmd_f = Popen(Q2, stdin=PIPE, stdout=PIPE, stderr=STDOUT, text=True)
            bad_out = cmd_f.communicate(input=in_txt)[:-1]

            cor = open(path + "correct_out.txt", "wt")
            print(str(*correct_out).rstrip(), file=cor)
            cor.close()
            bad = open(path + "bad_out.txt", "wt")
            print(str(*bad_out).rstrip(), file=bad)
            bad.close()
            return True
    return False


def check_ans(chat_id, test_format, correct_id, bad_id):
    generate_test(chat_id, test_format)
    path = f"user_files/{chat_id}/"
    in_file = open(path + "in.txt")
    in_txt = in_file.read()

    cmd = 'python ' + path

    Q1 = (cmd + f'{correct_id}').split()
    cmd_f = Popen(Q1, stdin=PIPE, stdout=PIPE, stderr=STDOUT, text=True)
    correct_out = cmd_f.communicate(input=in_txt)[:-1]

    Q2 = (cmd + f'{bad_id}').split()
    cmd_f = Popen(Q2, stdin=PIPE, stdout=PIPE, stderr=STDOUT, text=True)
    bad_out = cmd_f.communicate(input=in_txt)[:-1]

    return correct_out == bad_out
