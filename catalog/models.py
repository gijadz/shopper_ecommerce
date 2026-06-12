from django.db import models
from django.conf import settings

class Category(models.Model): #modello per le categorie di prodotti
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model): #modello per i prodotti
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    # Relazione obbligatoria: ogni prodotto è legato a una categoria
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Cart(models.Model): #modello per il carrello (per singolo utente))
    #specifico con relazione OneToOne che il carrello appartiene a un solo utente
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    #calcolo il prezzo totale di tutto il carrello
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

    #contatore di oggetti totali nel carrello
    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model): #modello per gli oggetti dentro al carrello (relazione molti a uno con Cart)
    #collego l'oggetto al carrello e al prodotto specifico
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    #calcolo il costo totale del singolo articolo (prezzo*quantità)
    def get_cost(self):
        return self.product.price * self.quantity


class Order(models.Model): #modello per gli ordini (relazione molti a uno con l'utente)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=50, verbose_name="Nome")
    last_name = models.CharField(max_length=50, verbose_name="Cognome")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=250, verbose_name="Indirizzo")
    postal_code = models.CharField(max_length=20, verbose_name="CAP")
    city = models.CharField(max_length=100, verbose_name="Città")
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False) #simula i pagamenti

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model): #modello per gli oggetti dentro l'ordine (relazione molti a uno con Order)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity