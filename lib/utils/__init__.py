import subprocess
import urllib.parse


class Utils:
    invis = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"

    @staticmethod
    def behind():
        cmd1 = ["git", "remote", "update"]
        cmd2 = ["git", "status", "-uno"]
        subprocess.run(cmd1)
        res = subprocess.run(cmd2, stdout=subprocess.PIPE)

        return "Your branch is behind" in res.stdout.decode('utf-8')

    def embed(self, author: str, title: str, description: str, color: str, redirect: str = "https://gccody.com", image_url: str = "https://i.imgur.com/n5mioQi.jpg"):
        query = f"author={urllib.parse.quote(author)}&title={urllib.parse.quote(title)}&imageurl={urllib.parse.quote(image_url)}&hexcolor={urllib.parse.quote(color)}&redirect={urllib.parse.quote(redirect)}&description={urllib.parse.quote(description)}"
        return f"{self.invis} https://auth.nighty.support/api/embed?{query}"

    def format_str(self, amount: int, string: str):
        if amount == 1:
            return string
        return string + 's'

    def humanize(self, time):
        times = []
        times_to_ms = {
            'Year': 3154e7,
            'Month': 2628e6,
            'Week': 604800,
            'Day': 86400,
            'Hour': 3600,
            'Minute': 60,
            'Second': 1
        }
        for i, mod in times_to_ms.items():
            amount, time = divmod(time, mod)
            if amount == 0: continue
            times.append(f'{int(amount)} {self.format_str(amount, i)}')

        return ' '.join(times) + ' ago'
