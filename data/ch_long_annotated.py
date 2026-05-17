"""Manual emotion annotation for ch_long.txt - sentence by sentence"""
# Format: (sentence_text, instruct_text_with_endofprompt)
# Moods:
#   SAD = grief, slow, heavy, trembling
#   WARM = nostalgic, tender, gentle affection
#   CALM = peaceful, contemplative, flowing

SAD = "An elderly woman, voice trembling with grief, speaking slowly and heavily, as if holding back tears. Each word is weighted with sorrow.<|endofprompt|>"
SAD_LIGHT = "An elderly woman, voice soft with quiet sadness. Speaking slowly, with a distant, world-weary tone, as if lost in painful memories.<|endofprompt|>"
SAD_CLIMAX = "An elderly woman, voice breaking with tears. Words come out choked and trembling, as if overwhelmed by a memory that still hurts deeply.<|endofprompt|>"
WARM = "A nostalgic middle-aged woman, recalling old memories with gentle affection. Soft, warm, tender tone, slightly slow, like telling a beloved story.<|endofprompt|>"
WARM_IRONIC = "A middle-aged woman, looking back at her younger self with gentle self-mockery. Warm but slightly amused, shaking her head at her own foolishness.<|endofprompt|>"
CALM = "A serene woman, reading beautiful prose by moonlight. Gentle, peaceful, contemplative, voice flowing like a quiet stream.<|endofprompt|>"
CALM_DREAMY = "A serene woman, voice soft and dreamy, as if describing something from a beautiful dream. Slow, floating, immersed in the scene.<|endofprompt|>"
CALM_WISTFUL = "A serene woman, voice gentle but touched with melancholy. Speaking slowly, as if missing something far away.<|endofprompt|>"
NORMAL = "A calm female narrator reading classic Chinese literature. Natural pacing, clear articulation.<|endofprompt|>"
FATHER = "A middle-aged woman, speaking in a gentle fatherly tone. Warm, caring, slightly gruff but full of love.<|endofprompt|>"
FATHER_WEAK = "An elderly woman, voice weak and trembling, as if spoken by an old man near the end of his life. Slow, labored, each word an effort.<|endofprompt|>"
POEM = "A serene woman, reciting ancient poetry. Rhythmic, lyrical, voice rising and falling with the verse, slow and deliberate.<|endofprompt|>"

ANNOTATIONS = [
    # === 背影 - Opening ===
    ("我与父亲不相见已二年余了，我最不能忘记的是他的背影", SAD_LIGHT),
    # === Paragraph 2: Death and funeral ===
    ("那年冬天，祖母死了，父亲的差使也交卸了，正是祸不单行的日子", SAD),
    ("我从北京到徐州，打算跟着父亲奔丧回家", SAD),
    ("到徐州见着父亲，看见满院狼藉的东西，又想起祖母，不禁簌簌地流下眼泪", SAD),
    ("父亲说：事已如此，不必难过，好在天无绝人之路", FATHER),
    # === Paragraph 3: Selling possessions ===
    ("回家变卖典质，父亲还了亏空", SAD),
    ("又借钱办了丧事", SAD),
    ("这些日子，家中光景很是惨澹，一半为了丧事，一半为了父亲赋闲", SAD),
    ("丧事完毕，父亲要到南京谋事，我也要回北京念书，我们便同行", NORMAL),
    # === Paragraph 4: Nanjing ===
    ("到南京时，有朋友约去游逛，勾留了一日", WARM),
    ("第二日上午便须渡江到浦口，下午上车北去", NORMAL),
    ("父亲因为事忙，本已说定不送我，叫旅馆里一个熟识的茶房陪我同去", WARM),
    ("他再三嘱咐茶房，甚是仔细", WARM),
    ("但他终于不放心，怕茶房不妥帖", WARM),
    ("颇踌躇了一会", WARM),
    ("其实我那年已二十岁，北京已来往过两三次，是没有什么要紧的了", WARM_IRONIC),
    ("他踌躇了一会，终于决定还是自己送我去", WARM),
    ("我再三劝他不必去", WARM),
    ("他只说：不要紧，他们去不好", FATHER),
    # === Paragraph 5: Train station ===
    ("我们过了江，进了车站", WARM),
    ("我买票，他忙着照看行李", WARM),
    ("行李太多了，得向脚夫行些小费才可过去", WARM),
    ("他便又忙着和他们讲价钱", WARM),
    ("我那时真是聪明过分，总觉他说话不大漂亮，非自己插嘴不可", WARM_IRONIC),
    ("但他终于讲定了价钱", WARM),
    ("就送我上车", WARM),
    ("他给我拣定了靠车门的一张椅子", WARM),
    ("我将他给我做的紫毛大衣铺好座位", WARM),
    ("他嘱我路上小心，夜里要警醒些，不要受凉", WARM),
    ("又嘱托茶房好好照应我", WARM),
    ("我心里暗笑他的迂", WARM_IRONIC),
    ("他们只认得钱，托他们只是白托", WARM_IRONIC),
    ("而且我这样大年纪的人，难道还不能料理自己么", WARM_IRONIC),
    ("我现在想想，我那时真是太聪明了", WARM_IRONIC),
    # === Paragraph 6: The orange scene (emotional climax) ===
    ("我说道：爸爸，你走吧", NORMAL),
    ("他往车外看了看，说：我买几个橘子去", FATHER),
    ("你就在此地，不要走动", FATHER),
    ("我看那边月台的栅栏外有几个卖东西的等着顾客", NORMAL),
    ("走到那边月台，须穿过铁道，须跳下去又爬上去", WARM),
    ("父亲是一个胖子，走过去自然要费事些", WARM),
    ("我本来要去的，他不肯，只好让他去", WARM),
    ("我看见他戴着黑布小帽，穿着黑布大马褂，深青布棉袍，蹒跚地走到铁道边，慢慢探身下去，尚不大难", WARM),
    ("可是他穿过铁道，要爬上那边月台，就不容易了", WARM),
    ("他用两手攀着上面，两脚再向上缩", WARM),
    ("他肥胖的身子向左微倾，显出努力的样子", WARM),
    ("这时我看见他的背影，我的泪很快地流下来了", SAD_CLIMAX),
    ("我赶紧拭干了泪", SAD),
    ("怕他看见，也怕别人看见", SAD),
    ("我再向外看时，他已抱了朱红的橘子往回走了", WARM),
    ("过铁道时，他先将橘子散放在地上，自己慢慢爬下，再抱起橘子走", WARM),
    ("到这边时，我赶紧去搀他", WARM),
    ("他和我走到车上，将橘子一股脑儿放在我的皮大衣上", WARM),
    ("于是扑扑衣上的泥土，心里很轻松似的", WARM),
    ("过一会儿说：我走了，到那边来信", FATHER),
    ("我望着他走出去", WARM),
    ("他走了几步，回过头看见我，说：进去吧，里边没人", FATHER),
    ("等他的背影混入来来往往的人里，再找不着了，我便进来坐下，我的眼泪又来了", SAD_CLIMAX),
    # === Paragraph 7: Later years ===
    ("近几年来，父亲和我都是东奔西走，家中光景是一日不如一日", SAD_LIGHT),
    ("他少年出外谋生，独力支持，做了许多大事", WARM),
    ("哪知老境却如此颓唐", SAD),
    ("他触目伤怀，自然情不能自已", SAD),
    ("情郁于中，自然要发之于外", SAD),
    ("家庭琐屑便往往触他之怒", SAD),
    ("他待我渐渐不同往日", SAD),
    ("但最近两年不见，他终于忘却我的不好，只是惦记着我，惦记着我的儿子", WARM),
    ("我北来后，他写了一信给我，信中说道：我身体平安，惟膀子疼痛厉害，举箸提笔，诸多不便，大约大去之期不远矣", FATHER_WEAK),
    ("我读到此处，在晶莹的泪光中，又看见那肥胖的青布棉袍黑布马褂的背影", SAD_CLIMAX),
    ("唉", SAD),
    ("我不知何时再能与他相见", SAD_CLIMAX),
    # === 荷塘月色 - Opening ===
    ("这几天心里颇不宁静", CALM),
    ("今晚在院子里坐着乘凉，忽然想起日日走过的荷塘，在这满月的光里，总该另有一番样子吧", CALM),
    ("月亮渐渐地升高了，墙外马路上孩子们的欢笑，已经听不见了", CALM_DREAMY),
    ("妻在屋里拍着闰儿，迷迷糊糊地哼着眠歌", CALM_DREAMY),
    ("我悄悄地披了大衫，带上门出去", CALM),
    # === Moonlight paragraph 2: The path ===
    ("沿着荷塘，是一条曲折的小煤屑路", CALM),
    ("这是一条幽僻的路", CALM),
    ("白天也少人走，夜晚更加寂寞", CALM),
    ("荷塘四面，长着许多树，蓊蓊郁郁的", CALM),
    ("路的一旁，是些杨柳，和一些不知道名字的树", CALM),
    ("没有月光的晚上，这路上阴森森的，有些怕人", CALM),
    ("今晚却很好，虽然月光也还是淡淡的", CALM),
    # === Moonlight paragraph 3: Solitude ===
    ("路上只我一个人，背着手踱着", CALM),
    ("这一片天地好像是我的", CALM),
    ("我也像超出了平常的自己，到了另一个世界里", CALM_DREAMY),
    ("我爱热闹，也爱冷静", CALM),
    ("爱群居，也爱独处", CALM),
    ("像今晚上，一个人在这苍茫的月下，什么都可以想，什么都可以不想，便觉是个自由的人", CALM_DREAMY),
    ("白天里一定要做的事，一定要说的话，现在都可不理", CALM),
    ("这是独处的妙处，我且受用这无边的荷香月色好了", CALM_DREAMY),
    # === Moonlight paragraph 4: Lotus leaves and flowers ===
    ("曲曲折折的荷塘上面，弥望的是田田的叶子", CALM),
    ("叶子出水很高，像亭亭的舞女的裙", CALM_DREAMY),
    ("层层的叶子中间，零星地点缀着些白花，有袅娜地开着的，有羞涩地打着朵儿的", CALM_DREAMY),
    ("正如一粒粒的明珠，又如碧天里的星星，又如刚出浴的美人", CALM_DREAMY),
    ("微风过处，送来缕缕清香，仿佛远处高楼上渺茫的歌声似的", CALM_DREAMY),
    ("这时候叶子与花也有一丝的颤动，像闪电般，霎时传过荷塘的那边去了", CALM),
    ("叶子本是肩并肩密密地挨着，这便宛然有了一道凝碧的波痕", CALM_DREAMY),
    ("叶子底下是脉脉的流水，遮住了，不能见一些颜色", CALM),
    ("而叶子却更见风致了", CALM_DREAMY),
    # === Moonlight paragraph 5: Moonlight ===
    ("月光如流水一般，静静地泻在这一片叶子和花上", CALM_DREAMY),
    ("薄薄的青雾浮起在荷塘里", CALM_DREAMY),
    ("叶子和花仿佛在牛乳中洗过一样", CALM_DREAMY),
    ("又像笼着轻纱的梦", CALM_DREAMY),
    ("虽然是满月，天上却有一层淡淡的云，所以不能朗照", CALM),
    ("但我以为这恰是到了好处——酣眠固不可少，小睡也别有风味的", CALM),
    ("月光是隔了树照过来的，高处丛生的灌木，落下参差的斑驳的黑影，峭楞楞如鬼一般", CALM),
    ("弯弯的杨柳的稀疏的倩影，却又像是画在荷叶上", CALM_DREAMY),
    ("塘中的月色并不均匀", CALM),
    ("但光与影有着和谐的旋律，如梵婀玲上奏着的名曲", CALM_DREAMY),
    # === Moonlight paragraph 6: Surroundings ===
    ("荷塘的四面，远远近近，高高低低都是树，而杨柳最多", CALM),
    ("这些树将一片荷塘重重围住", CALM),
    ("只在小路一旁，漏着几段空隙，像是特为月光留下的", CALM),
    ("树色一例是阴阴的，乍看像一团烟雾", CALM),
    ("但杨柳的丰姿，便在烟雾里也辨得出", CALM),
    ("树梢上隐隐约约的是一带远山，只有些大意罢了", CALM),
    ("树缝里也漏着一两点路灯光，没精打采的，是渴睡人的眼", CALM),
    ("这时候最热闹的，要数树上的蝉声与水里的蛙声", CALM),
    ("但热闹是它们的，我什么也没有", CALM_WISTFUL),
    # === Lotus gathering memory ===
    ("忽然想起采莲的事情来了", WARM),
    ("采莲是江南的旧俗，似乎很早就有，而六朝时为盛", WARM),
    ("从诗歌里可以约略知道", NORMAL),
    ("采莲的是少年的女子，她们是荡着小船，唱着艳歌去的", WARM),
    ("采莲人不用说很多，还有看采莲的人", WARM),
    ("那是一个热闹的季节，也是一个风流的季节", WARM),
    ("梁元帝采莲赋里说得好", NORMAL),
    ("于是妖童媛女，荡舟心许", POEM),
    ("鷁首徐回，兼传羽杯", POEM),
    ("棹将移而藻挂，船欲动而萍开", POEM),
    ("尔其纤腰束素，迁延顾步", POEM),
    ("夏始春余，叶嫩花初，恐沾裳而浅笑，畏倾船而敛裾", POEM),
    ("可见当时嬉游的光景了", WARM),
    ("这真是有趣的事，可惜我们现在早已无福消受了", CALM_WISTFUL),
    # === Xizhou Qu poem ===
    ("于是又记起西洲曲里的句子", CALM),
    ("采莲南塘秋，莲花过人头", POEM),
    ("低头弄莲子，莲子清如水", POEM),
    # === Ending ===
    ("今晚若有采莲人，这儿的莲花也算得过人头了", CALM_WISTFUL),
    ("只不见一些流水的影子，是不行的", CALM_WISTFUL),
    ("这令我到底惦着江南了", CALM_WISTFUL),
    ("这样想着，猛一抬头，不觉已是自己的门前", CALM),
    ("轻轻地推门进去，什么声息也没有，妻已睡熟好久了", CALM_DREAMY),
    ("一九二七年七月，北京清华园", NORMAL),
]
