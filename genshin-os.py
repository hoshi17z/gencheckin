import os
import sys
import random
import time


sys.dont_write_bytecode = True

from settings import log, CONFIG
from sign import Sign
#from notify import Notify


if __name__ == '__main__':
    rand = 2
    log.info(f"Sleeping for {rand}s")
    time.sleep(rand)
    log.info(f'Genshin Impact Check-In Helper v{CONFIG.GIH_VERSION}')
    log.info('If you fail to check in, please try to update!')

    #notify = Notify()
    msg_list = []
    ret = success_num = fail_num = 0
    """
    HoYoLAB Community's COOKIE
    :param OS_COOKIE: HoYoLAB cookie(s) for one or more accounts.
        Separate cookies for multiple accounts with the hash symbol #
        e.g. cookie1text#cookie2text
        Do not surround cookies with quotes "" if using Github Secrets.
    """
    # Github Actions -> Settings -> Secrets
    # Ensure that the Name is exactly: OS_COOKIE
    # Value should look like: login_ticket=xxx; account_id=696969; cookie_token=xxxxx; ltoken=xxxx; ltuid=696969; mi18nLang=en-us; _MHYUUID=xxx
    #         Separate cookies for multiple accounts with the hash symbol #
    #         e.g. cookie1text#cookie2text
    OS_COOKIE = ''
    token = ''

    if os.environ.get('OS_COOKIE', '') != '':
        OS_COOKIE = os.environ.get('OS_COOKIE')
    else:
        log.error("Cookie not set properly, please read the documentation on how to set and format your cookie in Github Secrets.")
        raise Exception("Cookie failure")

    cookie_list = OS_COOKIE.split('#')
    log.info(f'Number of account cookies read: {len(cookie_list)}')
    for i in range(len(cookie_list)):
        log.info(f'Preparing NO.{i + 1} Account Check-In...')
        try:
            #ltoken = cookie_list[i].split('ltoken=')[1].split(';')[0]
            token = cookie_list[i].split('cookie_token=')[1].split(';')[0]
            msg = f'	NO.{i + 1} Account:{Sign(cookie_list[i]).run()}'
            msg_list.append(msg)
            success_num = success_num + 1
        except Exception as e:
            if not token:
                log.error("Cookie token not found, please try to relog on the check-in page.")

            msg = f'	NO.{i + 1} Account:\n    {e}'
            msg_list.append(msg)
            fail_num = fail_num + 1
            log.error(msg)
            ret = -1
        continue
    #notify.send(status=f'\n  -Number of successful sign-ins: {success_num} \n  -Number of failed sign-ins: {fail_num}', msg=msg_list)
    push_msg = ""
    for i in msg_list:
        push_msg = push_msg + i
    if ret != 0:
        log.error('program terminated with errors')
        exit(ret)
    log.info('exit success')
    exit(0)