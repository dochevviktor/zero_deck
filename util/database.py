from typing import List

from StreamDeck.Devices.StreamDeck import StreamDeck
from peewee import *
import util.image as img
from command.command_type import CommandType

db = SqliteDatabase('./db/config.db')


class BaseModel(Model):
    class Meta:
        database = db


class Page(BaseModel):
    id = AutoField()
    number = IntegerField(null=False, unique=True, default=0)


class Font(BaseModel):
    id = AutoField()
    font = BlobField(null=False)


class ImageLabel(BaseModel):
    id = AutoField()
    image = BlobField(null=False)
    label = TextField()
    pressed_image = BlobField(null=True)
    pressed_label = TextField(null=True)
    label_position = IntegerField(null=False, default=1)
    rotation = IntegerField(null=False, default=0)
    font: Font = ForeignKeyField(Font, field=id, null=False)


class Command(BaseModel):
    id = AutoField()
    type = IntegerField(null=False, default=0)
    command = TextField(null=False, default="")
    parent = ForeignKeyField('self', backref='children', null=True)


class Key(BaseModel):
    id = AutoField()
    position = IntegerField(null=False)
    image_label: ImageLabel = ForeignKeyField(ImageLabel, field=id, null=False)
    command: Command = ForeignKeyField(Command, field=id, null=False)
    page: Page = ForeignKeyField(Page, backref='keys', null=False)


def initialize_default_font() -> Font:
    print("Initialize default font...")
    font = Font()
    font.font = img.load_default_font_to_base64("Roboto-Regular.ttf")
    font.save()
    print("Initialize default font...Done!")
    return font


def initialize_home_page(deck: StreamDeck, font: Font):
    print("Initialize home page...")
    home_page = Page()
    home_page.number = 0
    home_page.save()
    keys = deck.key_count()
    for key in range(keys):
        if key == keys - 4:
            continue
        command = Command()
        if key == keys - 1:
            new_image = create_image(font, key, "Settings.png", "settings")
            command.type = CommandType.PAGE.value
            command.command = "-1"
        else:
            new_image = create_image(font, key, "Released.png", "Key {}", "Pressed.png", "Pressed!")
        command.save()
        new_key = Key(position=key, image_label=new_image, command=command, page=home_page)
        new_key.save()
    print("Initialize home page...Done!")


def initialize_settings_page(deck: StreamDeck, font: Font):
    print("Initialize settings page...")
    settings_page = Page()
    settings_page.number = -1
    settings_page.save()
    keys = deck.key_count()
    for key in range(keys):
        if key == keys - 4:
            continue
        command: Command
        if key == keys - 1:
            new_image = create_image(font, key, "Back.png", "back")
            command = Command()
            command.type = CommandType.PAGE.value
            command.command = "0"
        elif key == 0:
            new_image = create_image(font, key, "Exit.png", "exit")
            command = Command()
            command.type = CommandType.SYSTEM.value
            command.command = "exit"
        elif key == 1:
            new_image = create_image(font, key, "BrightUp.png", "bup")
            command = Command()
            command.type = CommandType.SYSTEM.value
            command.command = "brightness_up"
        elif key == 2:
            new_image = create_image(font, key, "BrightDown.png", "bdn")
            command = Command()
            command.type = CommandType.SYSTEM.value
            command.command = "brightness_down"
        else:
            continue
        command.save()
        new_key = Key(position=key, image_label=new_image, command=command, page=settings_page)
        new_key.save()
    print("Initialize settings page...Done!")


def create_image(font, key, released_png, released_label, pressed_png=None, pressed_label=None):
    image_released = img.load_image_to_base64(released_png)
    if pressed_png is not None:
        image_pressed = img.load_image_to_base64(pressed_png)
    else:
        image_pressed = image_released
    label_released = released_label.format(key)
    if pressed_label is not None:
        label_pressed = pressed_label
    else:
        label_pressed = label_released
    new_image = ImageLabel(image=image_released,
                           label=label_released,
                           pressed_image=image_pressed,
                           pressed_label=label_pressed,
                           label_position=key,
                           font=font)
    new_image.save()
    return new_image


def load_keys_for_page(page: Page) -> List[Key]:
    keys: list[Key] = (Key.select(ImageLabel, Command, Page, Key)
                       .join_from(Key, ImageLabel)
                       .join_from(Key, Command)
                       .join_from(Key, Page)
                       .where(Key.page.number == page.number))
    return keys


def load_pages():
    return Page.select()


def load_all():
    pages: list[Page] = Page.select()
    keys: list[Key] = (Key.select(ImageLabel, Command, Page, Key, Font)
                       .join_from(Key, ImageLabel)
                       .join_from(Key, Command)
                       .join_from(Key, Page)
                       .join_from(ImageLabel, Font))
    pages_with_keys = prefetch(pages, keys)
    return pages_with_keys


def load(deck: StreamDeck):
    try:
        db.connect()
        db.create_tables([Font, Page, ImageLabel, Command, Key], safe=True)
        if Key.select().count() == 0:
            print("Initialize DB from empty state...")
            font = initialize_default_font()
            initialize_home_page(deck, font)
            initialize_settings_page(deck, font)
            print("Initialize DB from empty state...Done!")
        else:
            print("Load data")
        return load_all()
    except Exception as e:
        print("Error while loading from database", e)
        pass


def close():
    db.close()
