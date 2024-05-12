import discord
from discord import option
from discord.ext import commands
from utils.database import Database
from utils.discord import generate_message_embed

class TotalHonor(commands.Cog):
    async def generate_honor_bar(self, total_honor):
        """Generate a bar with 5 points to represent honor, with zero in the middle."""
        # Calculate the distance from zero
        distance_from_zero = min(9, max(-9, total_honor // 50))

        # Initialize the bar string with emojis
        emojis = [
            "<:lowest:1237260385787052043>",
            "<:lower:1237260422030032938>",
            "<:low:1237260382603579392>",
            "<:middle:1237260381202677761>",
            "<:middle:1237260381202677761>",
            "<:midhigh:1237260380393312267>",
            "<:high:1237260378929365053>",
            "<:higher:1237260377994166384>",
            "<:highest:1237260376467312701>"
        ]

        # Calculate the index of the emoji to be replaced
        middle_point_index = min(8, max(0, 4 + distance_from_zero))

        # Replace the appropriate emoji with the Arthur emoji
        emojis[middle_point_index] = "<:arthur:1237260715429986386>"

        honor_bar = ' '.join(emojis)

        return honor_bar

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
        name="count_total",
        description="Get a user's total honor word count")
    @option(name="user", description="User to get count of", required=False)
    async def count_total(self, ctx, user: discord.Member = None):
        """Get a person's total honor"""
        await ctx.defer()
        user = user if user else ctx.author
        # Validate mention.
        invalid_mention_msg = self.verify_mentions(user, ctx)
        if invalid_mention_msg:
            await ctx.respond(invalid_mention_msg)
            return

        # Fetch total honor word count of user if they have a count.
        total_honor = await Database.total_honor(ctx.guild.id, user.id)
        honor_bar = await self.generate_honor_bar(total_honor)
        embed = await generate_message_embed(
            f"**{user.display_name}**'s total honor: {total_honor}\n\n{honor_bar}",
            type="info", ctx=ctx)
        await ctx.respond(embed=embed, ephemeral=True,)

def setup(bot):
    bot.add_cog(TotalHonor(bot))
