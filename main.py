import discord
from discord.ext import commands
import config
from imgurpython import ImgurClient
import random
from time import sleep
import asyncio

imgur_id = "id"
imgur_secret = "secret"


def imgur_search(search=""):
    try:
        client2 = ImgurClient(imgur_id, imgur_secret)
    except ImgurClientError as e:
        if e.status_code == 403:
            return u'can i haz valid api keys?'
        else:
            return u'sorry i could not reach imgur :/  E_MSG: {0} E_CODE: {1}'.format(e.error_message, e.status_code)
    try:
        search_results = client2.gallery_search(search, advanced=None, sort='time', window='all', page=0)
    except ImgurClientError as e:
        return u'derp, something bad happened: {0}'.format(e.error_message)

    if len(search_results) > 0:
        item = random.choice(search_results)
        if item.is_album:
            try:
                search_results = client2.get_album_images(item.id)
                item = search_results[0]
            except ImgurClientError as e:
                return u'derp, something bad happened: {0}'.format(e.error_message)

        # gifs over 10mb get returned with an h appended to their id
        # shave it off to get the full animated gif
        if len(item.link) > 7 and item.link[-5] == 'h':
            gif_link = item.link[0:-5]+item.link[-4:]
            if DEBUG:
                print ("""[dankBot] [DEBUG] search="{0}" link="{1}" Large gif link found, modifying link.""").format(search, item.link)
        else:
            gif_link = item.link
    else:
        gif_link = None
        if DEBUG:
            print ("""[dankBot] [DEBUG] search="{0}" resource="{1}" No results found.""").format(search, "imgur")
    return gif_link




emoji = {"a": ":regional_indicator_a:","b": ":regional_indicator_b:","c": ":regional_indicator_c:","ç":":regional_indicator_c:","d":":regional_indicator_d:", "e":":regional_indicator_e:", "f":":regional_indicator_f:", "g":":regional_indicator_g:","ğ":":regional_indicator_g:","h":":regional_indicator_h:","ı":":regional_indicator_i:","i":":regional_indicator_i:","j":":regional_indicator_j:","k":":regional_indicator_k:","l":":regional_indicator_l:","m":":regional_indicator_m:","n":":regional_indicator_n:","o":":regional_indicator_o:","ö":":regional_indicator_o:","p":":regional_indicator_p:","r":":regional_indicator_r:","s":":regional_indicator_s:","ş":":regional_indicator_s:","t":":regional_indicator_t:","u":":regional_indicator_u:","ü":":regional_indicator_u:","v":":regional_indicator_v:","y":":regional_indicator_y:","z":":regional_indicator_z:","0":":zero:","1":":one:","2":":two:","3":":three:","4":":four:","5":":five:","6":":six:","7":":seven:","8":":eight:","9":":nine:"," ":" ","w":":regional_indicator_w:","x":":regional_indicator_x:","q":":regional_indicator_q:"}


prefix = "_"
client = commands.Bot(command_prefix = prefix)

def botmu(ctx):
    if ctx.author.bot == False:
        return True

@client.event
async def on_ready():
    print(
        f'\nŞu hesapla giriş yapıldı: {client.user.name}#{client.user.discriminator},',
        f'ID: {client.user.id}, Bot Version: {config.version}\n'
    )
    await client.change_presence(status=discord.Status.online, activity=discord.Game("_yardım | Sürüm {} | {} sunucuda hizmet veriyoruz!".format(config.version,len(client.guilds))))
    

    
@commands.check(botmu)
@client.command(aliases=["emojiyazı"])
async def emojiyaz(ctx, *, arg):
    arg = arg.lower()
    harfler = []
    for harf in arg:
        if harf in emoji:
            harfler.append(emoji[harf])
    harfler = ' '.join([str(elem) for elem in harfler]) 
    await ctx.send(harfler)

@commands.check(botmu)
@client.command()
async def üyesayısı(ctx):

    embed=discord.Embed(description="Bulunduğun sunucudaki üye sayısını gösterir.",color=0xffff00)
    embed.set_footer(text="Botlar dahil")
    embed.add_field(name="Üye Sayısı", value=ctx.guild.member_count, inline=False)
    await ctx.send(embed=embed)

@commands.check(botmu)
@client.command()
async def kedi(ctx):
    
    #await ctx.send(imgur_search(search="cat")
    kedi = imgur_search(search=random.choice(["kitten","cat"]))
    embed=discord.Embed(title="Rastgele Kedi Resmi", color=0x0000ff)
    embed.add_field(name="Miyav", value=kedi, inline=True)
    embed.set_footer(text="İmgur tarafından")
    embed.set_image(url=kedi)
    await ctx.send(embed=embed)

@commands.check(botmu)
@client.command()
async def kedi2(ctx):
    await ctx.send(imgur_search(search=random.choice(["kitten","cat"])))

@commands.check(botmu)
@client.command()
async def köpek(ctx):
    
    köpek = imgur_search(search="dog")
    embed=discord.Embed(title="Rastgele Köpek Resmi", color=0x0000ff)
    embed.add_field(name="Hav hav", value=köpek, inline=True)
    embed.set_footer(text="İmgur tarafından")
    embed.set_image(url=köpek)
    await ctx.send(embed=embed)

@commands.check(botmu)
@client.command()
async def köpek2(ctx):
    await ctx.send(imgur_search(search=random.choice(["dog","puppy"])))




@commands.check(botmu)
@client.command()
async def ping(ctx):
    embed=discord.Embed(title="Gecikme Hızı", description="", color=0xff0000)
    embed.add_field(name="Pong!", value=f"{round(client.latency, 1)} ms  :ping_pong:", inline=True)
    embed.set_footer(text="Anlık Gecikme Hızı")
    await ctx.send(embed=embed)


@commands.check(botmu)
@client.command()
async def yazdır(ctx, *, arg=""):
    if arg == "":
        await ctx.send("**Yazdıracağım Mesajı Girmelisin.**")
    else:
        embed=discord.Embed(color=0x04f2ff)
        embed.add_field(name=arg, value="Komutu isteyen: {}".format(ctx.author.name), inline=False)
        await ctx.send(embed=embed)

@commands.check(botmu)
@client.command()
async def gönder(ctx, *, argg=""):
    if argg == "":
        await ctx.send("**Yazdıracağım Mesajı Girmelisin.**")
    else:
        await ctx.send(argg)

@commands.check(botmu)
@client.command(aliases=["yazdırsil"])
async def göndersil(ctx, *, arggg=""):
    if arggg == "":
        await ctx.send("**Yazdıracağım Mesajı Girmelisin.**")
    else:
        await ctx.message.delete()
        await ctx.channel.send(arggg)




@commands.check(botmu)
@client.command()
async def imgurarama(ctx, *, aranacak):
    arama = imgur_search(search=aranacak)
    embed=discord.Embed(title="İmgur Araması", color=0x0000ff)
    embed.add_field(name="Arama Sonucu", value=arama, inline=True)
    embed.set_footer(text="İmgur tarafından")
    embed.set_image(url=arama)
    await ctx.send(embed=embed)

@commands.check(botmu)
@client.command()
async def seçimyap(ctx, *kuralar):
    embed=discord.Embed(color=0x00ff00)
    embed.add_field(name="Seçim Sonucu", value=random.choice(kuralar), inline=False)
    await ctx.send(embed=embed)

    
@commands.check(botmu)
@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def sil(ctx, limit=0):
        if limit == 0:
            await ctx.send("**Sileceğim Mesaj Miktarını Belirtmelisin!**")
        else:
            await ctx.channel.purge(limit=limit)
            embed=discord.Embed(color=0x800000)
            embed.add_field(name="{} Mesaj Silindi".format(limit), value="Gerçekleştiren {}".format(ctx.author.mention), inline=False)
            await ctx.send(embed=embed)
            await ctx.message.delete()

@sil.error
async def sil_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**Mesajları Yönetme Yetkiniz Yok.**")


@commands.check(botmu)
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member = "", *, reason=None):
    if member == "":
       await ctx.send("**Kimi Atacağımı Belirtmelisin.**")
    else:
        await member.kick(reason=reason)
        embed=discord.Embed(color=0xcb0af3)
        embed.add_field(name="{} Atıldı! Sebep: {}".format(member.mention,reason), value="{} tarfından".format(ctx.author.mention), inline=False)
        await ctx.send(embed=embed)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**Üyeleri Atma Yetkiniz Yok.**")


@commands.check(botmu)
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member = "", *, reason=None):
    if member == "":
        await ctx.send("**Kimi Banlayacağımı Belirtmelisin.**")
    else:
        await member.ban(reason=reason)
        embed=discord.Embed(color=0x4ef904)
        embed.add_field(name="{} Yasaklandı! Sebep: {}".format(member.mention,reason), value="{} tarfından".format(ctx.author.mention), inline=False)
        await ctx.send(embed=embed)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**Üyeleri Yasaklama Yetkiniz Yok.**")
        

@commands.check(botmu)
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member=""):
    if member == "":
        await ctx.send("**Kimin Yasağını Kaldıracağımı Belirtmelisin.**")
    else:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        
        for ban_entry in banned_users:
            user = ban_entry.user
            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed=discord.Embed(color=0xfb5302)
                embed.add_field(name="{} Adlı Üyenin Yasağı Kaldırıldı!".format(user), value="{} tarfından".format(ctx.author.mention), inline=False)
                await ctx.send(embed=embed)
                

@commands.check(botmu)
@client.command()          
async def yazıtura(ctx):
    embed=discord.Embed(color=0x1818e2)
    embed.add_field(name="Yazı Tura Sonucu", value=random.choice(["Yazı","Tura"]), inline=False)
    await ctx.send(embed=embed)
                




                
                
                
                          
                
  
client.run(config.token)
