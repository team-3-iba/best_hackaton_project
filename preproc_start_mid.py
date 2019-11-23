important = {'ABS (антиблокировочная система)',
     'AUX/iPod',
     'Bluetooth',
     'CD/MP3 проигрыватель',
     'ESP (система поддержания динамической стабильности)',
     'USB',
     'Автозапуск двигателя',
     'Антипробуксовочная система',
     'Датчик дождя',
     'Дополнительные опции:',
     'Иммобилайзер',
     'Камера заднего вида',
     'Климат-контроль',
     'Кондиционер',
     'Контроль мертвых зон на зеркалах',
     'Круиз-контроль',
     'Ксеноновые фары',
     'Легкосплавные диски',
     'Люк',
     'Материал салона - натуральная кожа',
     'Мультимедийный экран',
     'Обогрев зеркал',
     'Обогрев лобового стекла',
     'Обогрев руля',
     'Обогрев сидений',
     'Панорамная крыша',
     'Парктроники',
     'Подушки безопасности боковые',
     'Подушки безопасности задние',
     'Подушки безопасности передние',
     'Противотуманные фары',
     'Рейлинги на крыше',
     'Светодиодные фары',
     'Сигнализация',
     'Системы помощи',
     'Управление мультимедиа с руля',
     'Фаркоп',
     'Цвет салона - темный',
     'Штатная навигация',
     'Электрорегулировка сидений',
     'Электростеклоподъемники задние',
     'Электростеклоподъемники передние',
     'Материал салона - натуральная кожа'}

def _get_region(lst):
    if len(lst) == 1:
        return lst[0]
    return lst[1]

def check_m(lst):
    if lst[0] == 'Опубликовано':
        return 0
    return 1

def get_d(lst):
    if len(lst) == 4:
        return 1
    return 0

def preproc(avto):
    for imp in important:
        avto[imp] = avto.table.apply(lambda x: int(imp in x))
    avto.cuzov = avto.cuzov.apply(lambda x: x.split()[0])
    avto.fuel = avto.fuel.apply(lambda x: x.split()[0])
    
    avto['cost'] = avto['cost'].str.replace(' ', '').astype('int')

    avto['volume'] = avto['volume'].fillna('0').str.replace(' см3', '').astype('int')

    avto['run'] = avto['run'].str.replace(' км', '')
    miles_mask = avto['run'].str.endswith(' миль')
    avto.loc[miles_mask, 'run'] = avto[miles_mask]['run'].str.replace(' миль', '').astype('int') * 1.60934
    avto['run'] = avto['run'].astype('int')

    avto['today_views'] = avto['show'].str.extract('\+(.+) ')

    avto['show'] = avto['show'].str.extract('(.*)' + ' '*25)
    avto.rename(columns={'show': 'all_views'}, inplace=True)

    today_view_mask = pd.isna(avto['today_views'])
    avto.loc[today_view_mask, 'today_views'] = avto[today_view_mask]['all_views']
    
    avto['drive-unit'].fillna(value=0, inplace=True)
    temp = avto['drive-unit'].value_counts().index[0]
    for ind in avto.index:
        if ind == 0:
            avto.loc[avto['drive-unit'] == ind, 'drive-unit'] = temp
    
    avto['today_views'] = avto['today_views'].str.replace(' ', '').astype('int')
    avto['all_views'] = avto['all_views'].str.replace(' ', '').astype('int')
    
    tmp = list(map(lambda s: s.split(', '), avto.region))
    avto.region = list(map(_get_region, tmp))
    
    df['date'] = df['update'].apply(lambda x: x.split()[1])
    df['modified'] = df['update'].apply(lambda x: check_m(x.split()))
    df['up'] = df['update'].apply(lambda x: get_d(x.split()))

    return avto
