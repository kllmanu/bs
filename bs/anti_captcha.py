from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless


class AntiCaptcha:

    def __init__(self, client_key, website_key):
        self.solver = recaptchaV2Proxyless()

        self.solver.set_key(client_key)
        self.solver.set_website_key(website_key)
        self.solver.set_is_invisible(1)
        self.solver.set_verbose(0)
        self.solver.set_soft_id(0)

    def solve(self, url) -> str:
        """Solve the captcha and return the response."""

        self.solver.set_website_url(url)

        ticket = self.solver.solve_and_return_solution()

        if not ticket:
            raise Exception(f"Failed to solve the captcha: {self.solver.error_code}")

        return ticket
