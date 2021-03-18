#-*- coding:utf-8 -*-
import discord, asyncio, json, datetime, os, logging, logging.handlers

from discord.ext import tasks, commands

from dotenv import load_dotenv

from os import system

from dateutil import tz

intents = discord.Intents.default()

intents.members = True
intents.presences = True

client=commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')
client.load_extension('jishaku')

system('title '+'!BLACKBOT')

##LOG##
#logger 인스턴스 생성 및 로그 레벨 설정#
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#formatter 생성#
streamformatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
fileformatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)s] %(levelname)s: %(message)s')
#Handler 생성#
streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler(r'C:\Users\bestc\OneDrive\바탕 화면\PythonWorkspace\bots\DS\black.log', encoding='utf-8')
#Handler에 formatter 설정#
streamHandler.setFormatter(streamformatter)
fileHandler.setFormatter(fileformatter)
#Handler을 logging에 추가#
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

MAKER=[402075873790001153]
USER=[703248821299183697, 763246275902308352]
BLACK=[]
msgstatus = False

@commands.cooldown(1, 60, type=commands.BucketType.guild)
@client.command()
async def helpme(ctx):
    await help(ctx)

async def help(ctx):
    global msgstatus
    if ctx.author.id in MAKER:
        if msgstatus == False:
            await ctx.send('관리자는 도움말을 지원하지 않습니다. 개발자에게 문의하세요.')
        else:
            await ctx.channel.send('관리자는 도움말을 지원하지 않습니다. 개발자에게 문의하세요.')
    elif ctx.author.id in USER:
        logger.debug(f'{ctx.guild.name}(ID: {ctx.guild.id})에서 {ctx.author}(ID: {ctx.author.id})가 이용자용 헬프커맨드 작동')
        embed = discord.Embed(title='BLACKBOT- 사용자 도움말', description="""
        <필독: !guide 명령어를 통해 명령어 가이드를 꼭 확인해주세요!>
        **!helpme**: 현재 보고계신 이 도움말을 전송해줍니다.
        **!black <멘션/유저ID> [사유] [증거들]**: 제공해주신 파라미터들을 토대로 블랙리스트에 유저를 등재시킵니다.
        **!edit <멘션/유저ID> <사유/증거> <내용>**: 제공해주신 파라미터들을 토대로 블랙리스트에 등재된 유저의 항목을 수정합니다.
        **!inquire <멘션/유저ID> [항목]**: 해당 유저의 블랙리스트 기본 정보를 조회하거나, 항목 추가 시 항목에 따른 유저의 항목을 조회합니다. (항목 목록은 가이드 참조)
        **!autoexecute <ban/kick> [메시지 삭제 일수]**: 제공해주신 파라미터들을 토대로 자동으로 서버 전체 유저를 블랙리스트와 대조 및 해당 유저를 추방/차단합니다.
        **!blacklist user**: 전체 유저 블랙리스트를 전송해줍니다.
        **!reportuser <멘션/유저ID>** [사유] [증거들]: 제공해주신 파라미터들을 토대로 개발자에게 해당 유저를 신고합니다. 개발자는 신고내역을 검토 후 블랙리스트에 등재시킬 수 있습니다.
        **!botsuggest <내용>**: 내용을 봇 개발자에게 전송해줍니다.
        """)
        embed.set_author(name='<> = 필수 항목, [] = 선택 항목')
        if msgstatus == False:
            await ctx.send(embed=embed)
        else:
            await ctx.channel.send(embed=embed)
            msgstatus = False
    else:
        logger.debug(f'{ctx.guild.name}(ID: {ctx.guild.id})에서 {ctx.author}(ID: {ctx.author.id})가 일반인 헬프커맨드 작동')
        embed = discord.Embed(title='BLACKBOT- 일반인 도움말', description="""
        **!helpme** : 현재 보고계신 이 도움말을 전송해줍니다.
        **!inquire <멘션/유저ID> [항목]**: 해당 유저의 블랙리스트 기본 정보를 조회하거나, 항목 추가 시 항목에 따른 유저의 항목을 조회합니다. (항목 목록은 가이드 참조)
        **!reportuser <멘션/유저ID> [사유] [증거들]**: 제공해주신 파라미터들을 토대로 개발자에게 해당 유저를 신고합니다. 개발자는 신고내역을 검토 후 블랙리스트에 등재시킬 수 있습니다.
        **!botsuggest <내용>**: 내용을 봇 개발자에게 전송해줍니다.
        """)
        embed.set_author(name='<> = 필수 항목, [] = 선택 항목')
        if msgstatus == False:
            await ctx.send(embed=embed)
        else:
            await ctx.channel.send(embed=embed)
            msgstatus = False

@commands.cooldown(1, 120, type=commands.BucketType.user)
@client.command()
async def guide(ctx):
    if ctx.author.id in MAKER:
        await ctx.send('관리자는 가이드를 지원하지 않습니다. 개발자에게 문의하세요.')
    elif ctx.author.id in USER:
        logger.debug(f'{ctx.guild.name}(ID: {ctx.guild.id})에서 {ctx.author}(ID: {ctx.author.id})가 이용자용 가이드커맨드 작동')
        embed=discord.Embed(title='BLACKBOT- 사용자 가이드', description="""
        *<모든 명령어에는 악용 방지를 위해 쿨타임이 있을 수 있습니다.>*
        **<주의! 모든 명령어는 자체 로깅시스템에 의해 사용이 기록되며, 일부 로그는 일반인도 조회가 가능합니다.>**
        __**<경고! 본 봇으로 서버 채팅 도배를 시도하거나 욕설을 등재시키는 등 부적절한 행위를 할 시 영구/임시 블랙리스트 조치가 이뤄질 수 있습니다.>**__
        **!helpme**: !helpme 명령어가 기억이 나지 않으신다면 이 봇을 멘션하는 방법(유저당 6분에 1번으로 제한됨)으로 도움말을 전송받으실 수 있습니다.
        **!black**: 사유와 증거는 `||.||`로 구분하여야 하며, 사유나 증거는 1024자를 넘겨서는 안됩니다. 블랙리스트는 삭제가 개발자 전용으로 제한되어 있으니, 등재를 신중히 해주세요.
        **!edit**: 사유 혹은 증거만 수정이 가능하며, 수정잠금이 활성화됐을 경우 수정이 차단됩니다.
        **!inquire**: [항목 목록]-사유, 증거, 닉태그, 수정횟수, 수정시각, 수정유저, 수정내용, 수정잠금, 등재시각, 등재유저, 등재내용, 수정로그, 등재로그
        **!autoexecute**: 명령어 실행인과 본 봇에 추방&차단권한이 없다면 실행이 차단됩니다.
        **!blacklist**: 만약 블랙리스트가 2048자가 넘는다면 txt파일이 대신 전송됩니다. 절대 악성파일이 아니니 안심하세요.
        **!reportuser**: 유저를 개발자에게 신고하는 명령어입니다. 사유와 증거는 `||.||`로 구분하여야 하며, 사유나 증거는 1024자를 넘겨서는 안됩니다.
        **!botsuggest**: 블랙리스트 수정/삭제요청 시 본 명령어를 사용해주시면 되며, 건의사항은 2048자 이내로 써주셔야 하고, 수정/삭제요청 시 수정요청 시 대상 유저ID 18자, 사유 1000자 이내, 증거 1000자 이내, 구분용 띄어쓰기 3자, 수정사유 27자 이내를 지켜주시기 바랍니다.
        """)
        await ctx.author.send(embed=embed)
        await ctx.send(ctx.author.mention + ', 당신의 DM으로 BLACKBOT 가이드가 전송되었습니다!')
    else:
        logger.debug(f'{ctx.guild.name}(ID: {ctx.guild.id})에서 {ctx.author}(ID: {ctx.author.id})가 일반인 가이드커맨드 작동')
        embed=discord.Embed(title='BLACKBOT- 일반인 도움말', description="""
        *<모든 명령어에는 악용 방지를 위해 쿨타임이 있을 수 있습니다.>*
        **<주의! 모든 명령어는 자체 로깅시스템에 의해 사용이 기록되며, 일부 로그는 일반인도 조회가 가능합니다.>**
        __**<경고! 본 봇으로 서버 채팅 도배를 시도하거나 욕설을 등재시키는 등 부적절한 행위를 할 시 영구/임시 블랙리스트 조치가 이뤄질 수 있습니다.>**__
        **!helpme**: !helpme 명령어가 기억이 나지 않으신다면 이 봇을 멘션하는 방법(유저당 6분에 1번으로 제한됨)으로 도움말을 전송받으실 수 있습니다.
        **!inquire**: [항목 목록]-사유, 증거, 닉태그, 수정횟수, 수정시각, 수정유저, 수정내용, 수정잠금, 등재시각, 등재유저, 등재내용, 수정로그, 등재로그
        **!reportuser**: 유저를 개발자에게 신고하는 명령어입니다. 사유와 증거는 `||.||`로 구분하여야 하며, 사유나 증거는 1024자를 넘겨서는 안됩니다.
        **!botsuggest**: 블랙리스트 수정/삭제요청 시 본 명령어를 사용해주시면 되며, 건의사항은 2048자 이내로 써주셔야 하고, 수정/삭제요청 시 수정요청 시 대상 유저ID 18자, 사유 1000자 이내, 증거 1000자 이내, 구분용 띄어쓰기 3자, 수정사유 27자 이내를 지켜주시기 바랍니다.
        """)
        await ctx.author.send(embed=embed)
        await ctx.send(ctx.author.mention + ', 당신의 DM으로 BLACKBOT 가이드가 전송되었습니다!')

@commands.cooldown(1, 5, type=commands.BucketType.user)
@client.command()
async def black(ctx, userid, *, additions:str=''):
    if ctx.author.id not in MAKER and ctx.author.id not in USER:
        return
    if ctx.author.id in BLACK:
        return
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    listadditions = additions.split('||.||')
    if len(listadditions) >= 3:
        await ctx.send('부가요소를 다시 확인하십시오.')
        return
    if listadditions[0] == '':
        reason = '(사유가 등재되지 않음)'
    else:
        reason = listadditions[0]
    if len(listadditions) < 2:
        evidence = '(증거가 등재되지 않음)'
    else:
        evidence = listadditions[1]
    if len(reason) > 1024 or len(evidence) > 1024:
        await ctx.send(f'사유나 증거는 1024자를 넘겨서는 안됩니다.\n등재 사유 글자수: {len(reason)}, 등재 증거 글자수: {len(evidence)}')
        return
    with open('black-user.json', 'r', encoding='utf-8') as readfile:
        blacklist = json.load(readfile)
    global status
    startmsg = await ctx.send(ctx.author.mention + ', 당신에 의한 유저(' + userid + ') 블랙리스트 등재가 진행중입니다. 잠시만 기다려주세요.')
    status = 'BLACKING'
    if userid not in blacklist:
        blacklist[userid] = {}
        to = await client.fetch_user(int(userid))
        blacklist[userid]['nicktag'] = str(to)
        blacklist[userid]['reason'] = reason
        blacklist[userid]['evidence'] = evidence
        KST = tz.gettz('Asia/Seoul')
        time = str(datetime.datetime.now(tz=KST))
        time = list(time)[:19]
        time = ''.join(time)
        blacklist[userid]['uploadtime'] = time
        blacklist[userid]['uploaduser'] = str(ctx.author.id)
        if ctx.author.id in MAKER:
            blacklist[userid]['uploaduser'] = '관리자'
        blacklist[userid]['uploaddetail'] = additions
        blacklist[userid]['editedtime'] = '(아직 수정되지 않음)'
        blacklist[userid]['editeduser'] = '(아직 수정되지 않음)'
        blacklist[userid]['editeddetail'] = '(아직 수정되지 않음)'
        blacklist[userid]['edited'] = 0
        blacklist[userid]['locked'] = 0
        if ctx.author.id in MAKER:
            blacklist[userid]['locked'] = 1
        with open('black-user.json', 'w', encoding='utf-8') as outfile:
            json.dump(blacklist, outfile, indent=4, ensure_ascii=False)
        logger.info(f'{ctx.author}(ID: {ctx.author.id})에 의해 {to}(ID: {userid})유저가 성공적으로 블랙리스트에 등재됨.\n세부사항: {additions}')
        embed = discord.Embed(description=f'{to}({to.id}) 유저가\n**성공적으로 블랙리스트에 등재**되었습니다.', color=0x0000ff)
        try:
            await startmsg.delete()
        except:
            pass
        if reason != '(사유가 등재되지 않음)':
            embed.add_field(name='사유', value=reason)
        if evidence != '(증거가 등재되지 않음)':
            embed.add_field(name='증거', value=evidence)
        await requiredby(ctx, embed)
        await ctx.send(embed=embed)
        status = None
    else:
        to = await client.fetch_user(int(userid))
        embed = discord.Embed(description=f'{to}({to.id}) 유저는\n**이미 블랙리스트에 등재**되어 있습니다.', color=0xff0000)
        await requiredby(ctx, embed)
        await ctx.send(embed=embed)
        try:
            await startmsg.delete()
        except:
            pass
        status = None

@commands.cooldown(2, 60, type=commands.BucketType.user)
@client.command()
async def edit(ctx, userid, type, *, detail):
    if ctx.author.id not in MAKER and ctx.author.id not in USER:
        return
    if ctx.author.id in BLACK:
        return
    if detail == '(삭제됨)' or detail == '(사유가 등재되지 않음)' or detail == '(증거가 등재되지 않음)':
        await ctx.send('잘못된 접근을 감지했습니다. 다시 시도해주세요.')
    if type == '사유':
        type = 'reason'
    elif type == '증거':
        type = 'evidence'
    if type != 'reason' and type != 'evidence':
        await ctx.send('허용되지 않았거나 존재하지 않는 항목의 수정요청을 감지했습니다. 다시 시도해주세요.')
        return
    if len(detail) > 1024:
        await ctx.send(f'사유나 증거는 1024자를 넘겨서는 안됩니다.\n글자수: {len(detail)}')
        return
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    global status
    status = 'BLACKING'
    _from = await client.fetch_user(int(userid))
    with open('black-user.json', 'r', encoding='utf-8') as readfile:
        blacklist = json.load(readfile)
    if userid not in blacklist:
        await ctx.send(f'{_from}(ID: {userid}) 유저는 블랙리스트에 등재되지 않았습니다! 다시 시도해주세요.')
        status = None
        return
    if blacklist[userid]['locked'] == 1:
        if ctx.author.id not in MAKER:
            await ctx.send(f'{_from}(ID: {userid}) 유저의 세부사항은 관리자 이외 수정이 금지되어 있습니다. 자세한 내용은 관리자에게 문의바랍니다.')
            status=None
            return
    blacklist[userid][type] = detail
    blacklist[userid]['edited'] += 1
    KST = tz.gettz('Asia/Seoul')
    time = str(datetime.datetime.now(tz=KST))
    time = list(time)[:19]
    time = ''.join(time)
    blacklist[userid]['editedtime'] = time
    blacklist[userid]['editeduser'] = str(ctx.author.id)
    if ctx.author.id in MAKER:
        blacklist[userid]['editeduser'] = '관리자'
    blacklist[userid]['editeddetail'] = type + '-' + detail
    with open('black-user.json', 'w', encoding='utf-8') as outfile:
        json.dump(blacklist, outfile, indent=4, ensure_ascii=False)
    logger.info(f'{ctx.author}(ID: {ctx.author.id})에 의해 {_from}(ID: {userid})유저가 성공적으로 블랙리스트에서 수정됨.\n세부사항: {type}-{detail}')
    embed = discord.Embed(description=f'{_from}(ID: {userid}) 유저(블랙리스트)의 항목이 다음 항목으로 성공적으로 변경되었습니다.')
    embed.add_field(name=type, value=detail)
    await ctx.send(embed=embed)
    status = None

@commands.is_owner()
@client.command()
async def override(ctx, userid, type, *, detail):
    with open('black-user.json', 'r', encoding='utf-8') as readfile:
        blacklist = json.load(readfile)
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    if userid not in blacklist:
        await ctx.send(ctx.author.mention + ', 유저아이디 확인하십시오.')
        return
    if type not in blacklist[userid]:
        await ctx.send(ctx.author.mention + ', 세부항목 확인하십시오.')
        return
    to = await client.fetch_user(int(userid))
    if detail.startswith('int'):
        try:
            detail = int(detail.lstrip('int'))
        except:
            pass
    embed=discord.Embed(description=f'{ctx.author.mention}, 다음 항목(혹은 내용)이 오버라이드될 예정입니다.\n오버라이드 이후에는 (관리자 이외 수정 금지 해제요청 이외에는)관리자 이외의 수정이 자동으로 금지됩니다.\n메시지 Y로 수락을, N으로 거절을 해주세요.\n대상 유저: {to}(ID: {userid})\n오버라이드 내용: {type}-{detail}')
    await ctx.send(embed=embed)
    def check(m):
        return ((m.content == 'Y') or (m.content == 'N')) and (m.channel == ctx.channel)
    msg = await client.wait_for('message', check=check)
    if msg.content == 'Y':
        if type == 'locked' or type == 'edited':
            try:
                detail=int(detail)
            except:
                await ctx.send('처리 중 오류가 발생했습니다. 세부내용을 확인해주세요.')
            blacklist[userid][type] = detail
            addition = ''
            if type == 'edited':
                blacklist[userid]['locked'] = 1
                addition = '관리자 이외의 수정이 금지되었습니다.'
            await ctx.send(f'{ctx.author.mention}, 오버라이드 요청이 수락되었으며 {to}(ID: {userid}) 유저의 {type}세부사항이 {detail}로 변경되었습니다. {addition}')
        else:
            blacklist[userid][type] = detail
            blacklist[userid]['locked'] = 1
            await ctx.send(f'{ctx.author.mention}, 오버라이드 요청이 수락되었으며 {to}(ID: {userid}) 유저의 {type}세부사항이 {detail}로 변경되었고, 관리자 이외의 수정이 금지되었습니다.')
        with open('black-user.json', 'w', encoding='utf-8') as outfile:
            json.dump(blacklist, outfile, indent=4, ensure_ascii=False)
    elif msg.content == 'N':
        await ctx.send(ctx.author.mention + ', 오버라이드 요청이 거절되었습니다.')

@commands.is_owner()
@client.command()
async def delete(ctx, userid, type:str=None):
    with open('black-user.json', 'r', encoding='utf-8') as readfile:
        blacklist = json.load(readfile)
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    if userid not in blacklist:
        await ctx.send(ctx.author.mention + ', 유저아이디 확인하십시오.')
        return
    if (type not in blacklist[userid]) and (type != None):
        await ctx.send(ctx.author.mention + ', 세부항목 확인하십시오.')
        return
    if type != None:
        question=blacklist[userid][type]
    to = await client.fetch_user(int(userid))
    if type == None:
        embed=discord.Embed(description=f'{ctx.author.mention}, 다음 항목(혹은 내용)이 삭제될 예정입니다.\n메시지 Y로 수락을, N으로 거절을 해주세요.\n대상 유저: {to}(ID: {userid})\n삭제 대상: 유저({userid})')
    else:
        embed=discord.Embed(description=f'{ctx.author.mention}, 다음 항목(혹은 내용)이 삭제될 예정입니다.\n메시지 Y로 수락을, N으로 거절을 해주세요.\n대상 유저: {to}(ID: {userid})\n삭제 대상: 세부항목({type}-{question})')
    await ctx.send(embed=embed)
    def check(m):
        return ((m.content == 'Y') or (m.content == 'N')) and (m.channel == ctx.channel)
    msg = await client.wait_for('message', check=check)
    if msg.content == 'Y':
        if type == None:
            del blacklist[userid]
            await ctx.send(f'{ctx.author.mention}, 삭제 요청이 수락되었으며 {to}(ID: {userid}) 유저가 블랙리스트에서 삭제되었습니다.')
        else:
            blacklist[userid][type] = '(삭제됨)'
            blacklist[userid]['locked'] = 1
            await ctx.send(f'{ctx.author.mention}, 삭제 요청이 수락되었으며 {to}(ID: {userid}) 유저의 {type}세부사항이 삭제되었고, 관리자 이외의 수정이 금지되었습니다.')
        with open('black-user.json', 'w', encoding='utf-8') as outfile:
            json.dump(blacklist, outfile, indent=4, ensure_ascii=False)
    elif msg.content == 'N':
        await ctx.send(ctx.author.mention + ', 삭제 요청이 거절되었습니다.')

@commands.cooldown(3, 5, type=commands.BucketType.user)
@client.command()
async def inquire(ctx, userid, type:str=None):
    if ctx.author.id in BLACK:
        return
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    global status
    status = 'BLACKING' ; _from = await client.fetch_user(int(userid))
    with open('black-user.json', 'r', encoding='utf-8') as readfile:
        blacklist = json.load(readfile)
    if userid not in blacklist:
        embed = discord.Embed(description=f'{_from}(ID: {userid}) 유저는 **블랙리스트에 등재되지 않**았습니다!', color=0xff0000)
        await requiredby(ctx, embed)
        await ctx.send(embed=embed)
        status = None
        return
    if type == '사유':
        type = 'reason'
    elif type == '증거':
        type = 'evidence'
    elif type == '닉태그':
        type = 'nicktag'
    elif type == '수정횟수':
        type = 'edited'
    elif type == '수정시각':
        type = 'editedtime'
    elif type == '수정유저':
        type = 'editeduser'
    elif type == '수정내용':
        type = 'editeddetail'
    elif type == '등재시각':
        type = 'uploadtime'
    elif type == '등재유저':
        type = 'uploaduser'
    elif type == '등재내용':
        type = 'uploaddetail'
    elif type == '수정잠금':
        type = 'locked'
    elif type == '수정로그':
        type = 'editlogs'
    elif type == '등재로그':
        type = 'uplogs'
    elif type == None:
        pass
    else:
        try:
            temp = blacklist[userid][type]
        except KeyError:
            await ctx.send('존재하지 않는 항목의 조회 요청이 감지되었습니다. 다시 시도해주세요.')
            return
    if type==None:
        nicktag = blacklist[userid]['nicktag']
        reason = blacklist[userid]['reason']
        evidence = blacklist[userid]['evidence']
        embed = discord.Embed(title=f'{_from}(ID: {userid}) 유저 블랙리스트 조회 결과입니다.', description=f'**블랙리스트 등재됨**', color=0x00ff00)
        embed.add_field(name='등재 당시 닉태그', value=nicktag)
        embed.add_field(name='등재 사유', value=reason)
        embed.add_field(name='등재 증거', value=evidence)
        await requiredby(ctx, embed)
        await ctx.send(embed=embed)
        status = None
    elif type == 'editlogs':
        editedtime = blacklist[userid]['editedtime']
        editeduser = blacklist[userid]['editeduser']
        editeddetail = blacklist[userid]['editeddetail']
        edited = blacklist[userid]['edited']
        embed = discord.Embed(title=f'{_from}(ID: {userid})\n유저 블랙리스트 세부사항__(수정로그)__ 조회 결과입니다.', description=f'**블랙리스트 등재됨**', color=0x00ff00)
        embed.add_field(name='총 수정된 횟수', value=edited, inline=False)
        embed.add_field(name='최근 수정 시각', value=editedtime)
        embed.add_field(name='최근 수정 유저', value=editeduser)
        embed.add_field(name='최근 수정 내용', value=editeddetail)
        if blacklist[userid]['locked'] == 1:
            yesorno = '관리자 이외 수정이 잠금됨'
        else:
            yesorno = '잠금되어 있지 않음'
        embed.add_field(name='세부사항 수정 잠금 여부', value=yesorno, inline=False)
        await requiredby(ctx, embed)
        await ctx.send(embed=embed)
        status = None
    elif type == 'uplogs':
        uploadtime = blacklist[userid]['uploadtime']
        uploaduser = blacklist[userid]['uploaduser']
        uploaddetail = blacklist[userid]['uploaddetail']
        embed = discord.Embed(title=f'{_from}(ID: {userid})\n유저 블랙리스트 세부사항__(등재로그)__ 조회 결과입니다.', description=f'**블랙리스트 등재됨**', color=0x00ff00)
        embed.add_field(name='등재 시각', value=uploadtime)
        embed.add_field(name='등재 유저', value=uploaduser)
        if uploaddetail != '':
            embed.add_field(name='등재 내용', value=uploaddetail)
        else:
            embed.add_field(name='등재 내용(인증됨)', value='(사유 및 증거가 등재되지 않음)')
        await requiredby(ctx, embed)
        await ctx.send(embed=embed)
        status = None
    else:
        answer = blacklist[userid][type]
        embed = discord.Embed(title=f'{_from}(ID: {userid}) 유저 블랙리스트 세부사항 조회 결과입니다.', description=f'**블랙리스트 등재됨**', color=0x00ff00)
        embed.add_field(name=type, value=answer)
        await requiredby(ctx, embed)
        await ctx.send(embed=embed)
        status = None
        logger.debug(f'{ctx.author}(ID: {ctx.author.id})에 의해 ({userid}유저가 성공적으로 블랙리스트에서 조회되었습니다.\n세부사항: {type}')

@commands.guild_only()
@commands.has_guild_permissions(ban_members=True, kick_members=True)
@commands.bot_has_permissions(ban_members=True, kick_members=True)
@commands.cooldown(1, 4, type=commands.BucketType.user)
@client.command()
async def autoexecute(ctx, type:str='ban', msgdelday:int=0):
    if ctx.author.id not in MAKER and ctx.author.id not in USER:
        return
    if ctx.author.id in BLACK:
        return
    if type != 'ban' and type != 'kick':
        await ctx.send('종류는 ban/kick 중에 하나만 선택해주세요!')
        return
    if msgdelday < 0 or msgdelday > 7:
        await ctx.send('메시지 삭제 일수는 최대 7일까지만 가능합니다. 다시 시도해주세요.')
        return
    with open('black-user.json', 'r', encoding='utf-8') as readfile:
        blacklist = json.load(readfile)
    errcount = 0
    succount = 0
    totcount = 0
    servmem = len(ctx.guild.members)
    for member in ctx.guild.members:
        if str(member.id) in blacklist:
            totcount += 1
            if type == 'ban':
                try:
                    await member.ban(reason=f'BLACKLIST-EXECUTED by {ctx.author}(ID: {ctx.author.id})', delete_message_days=msgdelday)
                    succount += 1
                except:
                    errcount += 1
            elif type == 'kick':
                try:
                    await member.kick(reason=f'BLACKLIST-EXECUTED by {ctx.author}(ID: {ctx.author.id})')
                    succount += 1
                except:
                    errcount += 1
    logger.debug(f'{ctx.author}(ID: {ctx.author.id})에 의해 {ctx.guild.name}(ID: {ctx.guild.id})에서 자동처형이 실행되었습니다.\n세부사항: {type}')
    await ctx.send(f'**{servmem}명의 서버 유저** 중 **{totcount}명**의 서버 내 유저가 **블랙리스트에 등재**되었으며, __**{succount}명**의 유저가 **성공적**으로 추방/차단되었고 **{errcount}명**의 유저가 **오류**로 인해 추방/차단되지 않았습니다.__ **남은 서버 유저는 {len(ctx.guild.members)}명입니다.**')

async def requiredby(ctx, embed):
    if ctx.message.author.avatar != None:
        avatar_type='.png'
        if ctx.message.author.avatar.startswith('a_'):
            avatar_type='.gif'
        icon_url=f'https://cdn.discordapp.com/avatars/{ctx.message.author.id}/{ctx.message.author.avatar}{avatar_type}'
    else:
        discriminator=int(ctx.message.author.discriminator) % 5
        icon_url=f'https://cdn.discordapp.com/embed/avatars/{discriminator}.png'
    embed.set_footer(text=f'{ctx.author}(ID: {ctx.author.id})가 요청함', icon_url=icon_url)

@commands.cooldown(1, 15, type=commands.BucketType.guild)
@client.command()
async def blacklist(ctx, type:str=None):
    if ctx.author.id not in MAKER and ctx.author.id not in USER:
        return
    if ctx.author.id in BLACK:
        return
    if type == 'user':
        black=[]
        with open('black-user.json', 'r', encoding='utf-8') as readfile:
            blacklist = json.load(readfile)
        if len(blacklist) <= 1:
            await ctx.send('현재 등재된 유저 블랙리스트가 없습니다!')
            return
        for blackuser in blacklist:
            blackuser = await client.fetch_user(int(blackuser))
            black.append(f'{blackuser}(ID: {blackuser.id})')
        blacks=str(len(black))
        KST = tz.gettz('Asia/Seoul')
        time = str(datetime.datetime.now(tz=KST))
        time = list(time)[:19]
        time = ''.join(time)
        black='\n'.join(black)
        black=f'**총 {blacks}명의 유저가 등재되었습니다.**\n{black}'
        if len(black) > 2048:
            with open('temp.txt', 'w', encoding='utf-8') as f:
                f.write(f'유저 블랙리스트-{time}\n\n{black}')
            await ctx.send('블랙리스트가 2048자가 넘어 한번에 표시할 수 없어 txt파일 전송으로 대체합니다.', file=discord.File("temp.txt", filename="blacklist_user"))
            logger.info(f'{ctx.author}(ID: {ctx.author.id})에 의해 {type} 전체 블랙리스트가 조회됨.')
            os.remove('temp.txt')
            return
        try:
            embed = discord.Embed(title=f'유저 블랙리스트-{time}', description=black, color=0x00ffff)
            await requiredby(ctx, embed)
            await ctx.send(embed=embed)
        except:
            pass
    elif type == 'guild':
        await ctx.send('아직 서버블랙 기능은 지원 예정에 없습니다.')
    else:
        await ctx.send('user/guild 중 하나의 종류를 선택해주세요!')

@commands.cooldown(2, 300, type=commands.BucketType.user)
@client.command()
async def reportuser(ctx, userid, *, additions:str=''):
    if ctx.author.id in BLACK:
        return
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    listadditions = additions.split('||.||')
    if len(listadditions) >= 3:
        await ctx.send('부가요소를 다시 확인하십시오.')
        return
    if listadditions[0] == '':
        reason = '(사유가 추가되지 않음)'
    else:
        reason = listadditions[0]
    if len(listadditions) < 2:
        evidence = '(증거가 추가되지 않음)'
    else:
        evidence = listadditions[1]
    if len(reason) > 1024 or len(evidence) > 1024:
        await ctx.send(f'{ctx.author.mention}, 사유나 증거는 1024자를 넘겨서는 안됩니다.\n신고 사유 글자수: {len(reason)}, 신고 증거 글자수: {len(evidence)}')
        return
    with open('black-user.json', 'r', encoding='utf-8') as readfile:
        blacklist = json.load(readfile)
    if userid in blacklist:
        await ctx.send('이미 등재되어 있는 유저입니다. 수정요청은 !botsuggest 명령어를 사용해주세요.')
        return
    global status
    status = 'BLACKING'
    ds = await client.fetch_user(402075873790001153)
    reporting = await client.fetch_user(int(userid))
    embed = discord.Embed(title='BLACKBOT- 신고', description=f'신고인: {ctx.author}(ID: {ctx.author.id})\n피신고인: {reporting}(ID: {userid})', color=0xff0000)
    embed.add_field(name='신고 사유', value=reason)
    embed.add_field(name='신고 증거', value=evidence)
    await ds.send(embed=embed)
    logger.debug(f'{ctx.author}(ID: {ctx.author.id})에 의해 {reporting}(ID: {userid})유저가 성공적으로 개발자에게 신고됨.\n세부사항: {additions}')
    embed = discord.Embed(description=f'{reporting}({userid}) 유저가\n**성공적으로 개발자에게 신고**되었습니다.', color=0x0000ff)
    if reason != '(사유가 등재되지 않음)':
        embed.add_field(name='사유', value=reason)
    if evidence != '(증거가 등재되지 않음)':
        embed.add_field(name='증거', value=evidence)
    await requiredby(ctx, embed)
    await ctx.send(embed=embed)
    status = None

@commands.cooldown(1, 180, type=commands.BucketType.user)
@client.command()
async def botsuggest(ctx, *, detail):
    if ctx.author.id in BLACK:
        return
    if len(detail) > 2048:
        await ctx.send(ctx.author.mention + ', 건의사항은 2048자 이내로 작성해 주셔야 합니다.\n(수정요청 시 대상 유저ID 18자, 사유 1000자 이내, 증거 1000자 이내, 구분용 띄어쓰기 3자, 수정사유 27자 이내)')
    ds = await client.fetch_user(402075873790001153)
    embed = discord.Embed(title='BLACKBOT- 건의', description=detail, color=0x00ff00)
    await requiredby(ctx, embed)
    await ds.send(embed=embed)
    logger.debug(f'{ctx.author}(ID: {ctx.author.id})에 의해 개발자에게 건의사항이 전달됨.\n세부사항: {detail}')

@commands.is_owner()
@client.command()
async def debug(ctx):
    guilds = []
    num = 0
    for guild in client.guilds:
        guilds.append(f'{num}: {guild.name}(ID: {guild.id})- {guild.owner}(ID: {guild.owner_id})')
        num += 1
    guilds = '\n'.join(guilds)
    if len(guilds) > 2048:
        with open('temp.txt', 'w', encoding='utf-8') as f:
            f.write(guilds)
        await ctx.send('디버그가 2048자가 넘어 한번에 표시할 수 없어 txt파일 전송으로 대체합니다.', file=discord.File("temp.txt", filename="debug_blackbot"))
        return
    embed = discord.Embed(title='BLACKBOT- DEBUG', description=guilds, color=0x00ffff)
    await ctx.send(embed=embed)

@commands.is_owner()
@client.command()
async def leave(ctx, gid:int=None):
    await ctx.message.delete()
    if gid == None:
        await ctx.guild.leave()
        return
    guild = client.guilds[gid]
    if len(str(gid)) == 18:
        guild = await client.fetch_guild(gid)
    await guild.leave()
    await ctx.author.send(f'{guild}(ID: {guild.id}) 퇴장 성공.')

@commands.is_owner()
@client.command()
async def taskoff(ctx):
    changing_presence.stop()
    await ctx.send('SUCCESSFULLY STOPPED THE ACTIVITY LOOP')

@commands.is_owner()
@client.command()
async def taskon(ctx):
    changing_presence.start()
    await ctx.send('SUCCESSFULLY STARTED THE ACTIVITY LOOP')

@commands.is_owner()
@client.command()
async def gamemode(ctx, *, msg):
    if (msg != None) and (str(msg) != '%clear'):
        await client.change_presence(activity=discord.Game(name=str(msg)))
    elif str(msg) == '%clear':
        await client.change_presence(activity=discord.Game(name=''))
    else:
        await client.change_presence(activity=discord.Game(name=' '))
    embed=discord.Embed(title=':o: 성공적으로 처리되었습니다.', description=f'봇이 "{msg} 하는 중"으로 상태가 변경되었습니다.')
    await ctx.author.send(embed=embed)

@commands.is_owner()
@client.command()
async def op(ctx, userid):
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    global status
    status = 'BLACKING'
    to = await client.fetch_user(int(userid))
    MAKER.append(int(userid))
    embed = discord.Embed(description=f'{to}(ID: {userid}) 유저 긴급 관리자권한 부여 완료!', color=0x0000ff)
    await ctx.send(embed=embed)
    status = None

@commands.is_owner()
@client.command()
async def deop(ctx, userid):
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    global status
    status = 'BLACKING'
    to = await client.fetch_user(int(userid))
    MAKER.remove(int(userid))
    embed = discord.Embed(description=f'{to}(ID: {userid}) 유저 긴급 관리자권한 제거 완료!', color=0xff0000)
    await ctx.send(embed=embed)
    status = None

@commands.is_owner()
@client.command()
async def oplist(ctx):
    oplist=[]
    for op in MAKER:
        try:
            opuser = await client.fetch_user(op)
            oplist.append(f'{opuser}(ID: {op})')
        except:
            pass
    answer='\n'.join(oplist)
    embed = discord.Embed(title='긴급 관리자 권한이 부여된 사용자 목록', description=answer, color=0x00ffff)
    await ctx.send(embed=embed)

@commands.is_owner()
@client.command()
async def user(ctx, userid):
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    global status
    status = 'BLACKING'
    to = await client.fetch_user(int(userid))
    USER.append(int(userid))
    embed = discord.Embed(description=f'{to}(ID: {userid}) 유저 긴급 사용자권한 부여 완료!', color=0x0000ff)
    await ctx.send(embed=embed)
    status = None

@commands.is_owner()
@client.command()
async def deuser(ctx, userid):
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    global status
    status = 'BLACKING'
    to = await client.fetch_user(int(userid))
    USER.remove(int(userid))
    embed = discord.Embed(description=f'{to}(ID: {userid}) 유저 긴급 사용자권한 제거 완료!', color=0xff0000)
    await ctx.send(embed=embed)
    status = None

@commands.is_owner()
@client.command()
async def userlist(ctx):
    userlist=[]
    for user in MAKER:
        try:
            useruser = await client.fetch_user(user)
            userlist.append(f'{useruser}(ID: {user})')
        except:
            pass
    answer='\n'.join(userlist)
    embed = discord.Embed(title='긴급 관리자 권한이 부여된 사용자 목록', description=answer, color=0x00ffff)
    await ctx.send(embed=embed)

@commands.is_owner()
@client.command()
async def kill(ctx, userid):
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    global status
    status = 'BLACKING'
    to = await client.fetch_user(int(userid))
    BLACK.append(int(userid))
    embed = discord.Embed(description=f'{to}(ID: {userid}) 유저 긴급킬 완료!', color=0x0000ff)
    await ctx.send(embed=embed)
    status = None

@commands.is_owner()
@client.command()
async def unkill(ctx, userid):
    if userid.startswith('<'):
        userid = userid.lstrip('<@!').rstrip('>')
    global status
    status = 'BLACKING'
    to = await client.fetch_user(int(userid))
    BLACK.remove(int(userid))
    embed = discord.Embed(description=f'{to}(ID: {userid}) 유저 긴급언킬 완료!', color=0xff0000)
    await ctx.send(embed=embed)
    status = None

@commands.is_owner()
@client.command()
async def killlist(ctx):
    killlist=[]
    for kill in BLACK:
        try:
            killuser = await client.fetch_user(kill)
            killlist.append(f'{killuser}(ID: {kill})')
        except:
            pass
    answer='\n'.join(killlist)
    embed = discord.Embed(title='킬된 사용자 목록', description=answer, color=0x00ffff)
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    global missingperms
    if hasattr(ctx.command, 'on_error'): return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'{ctx.author.mention}, 현재 명령어가 쿨타임 상태입니다. {round(error.retry_after)}초 후에 다시 시도해주세요!') ; return
    if isinstance(error, commands.BotMissingPermissions):
        await krmissingperms(error)
        await ctx.send(f'{ctx.message.author.mention}, 봇에 `{missingperms}` 권한이 없어 명령을 실행할 수 없습니다.')
    if isinstance(error, commands.MissingPermissions):
        await krmissingperms(error)
        await ctx.send(f'{ctx.message.author.mention}, 당신에게 `{missingperms}`권한이 없어 명령 실행이 거부되었습니다.')
    error = getattr(error, 'original', error)
    if isinstance(error, discord.NotFound):
        try:
            global status
            if status == 'BLACKING':
                embed = discord.Embed(description='올바르지 않은 유저아이디가 입력되었습니다.', color=0xff0000)
                await requiredby(ctx, embed)
                await ctx.send(embed=embed)
                status = None
        except NameError:
            pass

async def krmissingperms(error):
    global missingperms
    kor_missingperms=[]
    for eng_missingperms in error.missing_perms:
        if eng_missingperms == 'create_instant_invite':
            kor_missingperms.append('초대 코드 만들기')
        elif eng_missingperms == 'kick_members':
            kor_missingperms.append('멤버 추방하기')
        elif eng_missingperms == 'ban_members':
            kor_missingperms.append('멤버 차단하기')
        elif eng_missingperms == 'administrator':
            kor_missingperms.append('관리자')
        elif eng_missingperms == 'manage_channels':
            kor_missingperms.append('채널 관리하기|채널 관리')
        elif eng_missingperms == 'manage_guild':
            kor_missingperms.append('서버 관리하기')
        elif eng_missingperms == 'add_reactions':
            kor_missingperms.append('반응 추가하기')
        elif eng_missingperms == 'view_audit_log':
            kor_missingperms.append('감사 로그 보기')
        elif eng_missingperms == 'priority_speaker':
            kor_missingperms.append('우선 발언권')
        elif eng_missingperms == 'stream':
            kor_missingperms.append('동영상')
        elif eng_missingperms == 'view_channel':
            kor_missingperms.append('채널 보기')
        elif eng_missingperms == 'send_messages':
            kor_missingperms.append('메시지 보내기')
        elif eng_missingperms == 'send_tts_messages':
            kor_missingperms.append('텍스트 음성 변환 메시지 전송')
        elif eng_missingperms == 'manage_messages':
            kor_missingperms.append('메시지 관리')
        elif eng_missingperms == 'embed_links':
            kor_missingperms.append('링크 첨부')
        elif eng_missingperms == 'attach_files':
            kor_missingperms.append('파일 첨부')
        elif eng_missingperms == 'read_message_history':
            kor_missingperms.append('메시지 기록 보기')
        elif eng_missingperms == 'mention_everyone':
            kor_missingperms.append('@everyone/@here/모든 역할 멘션하기')
        elif eng_missingperms == 'use_external_emojis':
            kor_missingperms.append('외부 이모티콘 사용하기')
        elif eng_missingperms == 'view_guild_insights':
            kor_missingperms.append('서버 인사이트 보기')
        elif eng_missingperms == 'connect':
            kor_missingperms.append('연결')
        elif eng_missingperms == 'speak':
            kor_missingperms.append('말하기')
        elif eng_missingperms == 'mute_members':
            kor_missingperms.append('멤버들의 마이크 음소거하기')
        elif eng_missingperms == 'deafen_members':
            kor_missingperms.append('멤버의 헤드셋 음소거하기')
        elif eng_missingperms == 'move_members':
            kor_missingperms.append('멤버 이동')
        elif eng_missingperms == 'use_vad':
            kor_missingperms.append('음성 감지 사용')
        elif eng_missingperms == 'change_nickname':
            kor_missingperms.append('별명 변경하기')
        elif eng_missingperms == 'manage_nickname':
            kor_missingperms.append('별명 관리하기')
        elif eng_missingperms == 'manage_roles':
            kor_missingperms.append('역할 관리하기|권한 관리')
        elif eng_missingperms == 'manage_webhooks':
            kor_missingperms.append('웹후크 관리하기')
        elif eng_missingperms == 'manage_emojis':
            kor_missingperms.append('이모티콘 관리')
        else:
            kor_missingperms.append('알 수 없음')
    if len(kor_missingperms) > 1:
        missingperms=', '.join(kor_missingperms)
    else:
        missingperms=str(kor_missingperms).lstrip("['").rstrip("']")

@client.event
async def on_member_join(member):
    with open('black-user.json', 'r', encoding='utf-8') as readfile:
        blacklist = json.load(readfile)
    if str(member.id) in blacklist:
        await member.ban(reason='BLACKIST-AUTOMATICALLY EXECUTED by BOT', delete_message_days=0)
        logger.info(f'{member}(ID: {member.id})유저가 블랙리스트 등재 및 {member.guild}(ID: {member.guild.id})서버 입장으로 자동 차단됨.')

@client.event
async def on_message(message):
    if message.content == f'<@!{client.user.id}>':
        bucket = cd.get_bucket(message)
        ratelimit = bucket.update_rate_limit()
        if ratelimit == None:
            print(f'{message.guild.name}(ID: {message.guild.id})에서 {message.author}(ID: {message.author.id}이 멘션도움말 작동함.')
            global msgstatus
            msgstatus = True
            await help(message)
            msgstatus = False
        else:
            await message.channel.send(f'{message.author.mention}님, !helpme 명령어를 기억하세요!')
    await client.process_commands(message)

@client.event
async def on_guild_join(guild):
    overwrites={
        guild.me: discord.PermissionOverwrite(read_messages=True, manage_channels=True, send_messages=True, embed_links=True, attach_files=True, use_external_emojis=True),
        guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, read_message_history=True, add_reactions=False)
    }
    chanan = await guild.create_text_channel("blackbot-공지", overwrites=overwrites)
    await chanan.send('**이 채널을 삭제하지 마세요. 채널 이름은 바꾸셔도 됩니다.**\n채널 삭제는 가능하지만 삭제 시 봇에 대한 공지사항을 서버에서 받으실 수 없습니다.\n실수로 삭제하셨다면 봇을 다시 초대하시거나, 봇 서포트서버 공지채널을 팔로우하시면 됩니다.\n채널 권한 제한도 관리자 선택적으로 가능하며, 이에 따른 공지 미발송 등은 본인 책임입니다.')
    with open('black-chanan.txt', 'a') as f:
        f.write(str(chanan.id) + '\n')
    print(f'BOT is added to the guild: {guild.name}(ID: {guild.id})')

@client.event
async def on_guild_remove(guild):
    with open('black-chanan.txt', 'r') as f:
        list = f.readlines()
    for channel in guild.channels:
        if str(channel.id) in list:
            with open('black-chanan.txt', 'w') as g:
                for line in list:
                    if line.strip('\n') != str(channel.id):
                        g.write(line)
    print(f'BOT is removed from the guild: {guild.name}(ID: {guild.id})')

@client.event
async def on_guild_channel_delete(channel):
    with open('black-chanan.txt', 'r') as f:
        list = f.readlines()
    if str(channel.id) in list:
        with open('black-chanan.txt', 'w') as g:
            for line in list:
                if line.strip('\n') != str(channel.id):
                    g.write(line)

@client.event
async def on_ready():
    global cd
    cd = commands.CooldownMapping.from_cooldown(1, 360, commands.BucketType.user)
    global gs
    gs = len(client.guilds)
    logger.info(f'THE BOT IS READY. BOT IS ADDED {gs} GUILDS')
    global gu
    global gb
    gu = 0
    with open('black-user.json', 'r', encoding='utf-8') as readfile:
        blacklist = json.load(readfile)
    gb = len(blacklist)
    for guild in client.guilds:
        gu += len(guild.members)
    changing_presence.start()
    logger.info('SUCCESSFULLY STARTED THE ACTIVITY LOOP.')

@tasks.loop(seconds=53.0)
async def changing_presence():
    global gu
    global gs
    global gb
    await client.change_presence(activity=discord.Game(name='BLACKBOT 작동중!'))
    await asyncio.sleep(5)
    await client.change_presence(activity=discord.Game(name=f'BLACKBOT 작동중! - 안전한 디스코드를 만드는 그날까지'))
    await asyncio.sleep(8)
    await client.change_presence(activity=discord.Game(name=f'BLACKBOT 작동중! - {gs}개의 서버와 함께'))
    await asyncio.sleep(8)
    await client.change_presence(activity=discord.Game(name=f'BLACKBOT 작동중! - {gu}명의 유저들과 함께'))
    await asyncio.sleep(8)
    await client.change_presence(activity=discord.Game(name=f'BLACKBOT 작동중! - {gb}명의 유저가 등재됨'))
    await asyncio.sleep(8)
    await client.change_presence(activity=discord.Game(name='BLACKBOT 작동중! - 봇을 멘션해 도움말을 확인하세요!'))
    await asyncio.sleep(8)
    await client.change_presence(activity=discord.Game(name=f'BLACKBOT 작동중! - 버그 제보 및 기타 건의사항 등은 DS .𝙿#7777에게'))
    await asyncio.sleep(8)

TOKEN = os.environ['token']
try:
    client.run(TOKEN) ; TOKEN = None
except Exception as e:
    input(f'{e}오류로 인해 로그인에 실패하였습니다.')