import random
import string

import discord
from discord import option
from discord.ext import commands
from utils.database import Database
from utils.discord import generate_message_embed

HIGHWORDS_LIST = [
    "Bunkie", "Bunk", "Bunkatron", "Taco Shop",
    "Beef Nacho Supreme", "Pasta", "Good Bot",
    "Hays Aircraft LLC", "Hess Services",
    "Playstation", "Lucia", "Jason", "ProfZ",
    "Zeller", "Jon", "Steve"
]

class HighHonorWordCounter(commands.Cog):
    """Commands for word count tracking"""

    def __init__(self, bot):
        self.bot = bot

        self.db = Database()

        self.high_honor_words = HIGHWORDS_LIST

    def count_words(self, msg: str) -> int:
        """Return occurrences of high honor words in a given message"""
        count = 0
        msg = msg.lower().strip().translate(
            {ord(char): "" for char in string.whitespace})
        for low in self.high_honor_words:
            count += msg.count(low)
        # Return count if count is positive, else return 0
        return count if count >= 0 else 0

    async def get_member_word_count(self, guild_id, member_id) -> int:
        """Return number of high honor words said by member if tracked in database"""
        member = await self.db.member_in_database(guild_id, member_id)
        if not member:
            return 0
        return member["high_honor_word_count"]

    def get_msg_response(self, word_count: int) -> str:
        """Return bot message response"""
        msg = None
        if word_count < 5:
            msg = "<:HighHonor:1199342542592933959>"
        elif word_count < 25:
            msg = "<:HighHonor:1199342542592933959><:HighHonor:1199342542592933959>"
        elif word_count < 100:
            msg = "<:HighHonor:1199342542592933959><:HighHonor:1199342542592933959><:HighHonor:1199342542592933959>"
        else:
            msg = "..."

        return msg

    @commands.Cog.listener()
    async def on_message(self, message):
        """Detect high honor words"""
        if message.author == self.bot.user:  # Ignore reading itself.
            return
        if message.author.bot:  # Ignore spammy bots.
            return

        guild = message.guild
        msg = message.content
        author = message.author  # Should fetch user by ID instead of name.

        # Ensure guild has its own place in the database.
        if not await self.db.guild_in_database(guild.id):
            await self.db.create_database(guild.id, guild.name)

        # Bot reaction to any high honor word occurrence.
        num_words = self.count_words(msg)

        # No high honor words found.
        if num_words <= 0:
            return

        if message.webhook_id:  # Ignore webhooks.
            return

        if not await self.db.member_in_database(guild.id, author.id):
            await self.db.create_member(guild.id, author.id, author.name)

        await self.db.increment_high_honor_word_count(guild.id, author.id, num_words)

        response = self.get_msg_response(word_count=num_words)

        await message.reply(f"{response}")

    def verify_mentions(self, mentions: discord.Member,
                        ctx: discord.ApplicationContext) -> str:
        """Check if mention being passed into command is valid. This is no longer needed as discord does this for us.
        With slash commands.

        This code checks if the user is in the guild, and if not, returns an error message.
        """

        # Ensure user is part of guild.
        guild = ctx.guild
        if not guild.get_member(mentions.id):
            return "User not in server"
        else:
            return ""

    @commands.slash_command(
        name="count_high",
        description="Get a person's total high honor word count")
    @option(name="user", description="User to get count of", required=False)
    async def count(self, ctx, user: discord.Member = None):
        """Get a person's total high honor word count"""
        await ctx.defer()
        user = user if user else ctx.author
        # Validate mention.
        invalid_mention_msg = self.verify_mentions(user, ctx)
        if invalid_mention_msg:
            await ctx.respond(invalid_mention_msg)
            return

        # Fetch high honor word count of user if they have a count.
        word_count = await self.get_member_word_count(ctx.guild.id, user.id)
        await ctx.respond(embed=await generate_message_embed(
            f"**{user.display_name}** has said high honor words **{word_count:,}** time{'' if word_count == 1 else 's'}",
            type="info", ctx=ctx), ephemeral=True)

def setup(bot):
    bot.add_cog(HighHonorWordCounter(bot))