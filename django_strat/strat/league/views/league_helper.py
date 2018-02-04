from league.models.transactions import Trades, TradePart,\
    TradePlayer, TradePick, TradeMoney


def collect_trades(year, team=None):
    if team is None:
        trade = Trades.objects.filter(year=year)
    else:
        trade = Trades.objects.filter(year=year, team=team)
    trades = []
    for t in trade:
        trd = collect_trade(t.id)
        trades.append(trd)
    return trades


def collect_trade(id):
    trade = Trades.objects.filter(id=id)
    trade_part = TradePart.objects.filter(trade=id)
    trade_vector_part = collect_trade_vectors(trade_part)
    trade_vector = []
    for t in trade_vector_part:
        trade_vector.append(collect_vector_part(t['giving'], t['receiving'], id))
    trade = {
        'trade': trade,
        'trade_vector': trade_vector,
    }
    return trade


def collect_trade_vectors(trade_parts):
    all_trade_vectors = []
    unique_trade_vectors = []
    for t in trade_parts:
        v = {
            'giving': t.team_giving,
            'receiving': t.team_receiving,
        }
        all_trade_vectors.append(v)
    for v in all_trade_vectors:
        if v not in unique_trade_vectors:
            unique_trade_vectors.append(v)
    return unique_trade_vectors


def collect_vector_part(giving, receiving, id):
    players = TradePlayer.objects.filter(team_giving=giving, team_receiving=receiving, trade=id)
    picks = TradePick.objects.filter(team_giving=giving, team_receiving=receiving, trade=id)
    money = TradeMoney.objects.filter(team_giving=giving, team_receiving=receiving, trade=id)
    vector = {
        'giving': giving,
        'receiving': receiving,
        'players': players,
        'picks': picks,
        'money': money,
    }
    return vector
