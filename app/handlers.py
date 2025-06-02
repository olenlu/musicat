from aiogram import Router
from yt_dlp import YoutubeDL
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile
import os
import tempfile
import asyncio

from app.utils import search_youtube_audio_by_name


router = Router()
user_search_results = {}

@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer('Привет! Введи название песни и исполнителя~')


@router.message(Command('help'))
async def cmd_help(message:Message):
    photo = FSInputFile("app/static/bot.png")
    await message.answer_photo(
        photo=photo,
        caption=(
            '📖 *Помощь по использованию бота*\n\n'
            '1. Введите название песни/подкаста/видео, которое хотите услышать в аудио формате.\n'
            '2. Бот пришлёт вам 5 результатов поиска.\n'
            '3. Нажмите на команду вида /1, /2 и т.д., чтобы выбрать нужный трек.\n'
            '4. Ожидайте — бот пришлёт аудиофайл 🎧'
        ),
        parse_mode='Markdown'
    )


@router.message(lambda m: m.text and m.text.startswith("/") and m.text[1:].isdigit())
async def download_song(message: Message, state: FSMContext):
    # user_id = message.from_user.id
    # results = user_search_results.get(user_id)
    results = (await state.get_data())["results"]
    if not results:
        await message.answer("Сначала введите название песни для поиска.")
        return
    try:
        num = int(message.text[-1]) - 1
        video = results[num]
    except (ValueError, IndexError):
        await message.answer("Неправильный номер.")
        return
    
    await message.answer(f"Скачиваю: {video['title']}...")

    url = f"https://www.youtube.com/watch?v={video['id']}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    def download_audio():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info).replace(info['ext'], 'mp3')


    audio_path = await asyncio.to_thread(download_audio)
    print(audio_path)
    audio_file = FSInputFile(audio_path)
    await message.answer_audio(audio=audio_file, title=video['title'])
    # os.remove(audio_path)





@router.message()
async def search_song(message: Message, state: FSMContext):
    await message.answer("Уже ищу!")
    title = message.text
    results = await search_youtube_audio_by_name(title)
    if not results: 
        await message.answer("К сожалению, не могу ничего найти по вашему запросу\nМожет поищем что-нибудь другое?")
    await state.update_data(results=results)
    # user_search_results[message.from_user.id] = results
    sms = ''
    for i, video in enumerate(results,1):
        sms+=f"/{i}. {video['title']}\n{video['url']}\n\n"
    await message.answer(sms, disable_web_page_preview=True)