from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest

async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`Invalid channel/group`")
            return None
        except ChannelPrivateError:
            await event.reply(
                "`This is a private channel/group or I am banned from there`"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Channel or supergroup doesn't exist`")
            return None
        except (TypeError, ValueError):
            await event.reply("`Invalid channel/group`")
            return None
    return chat_info


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = " ".join(names)
    return full_name


@bot.on(admin_cmd(pattern="inviteall ?(.*)"))
@bot.on(sudo_cmd(pattern="inviteall ?(.*)", allow_sudo=True))
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        LEGEND = await edit_or_reply(event, "`processing...`")
    else:
        LEGEND = await edit_or_reply(event, "`processing...`")
    aura = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await LEGEND.edit("`Sorry, Cant add users here`")
    s = 0
    f = 0
    error = "None"

    await LEGEND.edit("**⚜️[Ͳєямιиαℓ Տτατυѕ](https://t.me/Tgxbotz_chat)**\n\n`🔸ιиνιτιиg Ⴎѕєяѕ.......`")
    async for user in event.client.iter_participants(aura.full_chat.id):
        try:
            if error.startswith("Too"):
                return await LEGEND.edit(
                    f"[τєямιиαℓ ƒιиιѕнє∂ ωιτн єяяοя](https;//t.me/Tgxbotz_chat)\n`🔸 мαγ gοτ ℓιмιτє∂ ƒяοм τєℓєτнοи ρℓєαѕє τяγ αgαιи ℓατєя`\n🔸 єяяοя : \n`{error}`\n\n🔸 ιиνιτє∂ `{s}` ρєορℓє \n ⚠️ƒαιℓє∂ το ιиνιτє `{f}` ρєορℓє"
                )
            await event.client(
                functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s = s + 1
            await LEGEND.edit(
                f"[τєямιиαℓ яυииιиg](https://t.me/Tgxbotz_chat)\n\n🔸 ιиνιτє∂ `{s}` ρєορℓє \n⚠️ ƒαιℓє∂ το ιиνιτє `{f}` ρєορℓє \n\n** ℓαѕτ єяяοя** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f = f + 1
    return await LEGEND.edit(
        f"[τєямנиαℓ ƒιиιѕнє∂](https://t.me/Tgxbotz_chat) \n\n🔸 Sυϲϲєѕѕƒυℓℓγ ιиνιτє∂ `{s}` ρєορℓє \n⚠️ ƒαιℓє∂ το ιиνιτє `{f}` ρєορℓє"
    )


@bot.on(admin_cmd(pattern="add ?(.*)"))
@bot.on(sudo_cmd(pattern="add ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await edit_or_reply(event, "`.add` users to a chat, not to a Private Message")
    else:
        logger.info(to_add_users)
        if not event.is_channel and event.is_group:
            # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
            for user_id in to_add_users.split(" "):
                try:
                    await borg(
                        functions.messages.AddChatUserRequest(
                            chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                        )
                    )
                except Exception as e:
                    await event.reply(str(e))
            await edit_or_reply(event, "Invited Successfully")
        else:
            # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
            for user_id in to_add_users.split(" "):
                try:
                    await borg(
                        functions.channels.InviteToChannelRequest(
                            channel=event.chat_id, users=[user_id]
                        )
                    )
                except Exception as e:
                    await event.reply(str(e))
            await edit_or_reply(event, "Added user to the chat....")


CmdHelp("invite").add_command(
  "add", "<username/id>", "Adds the given user to the group"
).add_command(
  "inviteall", "<group username>", "Scraps user from the targeted group to your group. Basically Kidnapps user from one chat to another"
).add()
