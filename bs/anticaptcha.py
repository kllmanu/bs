from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless

import os

ANTICAPTCHA_KEY = os.getenv("ANTICAPTCHA_KEY")
WEBSITE_KEY = "6Ldd07ogAAAAACktG1QNsMTcUWuwcwtkneCnPDOL"

solver = recaptchaV2Proxyless()
solver.set_key(ANTICAPTCHA_KEY)
solver.set_website_key(WEBSITE_KEY)
solver.set_is_invisible(1)
solver.set_verbose(0)
solver.set_soft_id(0)


def decaptcha(host: str):
    solver.set_website_url(host)

    g_response = solver.solve_and_return_solution()

    if g_response != 0:
        return g_response

    else:
        print("task finished with error " + solver.error_code)
