from discord.user import User, Profile


class ScrapedUser():
    def __init__(self, user: User) -> None:
        self.mutual_guilds = None
        self.flags = None
        self.mutual_friends = None
        self.note = None
        self.discord_team_user = None
        self.discord_staff = None
        self.discord_partner = None
        self.early_supporter = None
        self.bug_hunter = None
        self.hypesquad_house = None
        self.nitro = None
        self.connected_accounts = None
        self.banner_url = None
        self.bio = None
        self.__profile: Profile | None = None
        self.__user = user
        self.id = self.__user.id
        self.display_name = self.__user.display_name
        self.discriminator = self.__user.discriminator
        self.avatar_url = f"https://cdn.discordapp.com{self.__user.avatar_url_as(format=('gif' if self.__user.is_avatar_animated() else 'png'))._url}"
        self.created_at_str = self.__user.created_at.strftime(f"%m/%d/%Y, %I:%M:%S %p")
        self.created_at_timestamp = self.__user.created_at.timestamp()

    async def init(self):
        self.__profile = await self.__user.profile()
        self.bio = self.__profile.bio
        self.banner_url = f"https://cdn.discordapp.com{self.__profile.banner_url}" if self.__profile.banner_url else None
        self.connected_accounts = self.__profile.connected_accounts
        self.nitro = self.__profile.nitro
        self.hypesquad_house = self.__profile.hypesquad_house if self.__profile.hypesquad else None
        self.bug_hunter = self.__profile.bug_hunter if self.__profile.bug_hunter else None
        self.early_supporter = self.__profile.early_supporter if self.__profile.early_supporter else None
        self.discord_partner = self.__profile.partner if self.__profile.partner else None
        self.discord_staff = self.__profile.staff if self.__profile.staff else None
        self.discord_team_user = self.__profile.team_user if self.__profile.team_user else None
        self.note = self.__profile.note
        self.mutual_guilds: list[MutualGuilds] = [MutualGuilds(guild.id, guild.name) for guild in self.__profile.mutual_guilds]
        self.mutual_friends: self.__profile.mutual_friends
        self.flags = self.__profile.flags

    def to_json_str(self) -> dict[str, any]:
        return {
            "Id": self.id,
            "Display Name": self.display_name,
            "Discriminator": self.discriminator,
            "Avatar Url": self.avatar_url,
            "Created At Str": self.created_at_str,
            "Created At Timestamp": self.created_at_timestamp,
            "Bio": self.bio,
            "Banner Url": self.banner_url if self.banner_url else "",
            "Connected Accounts": self.connected_accounts,
            "Nitro": self.nitro,
            "Hypesquad House": self.hypesquad_house if self.hypesquad_house else "",
            "Bug Hunter": self.bug_hunter if self.bug_hunter else "",
            "Early Supporter": self.early_supporter if self.early_supporter else "",
            "Discord Partner": self.discord_partner if self.discord_partner else "",
            "Discord Staff": self.discord_staff if self.discord_staff else "",
            "Discord Team User": self.discord_team_user if self.discord_team_user else "",
            "Note": self.note,
            "Mutual Guilds": [guild.to_json_str() for guild in self.mutual_guilds],
            "Mutual Friends": self.mutual_friends,
            "Flags": self.flags
        }


class MutualGuilds:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def to_json_str(self) -> dict[str, any]:
        return {
            "Id": self.id,
            "Name": self.name
        }
