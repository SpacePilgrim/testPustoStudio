# Поскольку игроков большое количество (!= 1), то имеет смысл либо добавление новой модели, которая будет содержать данные о призах, полученных игроком, 
# либо модификация существующей модели - например LevelPrize - добавлением поля с идентификатором игрока, тогда будет удобно отслеживать полученные каждым игроком призы за уровни.
# Выберу вариант с модификацией указанной модели.
from django.db import models
from django.utils import timezone # для задания 1
import csv                                   # для задания 2
from django.db.models import Prefetch        #
from django.core.paginator import Paginator  #

class Player(models.Model):
    player_id = models.CharField(max_length=100)
    
    
class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    
    
class Prize(models.Model):
    title = models.CharField()
    
    
class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    
    
class LevelPrize(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE) # новое поле в таблице - игрок - для удобного определения выданных за уровень призов
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()

# При написании указанного метода предполагается, что данные в таблице PlayerLevel заполнены, иначе нельзя проверить, окончен ли уровень и можно ли выдавать приз игроку
def award_player(player_ident, level_title):
    player_db = Player.objects.filter(player_id=player_ident).first()
    level_db = Level.objects.filter(title=level_title).first()
    
    if player_db is not None and level_db is not None:
        completed_level = PlayerLevel.objects.filter(player=player_db, level=level_db).first()
        
        if completed_level is not None and completed_level.is_completed:
            prize_db = LevelPrize.objects.filter(levelprize__level=level_db).first()
            
            if prize_db is not None:
                granted_award = LevelPrize.objects.create(player=player_db, level=level_db, prize=prize_db, received=timezone.now())
                granted_award.save()
                return True
    return False

# Буфер обработки данных задается в batch_size и может быть изменен в зависимости от параметров эффективности системы
# При помощи prefetch_related мы получим структуру players с вложенными в нее данными player_id и относящимися к этому игроку записями из моделей PlayerLeve и LevelPrize
# Далее после обработки каждой такой записи будем записывать ее в файл
def export_csv_data(filename, batch_size=1000):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        awriter.writerow(['Player ID', 'Level title', 'Level completed', 'Awarded prize']) # опциональная строка, в случае если далее файл пойдет на автоматическую обработку, то скорее всего ее нужно будет убрать

        players = Player.objects.prefetch_related(
            Prefetch('playerlevel_set', queryset=PlayerLevel.objects.select_related('level')),
            Prefetch('levelprize_set', queryset=LevelPrize.objects.select_related('level', 'prize'))

        paginator = Paginator(players, batch_size)

        for page_num in paginator.page_range:
            page = paginator.page(page_num)
            for player in page.object.list:
                for player_level in player.playerlevel_set.all():
                    level_prize = player.levelprize_set.filter(level=player_level.level).first()
                    prize_title = level_prize.prize.title if level_prize.prize.title else 'No prize'
                    writer.writerow([
                        player.player_id,
                        player_level.level.title,
                        '+' if player_level.is_completed else '-',
                        prize_title
                    ])
