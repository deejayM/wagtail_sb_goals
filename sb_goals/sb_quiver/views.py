from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Board


def home(request):

    context = {
        'boards': Board.objects.all()
    }
    return render(request, 'sb_quiver/home.html', context)

class BoardListView(ListView):
    model = Board
    template_name = 'sb_quiver/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'boards'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        user = kwargs.pop('user', self.request.user)
        return Board.objects.filter(author=user).order_by('-date_posted')


class UserBoardListView(ListView):
    model = Board
    template_name = 'sb_quiver/user_boards.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'boards'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Board.objects.filter(author=user).order_by('-date_posted')


class BoardDetailView(DetailView):
    model = Board

class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    fields = ['title', 'image', 'length', 'width', 'thickness', 'volume', 'wave_range_start',
            'wave_range_start', 'wave_range_end', 'shaper', 'year', 'make', 'notes']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.volume = form.instance.width * form.instance.length * 2.5 # we need to put a calculation here
        return super().form_valid(form)

class BoardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Board
    fields = ['title', 'image', 'length', 'width', 'thickness', 'volume', 'wave_range_start',
                'wave_range_start', 'wave_range_end', 'shaper', 'year', 'make', 'notes']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.volume = form.instance.width * form.instance.length * 2.5 # we need to put a calculation here
        return super().form_valid(form)

    def test_func(self):
        board = self.get_object()
        if self.request.user == board.author:
            return True
        return False

class BoardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Board
    success_url = '/'

    def test_func(self):
        board = self.get_object()
        if self.request.user == board.author:
            return True
        return False


def about(request):
    return render(request, 'sb_quiver/about.html', {'title': 'About'})

