from django.contrib.auth import authenticate, login, logout, decorators
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Bid, Comment, Whitelist, Auction
from . import utils


def index(request):
    data = reversed(Auction.objects.filter(closed=False))
    contents = []
    for a in data:
        contents.append(utils.format_auction(auction=a, user=request.user))
    return render(request, "auctions/index.html", {
        'auctions': contents,
        'title': 'All Active Auctions'
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        'title': 'Categories',
        'categories': Category.objects.all()
    })


def category(request, category_id):
    cat = Category.objects.get(pk=category_id)
    data = []
    for a in reversed(Auction.objects.filter(category=cat, closed=False)):
        data.append(utils.format_auction(auction=a, user=request.user))
    return render(request, 'auctions/category.html', {
        'title': f'Category: {cat.name}',
        'auctions': data
    })


@login_required
def new_auction(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = int(request.POST['price'])
        url = request.POST['image']
        if url:
            image = url
        else:
            image = 'https://media.sproutsocial.com/uploads/2017/08/Social-Media-Video-Specs-Feature-Image.png'
        category = None
        try:
            category = Category.objects.get(pk=int(request.POST['category']))
        except ValueError:
            pass

        try:
            Auction(user=request.user, title=title, description=description,
                    price=price, image=image, category=category).save()
        except Exception as err:
            print(err)
            return render(request, 'auctions/new.html', {
                'categories': Category.objects.all(),
                'auction': title,
                'description': description,
                'price': price,
                'image': image,
                'message': 'Error creating auction. Please try again.'
            })

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/new.html', {
            'categories': Category.objects.all(),
            'title': 'Create A Listing'
        })


@login_required
def whitelist(request):
    data = Whitelist.objects.filter(user=request.user)
    response = {
        'title': 'Whitelist'
    }
    wh = []
    for item in data:
        wh.append(utils.format_auction(
            auction=item.auction, user=request.user))

    response['auctions'] = wh
    try:
        aid = int(request.GET['remove'])
        if utils.remove_whitelist(aid, request.user):
            return HttpResponseRedirect(reverse('whitelist'))
        else:
            response['message'] = 'Error removing whitelist.'
            pass
    except:
        pass

    return render(request, "auctions/whitelist.html", response)


@login_required
def bids(request):
    data = []
    for b in Bid.objects.filter(user=request.user):
        data.append(utils.format_auction(auction=b.auction, user=request.user))
    return render(request, "auctions/bids.html", {
        'title': 'My Bids',
        'auctions': data
    })


def auction(request, auction_id):
    response = {}
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        try:
            a = Auction.objects.get(pk=auction_id)
            print(Bid.objects.filter(auction=a))
            b = int(request.POST['bid'])
            if utils.did_i_bid(auction=a, user=request.user):
                response['message'] = 'You already placed a bid.'
            elif utils.current_price(a) < b:
                new_bid = Bid(user=request.user, auction=a, bid=b)
                new_bid.save()
                print(new_bid)
                return HttpResponseRedirect(reverse('auction', args=[auction_id]))
            else:
                response['message'] = 'Bid must be greater than current price.'
        except Exception as e:
            print(e)

    try:
        a = Auction.objects.get(pk=auction_id)
        a.price = utils.current_price(a)
        response['title'] = a.title
        response['auction'] = a
        try:
            wl_req = request.GET['whitelist']
            if wl_req == 'add':
                try:
                    Whitelist.objects.get(user=request.user, auction=a)
                    response['message'] = 'Already whitelisted.'
                except Exception as e:
                    print(e)
                    if utils.add_whitelist(auction_id, request.user):
                        return HttpResponseRedirect(reverse('auction', args=[auction_id]))
                    else:
                        response['message'] = 'Error Adding to whitelist.'
            elif wl_req == 'remove':
                if utils.remove_whitelist(auction_id, request.user):
                    return HttpResponseRedirect(reverse('auction', args=[auction_id]))
                else:
                    response['message'] = 'Error removing from whitelist.'
        except:
            pass

        try:
            if 'close' in request.GET:
                utils.close_auction(request.user, auction_id)
                return HttpResponseRedirect(reverse('auction', args=[auction_id]))
        except:
            pass

        try:
            if Whitelist.objects.get(user=request.user, auction=a):
                response['whitelisted'] = True
        except:
            response['whitelisted'] = False

        response['comments'] = reversed(Comment.objects.filter(auction=a))

        try:
            b = Bid.objects.get(user=request.user, auction=a)
            response['mybid'] = b.bid
            if a.closed and b.bid == a.price and b.won:
                response['won'] = True
        except:
            pass

        if a.user == request.user:
            try:
                allbids = []
                for biid in Bid.objects.filter(auction=a):
                    allbids.append({
                        'user': biid.user,
                        'bid': biid.bid,
                        'won': biid.won
                    })
                response['bids'] = allbids
            except:
                pass

        return render(request, "auctions/auction.html", response)
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('index'))


@login_required
def comment(request, auction_id):
    try:
        text = request.POST['comment']
        a = Auction.objects.get(pk=auction_id)
        Comment(user=request.user, auction=a, comment=text).save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(reverse('auction', args=[auction_id]))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                'title': 'Login'
            })
    else:
        return render(request, "auctions/login.html", {
            'title': 'Login'
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                'title': 'Register'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                'title': 'Register'
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            'title': 'Register'
        })
