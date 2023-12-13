from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from .utils import *


class PlayersHome(DataMixin, ListView):
    paginate_by = 10
    model = Player
    template_name = 'players/index.html'
    context_object_name = 'players'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context['player_name'] = self.request.GET.get('player_name', '')
        context['team_name'] = self.request.GET.get('team_name', '')
        return {**context, **c_def}

    def get_queryset(self):
        players = Player.objects.select_related('team')

        player_name = self.request.GET.get('player_name', '')
        team_name = self.request.GET.get('team_name', '')

        if player_name:
            players = players.filter(name__icontains=player_name)

        if team_name:
            players = players.filter(team__name__icontains=team_name)

        return players


def about(request):
    return render(request, 'players/about.html', {'menu': menu, 'title': 'О сайте'})


def teams(request, team_id):
    if request.GET:
        print(request.GET)
    if int(team_id) > 100:
        return redirect('home', permanent=True)
    return HttpResponse(f"team's id: {team_id}")


class AddPlayer(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPlayerForm
    template_name = 'players/add_player.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление игрока")
        return {**context, **c_def}


def delete_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player.delete()
    return redirect('home')


def edit_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        form = AddPlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPlayerForm(instance=player)
    d = {'form': form, 'player': player}
    return render(request, 'players/edit_player.html', d)


def player_list(request):
    player_name = request.GET.get('player_name', '')
    team_name = request.GET.get('team_name', '')

    players = Player.objects.all()

    if player_name:
        players = players.filter(name__icontains=player_name)

    if team_name:
        players = players.filter(team__name__icontains=team_name)

    context = {
        'title': 'Player List',
        'players': players,
        'player_name': player_name,
        'team_name': team_name,
    }

    return render(request, 'players/player_list.html', context)


class SearchPlayers(DataMixin, ListView):
    paginate_by = 3
    model = Player
    template_name = 'players/player_list.html'
    context_object_name = 'players'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Player List")
        context['player_name'] = self.request.GET.get('player_name', '')
        context['team_name'] = self.request.GET.get('team_name', '')
        return {**context, **c_def}

    def get_queryset(self):
        players = Player.objects.all()

        player_name = self.request.GET.get('player_name', '')
        team_name = self.request.GET.get('team_name', '')

        if player_name:
            players = players.filter(name__icontains=player_name)

        if team_name:
            players = players.filter(team__name__icontains=team_name)

        return players

def search_players(request):
    player_name = request.GET.get('player_name', '')
    team_name = request.GET.get('team_name', '')

    players = Player.objects.all()

    if player_name:
        players = players.filter(name__icontains=player_name)

    if team_name:
        players = players.filter(team__name__icontains=team_name)

    context = {
        'title': 'Player List',
        'players': players,
        'player_name': player_name,
        'team_name': team_name,
    }

    return render(request, 'players/player_list.html', context)


def contact(request):
    return HttpResponse("Обратная связь")


class ShowPlayer(DataMixin, DetailView):
    model = Player
    template_name = 'players/player.html'
    slug_url_kwarg = 'player_slug'
    context_object_name = 'player'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['player'])
        return context


class PlayersTeam(DataMixin, ListView):
    paginate_by = 3
    model = Player
    template_name = 'players/index.html'
    context_object_name = 'players'
    allow_empty = False

    def get_queryset(self):
        return Player.objects.filter(team__slug=self.kwargs['team_slug']).select_related('team')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str(context['players'][0].team),
                                      team_selected=context['players'][0].team_id)
        return {**context, **c_def}


def pageNotFound(request, exception):
    return HttpResponseNotFound("Страница не найдена :(")


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'players/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'players/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
