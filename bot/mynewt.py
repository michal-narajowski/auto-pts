#!/usr/bin/env python

#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2018, Intel Corporation.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#

import logging
import os
import subprocess
import sys
import time

import autoptsclient_common as autoptsclient
import ptsprojects.mynewt as autoprojects
import ptsprojects.stack as stack
from pybtp import btp
from ptsprojects.mynewt.iutctl import get_iut

import bot.common


def check_call(cmd, env=None, cwd=None, shell=True):
    """Run command with arguments.  Wait for command to complete.
    :param cmd: command to run
    :param env: environment variables for the new process
    :param cwd: sets current directory before execution
    :param shell: if true, the command will be executed through the shell
    :return: returncode
    """
    cmd = subprocess.list2cmdline(cmd)

    return subprocess.check_call(cmd, env=env, cwd=cwd, shell=shell)


def get_tty_path(name):
    """Returns tty path (eg. /dev/ttyUSB0) of serial device with specified name
    :param name: device name
    :return: tty path if device found, otherwise None
    """
    serial_devices = {}
    ls = subprocess.Popen(["ls", "-l", "/dev/serial/by-id"],
                          stdout=subprocess.PIPE)

    awk = subprocess.Popen("awk '{if (NF > 5) print $(NF-2), $NF}'",
                           stdin=ls.stdout,
                           stdout=subprocess.PIPE,
                           shell=True)

    end_of_pipe = awk.stdout
    for line in end_of_pipe:
        device, serial = line.decode().rstrip().split(" ")
        serial_devices[device] = serial

    for device, serial in serial_devices.items():
        if name in device:
            tty = os.path.basename(serial)
            return "/dev/{}".format(tty)

    return None


def build_and_flash(project_path, board, overlay=None):
    """Build and flash Mynewt binary
    :param project_path: Mynewt source path
    :param board: IUT
    :param overlay: configuration map to be used
    :return: TTY path
    """
    logging.debug("{}: {} {} {}".format(build_and_flash.__name__, project_path,
                                        board, overlay))

    check_call('rm -rf bin/'.split(), cwd=project_path)
    check_call('rm -rf targets/{}_boot/'.format(board).split(),
               cwd=project_path)
    check_call('rm -rf targets/bttester/'.split(), cwd=project_path)

    check_call('newt target create {}_boot'.format(board).split(),
               cwd=project_path)
    check_call('newt target create bttester'.split(), cwd=project_path)

    check_call(
        'newt target set {}_boot bsp=@apache-mynewt-core/hw/bsp/{}'.format(
            board, board).split(), cwd=project_path)
    check_call(
        'newt target set {}_boot app=@apache-mynewt-core/apps/boot'.format(
            board).split(), cwd=project_path)

    check_call(
        'newt target set bttester bsp=@apache-mynewt-core/hw/bsp/{}'.format(
            board).split(), cwd=project_path)
    check_call(
        'newt target set bttester app=@apache-mynewt-nimble/apps/bttester'.split(),
        cwd=project_path)

    if overlay is not None:
        config = ':'.join(['{}={}'.format(k, v) for k, v in overlay.items()])
        check_call('newt target set bttester syscfg={}'.format(config).split(),
                   cwd=project_path)

    check_call('newt build {}_boot'.format(board).split(), cwd=project_path)
    check_call('newt build bttester'.split(), cwd=project_path)

    check_call('newt create-image {}_boot 0.0.0'.format(board).split(),
               cwd=project_path)
    check_call('newt create-image bttester 0.0.0'.split(), cwd=project_path)

    check_call('newt load {}_boot'.format(board).split(), cwd=project_path)
    check_call('newt load bttester'.split(), cwd=project_path)

    return get_tty_path("J-Link")


def get_target_description(project_path):
    return subprocess.check_output('newt target show bttester', shell=True,
                                   cwd=project_path)


def get_target_config(project_path):
    return subprocess.check_output('newt target config flat bttester',
                                   shell=True, cwd=project_path)


def get_newt_info(project_path):
    return subprocess.check_output('newt info',
                                   shell=True, cwd=project_path)


def get_newt_version(project_path):
    return subprocess.check_output('newt version',
                                   shell=True, cwd=project_path)


def get_build_info_file(project_path):
    file_name = "build_info.txt"
    build_info_str = ''

    build_info_str += 'newt info:\n'
    build_info_str += get_newt_info(project_path)
    build_info_str += '\n'

    build_info_str += 'newt version:\n'
    build_info_str += get_newt_version(project_path)
    build_info_str += '\n'

    build_info_str += 'newt target show:\n'
    build_info_str += get_target_description(project_path)
    build_info_str += '\n'

    build_info_str += 'newt target config:\n'
    build_info_str += get_target_config(project_path)
    build_info_str += '\n'

    with open(file_name, "w") as text_file:
        text_file.write(build_info_str)

    return file_name


def get_test_cases(ptses):
    """Get all test cases
    :param pts: PTS proxy instance
    :return: ZTestCase list
    """
    test_cases = autoprojects.gap.test_cases(ptses[0])
    test_cases += autoprojects.gatt.test_cases(ptses[0])
    test_cases += autoprojects.sm.test_cases(ptses[0])
    test_cases += autoprojects.l2cap.test_cases(ptses[0])
    mesh_test_cases, additional_mesh_test_cases = \
        autoprojects.mesh.test_cases(ptses)
    test_cases += mesh_test_cases
    additional_test_cases = additional_mesh_test_cases

    return test_cases, additional_test_cases


def run_tests(args, iut_config):
    """Run test cases
    :param args: AutoPTS arguments
    :param iut_config: IUT configuration
    :return: tuple of (status, results) dictionaries
    """
    results = {}
    status = {}
    descriptions = {}
    total_regressions = []

    callback_thread = autoptsclient.init_core()

    ptses = []
    for ip, local in zip(args['server_ip'], args['local_ip']):
        ptses.append(autoptsclient.init_pts(ip,
                                            args["workspace"],
                                            args["bd_addr"],
                                            args["enable_max_logs"],
                                            callback_thread,
                                            "mynewt_" + str(args["board"]),
                                            local))

    btp.init(get_iut)
    # Main instance of PTS
    pts = ptses[0]

    # Read PTS Version and keep it for later use
    args['pts_ver'] = "%x" % pts.get_version()

    stack.init_stack()
    stack_inst = stack.get_stack()
    stack_inst.synch_init(callback_thread.set_pending_response,
                          callback_thread.clear_pending_responses)
    cache = autoptsclient.cache_workspace(pts)

    default_to_omit = []

    for config, value in iut_config.items():
        if 'overlay' not in value:
            continue
        for test_case in value.get('test_cases', []):
            default_to_omit.append(test_case)

    for config, value in iut_config.items():
        overlay = None

        if 'overlay' in value:
            # TODO:
            overlay = value['overlay']
            to_run = value['test_cases']
            to_omit = None
        else:
            to_run = value['test_cases']
            to_omit = default_to_omit

        tty = build_and_flash(args["project_path"], args["board"],
                              overlay)
        logging.debug("TTY path: %s" % tty)

        time.sleep(10)

        autoprojects.iutctl.init(args["kernel_image"], tty, args["board"])

        # Setup project PIXITS
        autoprojects.gap.set_pixits(ptses[0])
        autoprojects.gatt.set_pixits(ptses[0])
        autoprojects.sm.set_pixits(ptses[0])
        autoprojects.l2cap.set_pixits(ptses[0])
        autoprojects.mesh.set_pixits(ptses)

        test_cases, additional_test_cases = get_test_cases(ptses)
        if to_run or to_omit:
            test_cases = autoptsclient.get_test_cases_subset(test_cases,
                                                             to_run, to_omit)

        status_count, results_dict, regressions = autoptsclient.run_test_cases(
            ptses, test_cases, additional_test_cases, int(args["retry"]))
        total_regressions += regressions

        for k, v in status_count.items():
            if k in status.keys():
                status[k] += v
            else:
                status[k] = v

        results.update(results_dict)
        autoprojects.iutctl.cleanup()

    for test_case_name in results.keys():
        descriptions[test_case_name] = \
            autoptsclient.get_test_case_description(cache, test_case_name)

    autoptsclient.cache_cleanup(cache)

    pts.unregister_xmlrpc_ptscallback()

    return status, results, descriptions, total_regressions


def compose_mail(args, mynewt_hash_html, summary_html,
                 reg_html, log_url_html, name):
    """ Create a email body
    """

    body = '''
    <p>This is automated email and do not reply.</p>
    <h1>Bluetooth test session</h1>
    <h2>1. IUT Setup</h2>
    <b> Board:</b> {} <br>
    <b> Source:</b> {} </p>
    <h2>2. PTS Setup</h2>
    <p><b> OS:</b> Windows 10 <br>
    <b> Platform:</b> VirtualBox <br>
    <b> Version:</b> {} </p>
    <h2>3. Test Results</h2>
    {}
    {}
    <h3>Logs</h3>
    {}
    <p>Sincerely,</p>
    <p> {}</p>
    '''.format(args["board"], mynewt_hash_html, args['pts_ver'],
               summary_html, reg_html, log_url_html, name)

    subject = "[Mynewt Nimble] AutoPTS test session results"

    return subject, body


def main(cfg):
    print("Mynewt bot start!")

    args = cfg['auto_pts']
    args['kernel_image'] = None

    repos_status = bot.common.update_repos(args['project_path'], cfg["git"])

    mynewt_hash_status = 'mynewt-core={}, mynewt-nimble={}'.format(
        repos_status['apache-mynewt-core'],
        repos_status['apache-mynewt-nimble'])

    summary, results, descriptions, regressions = \
        run_tests(args, cfg.get('iut_config', {}))

    report_file = bot.common.make_report_xlsx(results, summary, regressions,
                                              descriptions)
    logs_file = bot.common.archive_recursive("logs")

    build_info_file = get_build_info_file(os.path.abspath(args['project_path']))

    if 'gdrive' in cfg:
        drive = bot.common.Drive(cfg['gdrive'])
        url = drive.new_workdir(args['board'])
        drive.upload(report_file)
        drive.upload(logs_file)
        drive.upload(build_info_file)
        drive.upload("TestCase.db")

    if 'mail' in cfg:
        print("Sending email ...")

        # Summary
        summary_html = bot.common.status_dict2summary_html(summary)

        # Provide test case description
        _regressions = []
        for name in regressions:
            _regressions.append(
                name + " - " + descriptions.get(name, "no description"))

        reg_html = bot.common.regressions2html(_regressions)

        # Log in Google drive in HTML format
        if 'gdrive' in cfg:
            log_url_html = bot.common.url2html(url, "Results on Google Drive")
        else:
            log_url_html = "Not Available"

        subject, body = compose_mail(args, mynewt_hash_status, summary_html,
                                     reg_html, log_url_html,
                                     cfg['mail']['name'])

        bot.common.send_mail(cfg['mail'], subject, body)

        print("Done")

    bot.common.cleanup()

    print("\nBye!")
    sys.stdout.flush()
    return 0
