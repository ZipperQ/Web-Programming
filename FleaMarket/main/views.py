from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .forms import ThingForm
from .forms import Thing
from .models import Chat
from .forms import MessageForm
from .forms import CustomUserChangeForm
from django.contrib import messages
from django.db.models import Count, Case, When, IntegerField, Q


def index(request):
    # Получение всех товаров, исключая те, которые принадлежат текущему пользователю
    if request.user.is_authenticated:
        products = Thing.objects.exclude(owner=request.user).order_by('?')  # Исключение товаров текущего пользователя
    else:
        products = Thing.objects.order_by('?')  # Если пользователь не авторизован, то показываются все товары

    return render(request, 'main/index.html', {'products': products})


def about(request):
    return render(request, 'main/about.html')


@login_required
def create(request):
    if request.method == 'POST':
        form = ThingForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user  # Присвоение владельца - текущего пользователя
            product.save()
            return redirect('homepage')  # Перенаправление в профиль после создания товара
    else:
        form = ThingForm()

    return render(request, 'main/create.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматическая авторизация пользователя после регистрации
            return redirect('homepage')  # Перенаправление на главную страницу или другую страницу после регистрации
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})


@login_required
def profile(request, username):
    user_products = Thing.objects.filter(owner=request.user)  # Получение всех товаров, созданных пользователем
    user = get_object_or_404(User, username=username)  # Получение пользователя по username
    return render(request, 'main/profile.html', {'user_profile': user, 'products': user_products})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Thing, id=product_id)

    # Создание чата при заходе, если пользователь не владелец
    chat = None
    if request.user.is_authenticated and request.user != product.owner:
        chat, created = Chat.objects.get_or_create(
            product=product,
            participant=request.user,
            defaults={'owner': product.owner}
        )

    # Получение chat_id из GET-параметра
    chat_id = request.GET.get('chat_id')
    if chat_id and request.user == product.owner:
        chat = get_object_or_404(Chat, id=chat_id, product=product)

    if chat and request.user == product.owner:
        chat.messages.filter(is_read=False, sender=chat.participant).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.chat = chat
            message.save()
            return redirect(f'{request.path}?chat_id={chat.id}')
    else:
        form = MessageForm()

    messages = chat.messages.all().order_by('timestamp') if chat else []

    all_chats = None
    if request.user == product.owner:
        all_chats = Chat.objects.filter(product=product).annotate(
            message_count=Count('messages'),
            unread_count=Count(
                Case(
                    When(Q(messages__is_read=False) & ~Q(messages__sender=product.owner), then=1),
                    output_field=IntegerField()
                )
            )
        ).filter(message_count__gt=0)

    return render(request, 'main/thing.html', {
        'product': product,
        'chat': chat,
        'messages': messages,
        'form': form,
        'all_chats': all_chats,
    })


def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Thing.objects.filter(name__icontains=query)  # Search by item name

    return render(request, 'main/search.html', {'results': results, 'query': query})


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Thing, id=product_id, owner=request.user)
    if request.method == 'POST':
        form = ThingForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ThingForm(instance=product)

    return render(request, 'main/edit_thing.html', {'form': form})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Thing, id=product_id, owner=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('profile', username=request.user.username)

    return render(request, 'main/delete_thing.html', {'product': product})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('profile', username=request.user.username)
    else:
        user_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'main/edit_profile.html', {'user_form': user_form})
