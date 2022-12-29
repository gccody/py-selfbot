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
