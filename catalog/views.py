from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProductForm, OrderCreateForm
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Product, Cart, CartItem, OrderItem, Order, Category


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    #gestisce la barra di ricerca e il filtro delle categorie
    def get_queryset(self):
        #select_related per precaricare la categoria associata a ciascun prodotto
        queryset = super().get_queryset().select_related('category')
        query = self.request.GET.get('q')  #prende la parola cercata
        category_id = self.request.GET.get('category')  #prende la categoria cliccata

        if query:
            queryset = queryset.filter(name__icontains=query)  #cerca nel nome
        if category_id:
            queryset = queryset.filter(category_id=category_id)  #filtra per categoria

        return queryset

    #aggiunge le categorie per il filtro
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


#impongo che solo lo Store Manager può aggiungere prodotti
class ProductCreateView(UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    #permission check
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_manager


#funzione per aggiungere un prodotto al carrello (solo per utenti loggati)
@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    #ritorna alla pagina da cui proveniva l'utente
    next_page = request.META.get('HTTP_REFERER', 'product_list')

    #controllo dello stock (se il prodotto è esaurito blocca l'operazione)
    if product.stock <= 0:
        return redirect(next_page)

    #recupera il carrello dell'utente o lo crea se vuoto
    cart, created = Cart.objects.get_or_create(user=request.user)

    #se il prodotto è già nel carrello aumenta la quantità sennò lo crea
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        #aumenta la quantità solo se non supera lo stock disponibile
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()

    return redirect(next_page)


#diminuisce di 1 la quantità di un elemento nel carrello
@login_required
@require_POST
def decrease_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart_detail')


#vista della schermata del carrello
class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #passa il carrello dell'utente al template HTML
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        return context


@login_required
def order_create(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    #se il carrello è vuoto impedisce l'accesso alla pagina di acquisto
    if not cart.items.all():
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():

            #controllo, prima di confermare il pagamento, che la quantità del prodotto sia disponibile nello stock
            for item in cart.items.all():
                if item.quantity > item.product.stock:
                    form.add_error(None,
                                   f"Spiacenti, il prodotto '{item.product.name}' non ha scorte sufficienti (Disponibili: {item.product.stock}). Modifica il carrello.")
                    return render(request, 'catalog/order_create.html', {'cart': cart, 'form': form})

            order = form.save(commit=False)
            order.user = request.user
            order.save()

            #trasferisce gli articoli dal carrello ai dettagli dell'ordine
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )

                #diminuisce automaticamente la quantità acquistata dal magazzino
                product = item.product
                product.stock -= item.quantity
                product.save()

            #svuota il carrello dell'utente nel database
            cart.items.all().delete()

            #mostra la pagina di "Acquisto completato"
            return render(request, 'catalog/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'catalog/order_create.html', {'cart': cart, 'form': form})


#voglio modificare un prodotto già esistente e impongo che solo lo Store Manager può modificare i prodotti
class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    #solo il manager e il superuser/admin possono modificare
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_manager


#eliminare un prodotto
class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_manager


#visualizzare lo storico ordini del cliente
class CustomerOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'catalog/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        #il cliente vede solo i propri ordini dal più recente al più vecchio
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


#storico ordini degli utenti per lo Store Manager/admin
class ManagerOrderListView(UserPassesTestMixin, ListView):
    model = Order
    template_name = 'catalog/manager_order_list.html'
    context_object_name = 'orders'

    def test_func(self):
        #solo i manager possono accedere a questa pagina
        return self.request.user.is_authenticated and self.request.user.is_manager

    def get_queryset(self):
        #il manager vede tutti gli ordini del negozio
        return Order.objects.all().order_by('-created_at')


#dettaglio del singolo prodotto
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


@login_required
@require_POST 
def remove_from_cart(request, product_id):
    #recupero il carrello dell'utente in modo sicuro
    cart, created = Cart.objects.get_or_create(user=request.user)
    #trovo il prodotto da rimuovere
    product = get_object_or_404(Product, id=product_id)
    #elimino l'oggetto dal carrello
    CartItem.objects.filter(cart=cart, product=product).delete()
    return redirect('cart_detail')
