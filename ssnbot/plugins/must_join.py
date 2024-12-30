from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.exceptions import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

API_TOKEN = 'your-bot-api-token'
MUST_JOIN = 'your-channel-id-or-username'  # Set the required channel ID or username

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'], state=None)
async def must_join_channel(msg: types.Message):
    if not MUST_JOIN:  # Not compulsory
        return
    try:
        try:
            # Check if the user is a member of the MUST_JOIN channel
            member = await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
            if member.status == 'left':  # User is not a member
                raise UserNotParticipant
        except UserNotParticipant:
            # If not a member, generate the join link
            if MUST_JOIN.isalpha():
                link = f"https://t.me/{MUST_JOIN}"
            else:
                chat_info = await bot.get_chat(MUST_JOIN)
                link = chat_info.invite_link

            # Send a message with the join link
            try:
                await msg.reply(
                    f"To use my services, please join [this channel]({link}) first. After that, you can try again 🧑‍💻",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton("❤️‍🩹 Join Channel ❤️‍🩹", url=link)]
                        ]
                    )
                )
                return  # Stop further processing
            except ChatWriteForbidden:
                pass  # If the bot can't send a message in the chat

    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat: {MUST_JOIN}!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
