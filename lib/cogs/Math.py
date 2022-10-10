import operator
from sre_parse import DIGITS
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.context import Context

from lib.bot import Bot

class Math(Cog):
  def __init__(self, bot):
    self.bot: Bot = bot
    self.DIGITS = set('0123456789')
    self.OPERATIONS = {
      '+' : operator.add,
      '-' : operator.sub,
      '*' : operator.mul,
      '/' : operator.floordiv,
      '^' : operator.pow,
    }

  def __is_digit(self, var):
    return var in self.DIGITS

  def __get_number(self, varstr):
    s=""
    if varstr[0] == '-':
      s+="-"
      varstr=varstr[1:]
    for c in varstr:
      if not self.__is_digit(c):
        break
      s+=c
    return (int(s), len(s))

  def __perform_operation(self, string, num1, num2):
    op = self.OPERATIONS.get(string, None)
    if op is not None:
      return op(num1, num2)
    else:
      return None

  @command(name="calc", aliases=['calculate'])
  async def calc(self, ctx: Context, expr: str):
    n, end_n = self.__get_number(expr)
    expr = expr[end_n:]
    while expr:
      op, expr = expr[0], expr[1:]
      n2, end_n = self.__get_number(expr)
      n = self.__perform_operation(op, n, n2)
      expr = expr[end_n:]
    await ctx.send(n)

def setup(bot):
  bot.add_cog(Math(bot))