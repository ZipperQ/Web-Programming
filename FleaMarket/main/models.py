from django.db import models
from django.contrib.auth.models import User


# Thing model
class Thing(models.Model):
    choice = [
        ('Электроника', 'Электроника'),
        ('Одежда и обувь', 'Одежда и обувь'),
        ('Мебель', 'Мебель'),
        ('Книги и журналы', 'Книги и журналы'),
        ('Детские товары', 'Детские товары'),
        ("Домашний декор и аксессуары", "Домашний декор и аксессуары"),
        ("Спортивные товары", "Спортивные товары"),
        ("Инструменты и садовый инвентарь", "Инструменты и садовый инвентарь"),
        ("Кухонные принадлежности", "Кухонные принадлежности"),
        ("Хобби и развлечения", "Хобби и развлечения"),
        ("Товары для домашних животных", "Товары для домашних животных"),
        ("Автомобильные товары", "Автомобильные товары"),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=choice)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)  # Card creation date
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Owner of the element (refers to the user)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


# Chat model
class Chat(models.Model):
    product = models.ForeignKey(Thing, on_delete=models.CASCADE)  # Link to item
    owner = models.ForeignKey(User, related_name='owner_chats', on_delete=models.CASCADE)  # Owner
    participant = models.ForeignKey(User, related_name='participant_chats',
                                    on_delete=models.CASCADE)  # The user who wrote the message

    def __str__(self):
        return f"Chat for {self.product.name} between {self.owner} and {self.participant}"


# Message model
class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)  # Link to chat
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # Sender
    content = models.TextField()  # Message text
    timestamp = models.DateTimeField(auto_now_add=True)  # Time
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"
