import sqlite3
import logging
import json

# Fetch SQLite database file path
db_file_path = "database.db"

# Initialize SQLite connection
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Create the guilds table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS guilds
                  (guild_id INTEGER PRIMARY KEY,
                  guild_name TEXT,
                  members TEXT,
                  settings TEXT)''')
conn.commit()


class Database:
    """SQLite database"""

    @classmethod
    async def create_database(cls, guild_id: int, guild_name: str) -> None:
        """Initialize guild template in database"""
        cursor.execute("""
            INSERT INTO guilds (guild_id, guild_name, members, settings) 
            VALUES (?, ?, ?, ?)
        """, (guild_id, guild_name, "[]", "[]"))
        conn.commit()  # Commit the transaction to save changes
        logging.info(f"Guild added! {guild_name} with id {guild_id}")

    @classmethod
    async def guild_in_database(cls, guild_id: int) -> bool:
        """Return True if guild is already recorded in database"""
        cursor.execute("SELECT COUNT(*) FROM guilds WHERE guild_id = ?", (guild_id,))
        count = cursor.fetchone()[0]
        return count > 0

    @classmethod
    async def update_guilds(cls):
        """Update all guilds in database to have a settings field if they don't already."""
        cursor.execute("UPDATE guilds SET settings = ? WHERE settings IS NULL", ("[]",))
        conn.commit()

    @classmethod
    async def get_internal_guild_settings(cls, guild_id: int) -> list:
        """Return guild settings as a list"""
        cursor.execute("SELECT settings FROM guilds WHERE guild_id = ?", (guild_id,))
        row = cursor.fetchone()
        settings = row[0] if row else "[]"
        return json.loads(settings)

    @classmethod
    async def update_guild_settings(cls, guild_id: int, settings: list) -> None:
        """Update guild settings"""
        cursor.execute("UPDATE guilds SET settings = ? WHERE guild_id = ?", (json.dumps(settings), guild_id))
        conn.commit()

    @classmethod
    async def get_guild_settings(cls, guild_id: int):
        new_settings = {}
        settings = await cls.get_internal_guild_settings(guild_id)
        for setting in settings:
            new_settings[setting["int_name"]] = setting
        return new_settings

    @classmethod
    async def member_in_database(cls, guild_id: int, member_id: int) -> object | None:
        """Return True if member is already recorded in guild database"""
        cursor.execute("SELECT members FROM guilds WHERE guild_id = ?", (guild_id,))
        row = cursor.fetchone()
        if row:
            members = json.loads(row[0])
            for member in members:
                if member["id"] == member_id:
                    return member
        return None

    @classmethod
    async def create_member(cls, guild_id, member_id, member_name) -> None:
        """Initialize member data in guild database"""
        cursor.execute("SELECT members FROM guilds WHERE guild_id = ?", (guild_id,))
        row = cursor.fetchone()
        if row:
            members = json.loads(row[0])
            members.append({"id": member_id, "name": member_name, "high_honor_word_count": 0, "low_honor_word_count": 0})
            cursor.execute("UPDATE guilds SET members = ? WHERE guild_id = ?", (json.dumps(members), guild_id))
            conn.commit()

    @classmethod
    async def increment_low_honor_word_count(cls, guild_id, member_id, count) -> None:
        """Add to low honor word count of person's data info in server"""
        cursor.execute("SELECT members FROM guilds WHERE guild_id = ?", (guild_id,))
        row = cursor.fetchone()
        if row:
            members = json.loads(row[0])
            for member in members:
                if member["id"] == member_id:
                    member["low_honor_word_count"] += count
                    cursor.execute("UPDATE guilds SET members = ? WHERE guild_id = ?", (json.dumps(members), guild_id))
                    conn.commit()
                    break

    @classmethod
    async def increment_high_honor_word_count(cls, guild_id, member_id, count) -> None:
        """Add to high honor word count of person's data info in server"""
        cursor.execute("SELECT members FROM guilds WHERE guild_id = ?", (guild_id,))
        row = cursor.fetchone()
        if row:
            members = json.loads(row[0])
            for member in members:
                if member["id"] == member_id:
                    # Check if 'high_honor_word_count' key exists
                    if "high_honor_word_count" in member:
                        member["high_honor_word_count"] += count
                    else:
                        # If not, initialize it with count
                        member["high_honor_word_count"] = count
                    cursor.execute("UPDATE guilds SET members = ? WHERE guild_id = ?", (json.dumps(members), guild_id))
                    conn.commit()
                    break

    @classmethod
    async def total_honor(cls, guild_id, member_id) -> int:
        """Calculate total honor (high honor + low honor word counts) for a member in a guild"""
        cursor.execute("SELECT members FROM guilds WHERE guild_id = ?", (guild_id,))
        row = cursor.fetchone()
        if row:
            members = json.loads(row[0])
            for member in members:
                if member["id"] == member_id:
                    high_honor_count = member.get("high_honor_word_count", 0)
                    low_honor_count = member.get("low_honor_word_count", 0)
                    # Return the sum of high honor count and negation of low honor count
                    return high_honor_count + (-low_honor_count)
        return 0
    @classmethod
    async def get_total_documents(cls) -> int:
        """Return total number of documents in database"""
        cursor.execute("SELECT COUNT(*) FROM guilds")
        return cursor.fetchone()[0]

    @classmethod
    async def get_high_honor_word_server_total(cls, guild_id) -> int:
        """Return integer sum of total low honor words said in a server"""
        cursor.execute("SELECT members FROM guilds WHERE guild_id = ?", (guild_id,))
        row = cursor.fetchone()
        if row:
            members = json.loads(row[0])
            total = sum(member.get("high_honor_word_count", 0) for member in members)
            return total
        return 0

    @classmethod
    async def get_low_honor_word_server_total(cls, guild_id) -> int:
        """Return integer sum of total low honor words said in a server"""
        cursor.execute("SELECT members FROM guilds WHERE guild_id = ?", (guild_id,))
        row = cursor.fetchone()
        if row:
            members = json.loads(row[0])
            total = sum(member.get("low_honor_word_count", 0) for member in members)
            return total
        return 0
