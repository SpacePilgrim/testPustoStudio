"""Приложение подразумевает ежедневный вход пользователя, начисление баллов за вход. 
Нужно отследить момент первого входа игрока для аналитики. 
Также у игрока имеются игровые бонусы в виде нескольких типов бустов. 
Нужно описать модели игрока и бустов с возможностью начислять игроку бусты за прохождение уровней или вручную. (Можно написать, применяя sqlachemy)"""

from django.db import models


class Player(models.Model):
    pass
    

class Boost(models.Model):
    pass
