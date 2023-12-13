from django import template
from players.models import *


register = template.Library()


@register.simple_tag()
def get_teams(filter=None):
    if not filter:
        return Team.objects.all()
    return Team.objects.filter(pk=filter)


@register.inclusion_tag('players/team_list.html')
def show_teams(sort=None, team_selected=0):
    if not sort:
        teams = Team.objects.all()
    else:
        teams = Team.objects.order_by(sort)
    return {"teams": teams, "team_selected": team_selected}
