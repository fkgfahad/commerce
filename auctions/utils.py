from .models import Bid, Auction, Category, Comment, Whitelist


def add_whitelist(auction_id, user):
    try:
        a = Auction.objects.get(pk=auction_id)
        Whitelist(user=user, auction=a).save()
        return True
    except:
        return False


def remove_whitelist(id, user):
    try:
        a = Auction.objects.get(pk=id)
        Whitelist.objects.get(auction=a, user=user).delete()
        return True
    except:
        return False


def close_auction(user, id):
    try:
        a = Auction.objects.get(pk=id, user=user)
        if len(Bid.objects.filter(auction=a)) > 0:
            make_won(a)
        a.closed = True
        a.save()
        return True
    except:
        return False


def current_price(auction):
    try:
        return Bid.objects.filter(auction=auction).last().bid
    except Exception as e:
        print(e)
        return auction.price


def did_i_bid(auction, user):
    try:
        Bid.objects.get(user=user, auction=auction)
        return True
    except:
        return False


def make_won(auction):
    try:
        b = Bid.objects.filter(auction=auction).last()
        b.won = True
        b.save()
        return True
    except Exception as e:
        print(e)
        return False


def format_auction(auction, user):
    cp = current_price(auction)
    a = {
        'id': auction.id,
        'title': auction.title,
        'price': cp,
        'date': auction.date,
        'category': auction.category,
        'image': auction.image,
        'closed': auction.closed,
        'description': auction.description
    }
    if user.is_authenticated:
        try:
            b = Bid.objects.get(user=user, auction=auction)
            a['mybid'] = b.bid
            if auction.closed and cp == b.bid and b.won:
                a['won'] = True
        except:
            pass
    return a
