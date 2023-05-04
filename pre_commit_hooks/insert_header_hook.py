"""Pre-commit hook - File header inserter for python files."""
import argparse
import datetime
import os
from typing import Optional, Sequence

import git


def check_header(filename: str, organisation_name: str ,project_name: str):  # noqa C901
    """Check the header & updates the header."""
    filename_only, creator, updator = get_git_log(filename)
    header_text = _get_header(filename_only, creator, updator,
                              project_name, organisation_name).splitlines(True)

    if filename_only[-3:] != '.py':
        return False

    with open(filename, mode='r') as f:
        filelines = f.readlines()

    insert_header = True
    last_line_num = 0
    if filelines:
        if filelines[0] != header_text[0] and filelines[0].startswith('#!'):
            header_text = header_text[1:]
            last_line_num = 1
        if (filelines[:len(header_text)] == header_text):
            return False
        if (header_text[0] == filelines[last_line_num]) and (header_text[-1] == filelines
                                                             [last_line_num + len(header_text) - 1]):
            insert_header = False
        elif (header_text[0] == filelines[last_line_num]):
            # check if last line exists at different line number
            insert_header = True
            num_instances = 0
            for i, line in enumerate(filelines):
                if (header_text[-1] == line):
                    if (num_instances == 2):
                        last_line_num = i + 1
                        break
                    else:
                        num_instances += 1

    with open(filename, mode='w') as file_processed:
        updated = False
        if insert_header:
            for line in header_text:
                file_processed.write(line)

        else:
            if last_line_num:
                file_processed.write(filelines[0])
            for i, line in enumerate(header_text):
                fileline = filelines[i + last_line_num]
                if line != fileline:
                    file_processed.write(line)
                    updated = True
                else:
                    file_processed.write(fileline)
            last_line_num += len(header_text)

        for i in range(last_line_num, len(filelines)):
            file_processed.write(filelines[i])

    return insert_header or updated


def get_git_log(filename: str):
    """Get the git log information."""

    g = git.Git()
    user_name = g.config('user.name')
    user_email = g.config('user.email')
    filename_only = os.path.basename(filename)

    log_histoy = g.log('--pretty=%cd;%an;%ae;%s;%H',
                       '--date=short', '--follow', '--', filename).split('\n')
    if (log_histoy[-1] != ''):
        cre = log_histoy[-1].split(';')
        creator = {'author': cre[1], 'date': cre[0],
                   'email': cre[2], 'hash': cre[4], 'comment': cre[3]}
    else:  # new file added - get current user
        creator = {'author': user_name, 'date': str(datetime.date.today()),
                   'email': user_email, 'hash': '', 'comment': ''}

    updator = {'author': user_name, 'date': str(
        datetime.date.today()), 'email': user_email, 'hash': '', 'comment': ''}

    return filename_only, creator, updator


def _get_header(filename_only: str = '', creator: dict = {}, updater: dict = {}, project_name: str = '', organisation_name: str = ''):

    def header_definition(filename_only, organisation_name, project_name,
                          created_by, last_update):
        header = """#!python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# PYTHONSCRIPT: {}
# ------------------------------------------------------------------------------
# Copyright:    {}
# Project:      {}
#
# Created by:   {}
# Last Update:  {}
# ------------------------------------------------------------------------------\n""".format(filename_only,
                                                                                             organisation_name,
                                                                                             project_name, created_by,
                                                                                             last_update)
        return header

    if len(creator.keys()):

        created_by = f'{creator["date"]} by {creator["author"]} <{creator["email"]}>'
        last_update = f'{updater["date"]} by {updater["author"]} <{updater["email"]}>'
        header = header_definition(
            filename_only, organisation_name, project_name, created_by, last_update)
    else:
        header = header_definition('', '', '', '', '')

    return header


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Input main function to update the header."""
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    parser.add_argument('--project',
                        type=str,
                        default='Test',
                        help='Name of the project in file header.')
    parser.add_argument('--organisation',
                        type=str,
                        default='Test Ltd.',
                        help='Name of the organisation in file header.')
    args = parser.parse_args(argv)

    return_code = 0

    for filename in args.filenames:
        if check_header(filename=os.path.abspath(filename),
                        organisation_name= args.organisation,
                        project_name=args.project):
            print(f'Updated header for {filename}')
            return_code = 1
    return return_code


if __name__ == '__main__':
    exit(main())

