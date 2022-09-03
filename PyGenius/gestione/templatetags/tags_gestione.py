import datetime

from django import template
from django.shortcuts import get_object_or_404

from ..models import Canzone

register = template.Library()

@register.simple_tag
def ip(request):
    return sum(list(map(int,request.META['REMOTE_ADDR'].split(sep='.'))))


@register.simple_tag
def visita(canzone, utente):
    c = get_object_or_404(Canzone, pk=canzone.pk)
    found = False
    with open(c.file_visite,'r') as file:
        for line in file:
            list_line = line.split(sep=',')
            if int(list_line[1]) == utente:
                found = True

    if not found:
        try:
            c.visite += 1
            with open(c.file_visite,'a') as file:
                dat = (f'{datetime.date.today().month}/{datetime.date.today().year}', utente)
                for i in dat:
                    file.write(f'{i},')
                file.write('\n')
            c.save()



        except Exception as e:
            print(f'Errore nel aumentare le visite: {e}')


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()





# @register.simple_tag
# def popolarità(canzone, mese_anno = (datetime.date.today().month,datetime.date.today().year)):
#
#     visite_tot = Canzone.objects.aggregate(Sum('visite'))['visite__sum']
#     c = get_object_or_404(Canzone, pk=canzone.pk)
#     l = []
#
#     with open(c.file_visite,'r') as file:
#         for line in file:
#             l.append(np.array(line.split(sep=',')))
#
#     matrice = np.row_stack(l)
#     #print(matrice)
#     s = ((np.unique(matrice[:,:1]).tolist()))
#     counts=[]
#     #print(s)
#     for el in s:
#         counts.append((el,(matrice[:,:1] == el).sum()))
#     #print(counts)
#     p=sum(list(map(lambda x: (int(x[1])/(distanza(x[0])+1))/(visite_tot+1),counts)))
#     try:
#         c.popolarità = p
#         c.save()
#     except Exception as e:
#         print(e)
#     return (p,visite_tot)


