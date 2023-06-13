# Freela do Workana
# Controle de Aluguéis

![w2.png](https://raw.githubusercontent.com/djangomy/immobile/main/w2.png)

Desenvolver um sistema que permita o controle de aluguéis de imóveis em uma imobiliária.

Fluxo

![core.png](https://raw.githubusercontent.com/djangomy/immobile/main/core.png)

- Cadastro de imóveis:  `Código, Tipo, endereço e Valor`

- Tipos: `APARTAMENTO, KITNET e CASA`

- Lista imóveis por `tipo` Na homepage e colocar Filtro por `tipo`. 

- Cadastro de Clientes: `Nome, e-mail e Telefone`

- Registrar de Locação: `Cliente, Imóvel, Período (Inicio e Término)`

- `Relatório` de Imóveis Locados.

- Layout Bootstrap `HTML/CSS/JS`

- Banco de Dados (`Sqlite3`)
  

Vídeo de como configurar Projeto: 

Repositório: `https://github.com/djangomy/config-default-simple.git`

Eu clonei o repositório !!! 

Depois de feito as configurações iniciais e executado o projeto. 

Vamos para criação do nosso modelo e estrutura do projeto.

Pack de imagens q vou utilizar no vídeo.

- Imagens pegar do repositório

Vamos lá.
 
<details><summary><b>Criar Modelo</b></summary>

- **Criar Modelo**
    
    myapp/models.py

    -- Cadastro  de Clientes

    ```python
    ## Cadastro de Clientes     
    class Client(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField(max_length=200)
        phone = models.CharField(max_length=15)
        
        def __str__(self):
            return "{} - {}".format(self.name, self.email)
        
        class Meta:
            verbose_name = 'Cliente'
            verbose_name_plural = 'Clientes'
            ordering = ['-id']
    ```

    -- Cadastro de Imóveis

    ```python
    ## Opções de Imóveis
    class TypeImmobile(models.TextChoices):
        APARTMENT = 'APARTAMENTO','APARTAMENTO'
        KITNET = 'KITNET','KITNET'
        HOUSE = 'CASA','CASA'

    ## Cadastro de Imóveis
    class Immobile(models.Model):
        code = models.CharField(max_length=100)
        type_item = models.CharField(max_length=100, choices=TypeImmobile.choices)
        address = models.TextField()
        price = models.DecimalField(max_digits=10,decimal_places=2)
        is_locate = models.BooleanField(default=False)
        
        
        def __str__(self):
            return "{} - {}".format(self.code, self.type_item)
        
        class Meta:
            verbose_name = 'Imóvel'
            verbose_name_plural = 'Imóveis'
            ordering = ['-id']
    ```

    ```python
    ## Cadastrar as Imagens do Imóvel
    class ImmobileImage(models.Model):
        image = models.ImageField('Images',upload_to='images')
        immobile = models.ForeignKey(Immobile, related_name='immobile_images', on_delete=models.CASCADE)
        
        def __str__(self):
            return self.immobile.code
    ```

    -- Registrar Locação

    ```python
    ## Registrar Locação
    class RegisterLocation(models.Model):
            immobile = models.ForeignKey(Immobile, on_delete=models.CASCADE, related_name='reg_location')
        client = models.ForeignKey(Client, on_delete=models.CASCADE)
        dt_start = models.DateTimeField('Inicio')
        dt_end = models.DateTimeField('Fim')
        create_at = models.DateField(default=datetime.now, blank=True)
        
        def __str__(self):
            return "{} - {}".format(self.client, self.immobile)
        
        class Meta:
            verbose_name = 'Registrar Locação'
            verbose_name_plural = 'Registrar Locação'
            ordering = ['-id']
    ```

    admin.py

    ```python
    class ImmobileImageInlineAdmin(admin.TabularInline):
        model = models.ImmobileImage
        extra = 0

    class ImmobileAdmin(admin.ModelAdmin):
        inlines = [ImmobileImageInlineAdmin]

    admin.site.register(models.Immobile, ImmobileAdmin)
    ```

</details>

<details><summary><b>Listar Imóveis</b></summary>

- **Listar Imóveis**
    
    *myapp/views.py*
    
    ```python
    def list_location(request):
    	 immobiles = Immobile.objects.filter(is_locate=False)
    	 context = {
            'immobiles': immobiles
        }
        return render(request, 'list-location.html', context)
    ```
    
    *myapp/urls.py*
    
    ```python
    from django.urls import path 
    from myapp import views
    
    urlpatterns = [
        path('', views.list_location, name='list-location'),
     ]
    ```
    
    *myapp/templates/list-location.html*
    
    ```python
    {% extends 'base.html' %}
    
    {% block title %}Lista de Locações{% endblock %}
    
    {% block content %} 
     
    <div class="container">
        <div class="cards">
            {% for immobile in immobiles %}  
            <div class="card-item h-100"> 
    			 			{% for el in immobile.immobile_images.all %}
                {% if forloop.first %}
                <img src="{{el.image.url}}" class="card-image"  width="100%" height="320" alt="{{el.id}}"> 
                {% endif %}  
                {% endfor %}   
                <div class="card-body p-3">
                    <p>Codígo: {{immobile.code}}</p> 
                    <p>Endereço: {{immobile.address}}</p>
                    <p>Valor: {{immobile.price}}</p>   
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="badge bg-success">Tipo: {{immobile.type_item}}</div> 
                    </div>
                </div>  
            </div> 
            {% endfor %} 
        </div>
    </div>
    {% endblock %}
    ```
    
    *base/static/css/style.css*
    
    Utilizando *Flexbox* para os cards na homepage.
    
    ```css
    .cards {
        display: flex;
        flex-wrap: wrap;
        align-items: stretch;
    }
     
    .card-item {
        flex: 0 0 25rem;
        box-sizing: border-box;
        margin: 1rem 0.25em;
        border-radius: 10px;
        border: 1px solid;
    }
    
    .card-image {
        border-radius: 10px;
    }
    ```
    
    Card Slide de Imagens 
    
    ```html
    <div class="card-image"> 
    	<div id="carouselIndicators{{immobile.id}}" class="carousel slide" data-bs-ride="false"> 
    		<div class="carousel-indicators">
    			{% for el in immobile.immobile_images.all %} 
    			{% if forloop.first %}
    			<button type="button" data-bs-target="#carouselIndicators{{immobile.id}}" data-bs-slide-to="{{forloop.counter0}}" class="active" aria-current="true" aria-label="Slide {{forloop.counter0}}"></button>
    			{% else %} 
    			<button type="button" data-bs-target="#carouselIndicators{{immobile.id}}" data-bs-slide-to="{{forloop.counter0}}" aria-label="Slide {{forloop.counter0}}"></button>
    			{% endif %}  
    			{% endfor %}  
    		</div> 
    		<div class="carousel-inner">
    			{% for el in immobile.immobile_images.all %}
    	 		<div class="carousel-item {% if forloop.first %}active{% endif %}">
    				<img src="{{el.image.url}}" class="card-image"  width="100%" height="320" alt="{{el.id}}">
    			</div>
    			{% endfor %}
    		</div>
    		<button class="carousel-control-prev" type="button" data-bs-target="#carouselIndicators{{immobile.id}}" data-bs-slide="prev">
    			<span class="carousel-control-prev-icon" aria-hidden="true"></span>
    			<span class="visually-hidden">Previous</span>
    		</button>
    		<button class="carousel-control-next" type="button" data-bs-target="#carouselIndicators{{immobile.id}}" data-bs-slide="next">
    			<span class="carousel-control-next-icon" aria-hidden="true"></span>
    			<span class="visually-hidden">Next</span>
    		</button>
    	</div>
    </div>
    ```

</details>

<details><summary><b>Formulário Cliente</b></summary>

- **Formulário Cliente**
    
    *myapp/forms.py*
    
    ```python
    ## Cadastra Cliente          
    class ClientForm(forms.ModelForm):
        class Meta:
            model = Client
            fields = '__all__'
            
        def __init__(self, *args, **kwargs): # Adiciona 
            super().__init__(*args, **kwargs)  
            for field_name, field in self.fields.items():   
                  field.widget.attrs['class'] = 'form-control'
    ```
    
    myapp/views.py
    
    ```python
    def form_client(request):
        form = ClientForm() 
        if request.method == 'POST':
            form = ClientForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('list-location')   
        return render(request, 'form-client.html', {'form': form})
    ```
    
    myapp/urls.py
    
    ```python
    from django.urls import path 
    from myapp import views
    
    urlpatterns = [
        path('', views.list_location, name='list-location'), 
        path('form-client/', views.form_client, name='client-create'), 
    ]
    ```
    
    *myapp/templates/form-client.html*
    
    ```html
    {% extends 'base.html' %} 
    
    {% block title %}Cadastrar Cliente{% endblock %}
    
    {% load static %}
    
    {% block content %}
    <div class="container"> 
        <div class="d-flex gap-4 mt-3">
     
            <img src="{% static 'images/client.jpg' %}" class="card-image" width="100%" height="500" alt="client">
      
            <form class="col-md-4" action="{% url 'client-create' %}" method="post">
                {% csrf_token %}
                <h3>Cadastrar Cliente</h3>
                {% for field in form %}
                <div class="mt-3">
                    {{field.label}}
                    {{field}}
                </div>
                {% endfor %}
                <input type="submit" class="btn btn-primary mt-3" value="Salvar">
            </form>
            
        </div> 
    </div>
    {% endblock %}
    ```

</details>

<details><summary><b>Formulário Imóvel</b></summary>

- **Formulário Imóvel**
    
    *myapp/forms.py*
    
    ```python
    class MultipleFileInput(forms.ClearableFileInput):
      allow_multiple_selected = True

    class MultipleFileField(forms.FileField):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault("widget", MultipleFileInput())
            super().__init__(*args, **kwargs)

        def clean(self, data, initial=None):
            single_file_clean = super().clean
            if isinstance(data, (list, tuple)):
                result = [single_file_clean(d, initial) for d in data]
            else:
                result = single_file_clean(data, initial)
            return result
  
    ## Cadastra um Imovel
    class ImmobileForm(forms.ModelForm):
        immobile = MultipleFileField()
        class Meta:
            model = Immobile
            fields = '__all__'
            exclude = ('is_locate',)
            
        def __init__(self, *args, **kwargs): # Adiciona 
            super().__init__(*args, **kwargs)  
            for field_name, field in self.fields.items():   
                if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                    field.widget.attrs['class'] = 'form-check-input'
                else:
                    field.widget.attrs['class'] = 'form-control'
    ```
    
    *myapp/views.py*
    
    ```python
    def form_immobile(request):
        form = ImmobileForm()
        if request.method == 'POST':
            form = ImmobileForm(request.POST, request.FILES)
            if form.is_valid():
                immobile = form.save()
                files = request.FILES.getlist('immobile') ## pega todas as imagens
                if files:
                    for f in files:
                        ImmobileImage.objects.create( # cria instance para imagens
                            immobile=immobile, 
                            image=f)
                return redirect('list-location')  
        return render(request, 'form-immobile.html', {'form': form})
    ```
    
    *myapp/urls.py*
    
    ```python
    from django.urls import path 
    from myapp import views
    
    urlpatterns = [
        path('', views.list_location, name='list-location'), 
        path('form-client/', views.form_client, name='client-create'), 
        path('form-immobile/', views.form_immobile, name='immobile-create'),  
    ]
    ```
    
    *myapp/templates/form-immobile.html*
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Cadastrar Imóvel{% endblock %}
    
    {% load static %}
    
    {% block content %}
    <div class="container">
    
        <div class="d-flex gap-4 mt-3"> 
    			
            <img src="{% static 'images/imovel.png' %}" class="card-image" width="100%" height="500" alt="client"> 
            
            <form class="col-md-6" action="{% url 'immobile-create' %}" method="post" 
                enctype="multipart/form-data">
                {% csrf_token %} 
                <h3>Cadastrar Imóvel</h3>
                {% for field in form %}
                <div class="mt-3">
                    {{field.label}}
                    {{field}}
                </div>
                {% endfor %} 
                <input type="submit" class="btn btn-primary mt-3" value="Salvar">
            </form>
    
        </div>
     
    </div>
    {% endblock %}
    ```

</details>

<details><summary><b>Formulário Registro de Locação</b></summary>

- **Formulário Registro de Locação**
    
    *myapp/forms.py*
    
    ```python
    ## Registra Locação do Imovel    
    class RegisterLocationForm(forms.ModelForm):
        dt_start = forms.DateTimeField(widget=forms.DateInput(format='%d-%m-%Y',attrs={'type': 'date',}))
        dt_end = forms.DateTimeField(widget=forms.DateInput(format='%d-%m-%Y',attrs={'type': 'date',}))
    
        class Meta:
            model = RegisterLocation
            fields = '__all__'
            exclude = ('immobile','create_at',)
            
        def __init__(self, *args, **kwargs): # Adiciona 
            super().__init__(*args, **kwargs)  
            for field_name, field in self.fields.items():   
                  field.widget.attrs['class'] = 'form-control'
    ```
    
    *myapp/views.py*
    
    Vamos Registar uma locação a partir de um objeto. No caso o Imóvel.
    
    ```python
    def form_location(request, id):
        get_locate = Immobile.objects.get(id=id) ## pega objeto
        form = RegisterLocationForm()  
        if request.method == 'POST':
            form = RegisterLocationForm(request.POST)
            if form.is_valid():
                location_form = form.save(commit=False)
                location_form.immobile = get_locate ## salva id do imovel 
                location_form.save() 
    						## muda status do imovel para "Alugado" ???
                return redirect('list-location') # Retorna para lista
        context = {'form': form, 'location': get_locate}
        return render(request, 'form-location.html', context)
    ```
    
    Mudar o Status do Imóvel como Já Locado. O campo `is_locate` para a ser True. 
    
    ```python
    ## muda status do imovel para "Alugado"
    immo = Immobile.objects.get(id=id)
    immo.is_locate = True ## passa ser True
    immo.save() 
    ```
    
    *myapp/urls.py*
    
    ```python
    from django.urls import path 
    from myapp import views
    
    urlpatterns = [
        path('', views.list_location, name='list-location'), 
        path('form-client/', views.form_client, name='client-create'), 
        path('form-immobile/', views.form_immobile, name='immobile-create'), 
        path('form-location/<int:id>/', views.form_location, name='location-create'), 
    ]
    ```
    
    *myapp/templates/form-location.html*
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Cadastrar Locação{% endblock %}
    
    {% block content %}
    <div class="container"> 
        <div class="d-flex gap-4 mt-4">  
    
    				<!-- Informções do Objeto Here --> 
    
            <form class="col-md-4" action="{% url 'location-create' location.id %}" method="post">
                {% csrf_token %}
                <h3>Formulário de Registro Locação</h3>
                {% for field in form %}
                <div class="mt-3">
                    {{field.label}}
                    {{field}}
                </div>
                {% endfor %}
                <input type="submit" class="btn btn-primary mt-3" value="Locar">
            </form> 
        </div> 
    </div>
    {% endblock %}
    ```
    
    Como temos um context `location` para objeto podemos colocar algumas informações no templates. 
    
    ```html
    <!-- Informções do Objeto Here --> 
    <div class="">
    	  <div id="carouselExampleControls" class="carousel slide" data-bs-ride="false">
    	      <div class="carousel-inner">
    	          {% for el in location.immobile_images.all %}
    	          <div class="carousel-item {% if forloop.first %}active{% endif %}">
    	             <img src="{{el.image.url}}" class="card-image" width="100%" height="500" alt="{{el.id}}">
    	          </div>
    	          {% endfor %}
    	      </div>
    	      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
    	          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    	          <span class="visually-hidden">Previous</span>
    	      </button>
    	      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
    	          <span class="carousel-control-next-icon" aria-hidden="true"></span>
    	          <span class="visually-hidden">Next</span>
    	      </button>
    	  </div>
    	
    	  <div class="mt-3">
    	      <p>Codígo: {{location.code}}</p>
    	      <p>Endereço: {{location.address}}</p>
    	      <p>Valor: {{location.price}}</p>
    	      <div class="badge bg-success">Tipo: {{location.type_item}}</div> 
    	  </div> 
    
    </div>
            
    ```

</details>

<details><summary><b>Navbar</b></summary>

- **Navbar**
    
    navbar.html
    
    ```html
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    
        <div class="container-fluid">
    
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
    
            <a class="navbar-brand" href="#">Myapp</a>
    
            <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
    
                <ul class="navbar-nav gap-3 mb-2 mb-lg-0 mx-auto">
    
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="/">Inicio</a>
                    </li>
    
                    <li class="nav-item">
                        <a class="nav-link" href="/">Relatório</a>
                    </li>
    
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Cadastrar
                        </a>
                        <ul class="dropdown-menu dropdown-menu-dark">
                            <li>
                                <a class="dropdown-item" href="{% url 'client-create' %}">Cliente</a>
                            </li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li>
                                <a class="dropdown-item" href="{% url 'immobile-create' %}">Imóvel</a>
                            </li>
                        </ul>
                    </li> 
                </ul>
    
                <a class="navbar-brand" href="#">@eticialima</a> 
    
            </div>
    
        </div>
    
    </nav>
    ```

</details>

<details><summary><b>Message</b></summary>

- **Message**
    
    message.html
    
    ```html
    {% if messages %}
    <div class="messages">
        {% for message in messages %}
        <div {% if message.tags %} class="alert {{ message.tags }}"{% endif %} role="alert">{{ message }}</div>
        {% endfor %}
    </div>
    {% endif %}
    ```
    
    core/settings.py
    
    ```python
    # --- Messages --- #
    from django.contrib.messages import constants
    
    MESSAGE_TAGS = {
    	constants.ERROR: 'alert-danger',
    	constants.WARNING: 'alert-warning',
    	constants.DEBUG: 'alert-danger',
    	constants.SUCCESS: 'alert-success',
    	constants.INFO: 'alert-info',
    }
    ```

</details>

<details><summary><b>Relatório Simples</b></summary>

- **Relatório Simples**
    
    *myapp/views.py*
    
    ```python
    def reports(request): ## Relatórios   
        immobile = Immobile.objects.all()  
        return render(request, 'reports.html', {'immobiles':immobile})
    ```
    
    *myapp/urls.py*
    
    ```python
    from django.urls import path 
    from myapp import views
    
    urlpatterns = [
        ...
        path('reports/', views.reports, name='reports'),
    		...
     ]
    ```
    
    *myapp/templates/reports.html* 
    Esses 3 campos está em uma tabela relacionada. Então para chamar essas informações de outra tabela estou fazendo um for `immobile.reg_location.all` , para obter as informações dos registros de ***Locação Relacionados*** com a tabela de ***Imóveis***.
    
    ```html
    <td scope="row">{% for location in immobile.reg_location.all %}{{location.dt_start|date:"d/m/Y"}}{% endfor %}</td>
    <td scope="row">{% for location in immobile.reg_location.all %}{{location.dt_end|date:"d/m/Y"}}{% endfor %}</td>
    <td scope="row">{% for location in immobile.reg_location.all %}{{location.client}}{% endfor %}</td>
    
    ```
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Relatório{% endblock %}
    
    {% block content %}
    
    <div class="container"> 
    
        <!-- Tabela com todas informações de Registro de Locação -->
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Registro Inicial</th>
                    <th scope="col">Registro Final</th>
                    <th scope="col">Cliente</th>
                    <th scope="col">Codigo</th>
                    <th scope="col">Imovel</th>
                    <th scope="col">Valor</th>
                    <th scope="col">Locado</th>
                </tr>
            </thead>
            <tbody>
                {% for immobile in immobiles %}
                <tr>
                    <td scope="row">{{immobile.id}}</td>
    
                    <td scope="row">{% for location in immobile.reg_location.all %}{{location.dt_start|date:"d/m/Y"}}{% endfor %}</td>
                    <td scope="row">{% for location in immobile.reg_location.all %}{{location.dt_end|date:"d/m/Y"}}{% endfor %}</td>
                    <td scope="row">{% for location in immobile.reg_location.all %}{{location.client}}{% endfor %}</td>
    
                    <td scope="row">{{immobile.code}}</td>
                    <td scope="row">{{immobile.type_item}}</td>
                    <td scope="row">R$ {{immobile.price}}</td>
    
                    <td scope="row">
                        {% if immobile.is_locate == True %}
                        <i class="fas fa-check-circle fa-2x link-success"></i>
                        {% else %}
                        <i class="fas fa-minus-circle fa-2x link-danger"></i>
                        {% endif %} 
                    </td>
    
                </tr>  
                {% endfor %}
            </tbody>
        </table> 
    </div>
    
    {% endblock %}
    ```
    
    Outro detalhe adicionar a Tag do **Font Awesome**. Para aparecer os icones que coloquei na tabela acima.
    
    ```html
    <!-- CSS -->
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.4/css/all.css" integrity="sha384-DyZ88mC6Up2uqS4h/KRgHuoeGwBcD4Ng9SiP4dIRy0EXTlnuz47vAwmeGwVChigm" crossorigin="anonymous"/>
    ```
    
    **Filtrar pelo status do imóvel se está locado ou não locado**
    
    ```python
    def reports(request): ## Relatórios   
        immobile = Immobile.objects.all()
        is_locate = request.GET.get('is_locate') 
        if is_locate: ## Imovel foi locado ou não
            immobile = Immobile.objects.filter(is_locate=is_locate) 
        return render(request, 'reports.html', {'immobiles':immobile})
    ```
    
    ```html
    <div class="row g-3 align-items-center m-3 bg-light p-3"> 
        <!-- Filtrar pelo status do imóvel se está locado ou não locado -->
        <div class="col-auto">
            <form action="{% url 'reports' %}">
                <label>Status Locação</label>
                <select name="is_locate" class="form-select" onchange="this.form.submit()">
                    <option></option> 
                    <option value="True" {% if request.GET.is_locate == 'True' %}selected{% endif %}>LOCADO</option>
                    <option value="False" {% if request.GET.is_locate == 'False' %}selected{% endif %}>NÃO LOCADO</option> 
                </select>
            </form>
        </div>
    
        <!-- Resetar estado dos filtros -->
        <div class="col-auto"> 
            <a class="btn btn-danger" href="{% url 'reports' %}"><i class="fas fa-window-close"></i></a>
        </div>  
    </div>
    ```

</details>

<details><summary><b>Filtros</b></summary>

- **Filtros**
 
    **Filter pelo tipo de imóvel**
    
    ```python
    def reports(request): ## Relatórios   
        immobile = Immobile.objects.all()  
        type_item = request.GET.get('type_item')
        is_locate = request.GET.get('is_locate') 
        if type_item: ## Tipo de Imovel
            immobile = Immobile.objects.filter(type_item=type_item) 
        if is_locate: ## Imovel foi locado ou não
            immobile = Immobile.objects.filter(is_locate=is_locate) 
        return render(request, 'reports.html', {'immobiles':immobile})
    ```
    
    ```html
    <!-- Filter pelo tipo de imóvel -->
    <div class="col-auto">
        <form class="" action="{% url 'reports' %}">
           <label>Tipo de Imóvel</label>
            <select name="type_item" class="form-select" onchange="this.form.submit()">
                <option></option> 
                <option value="APARTAMENTO" {% if request.GET.type_item == 'APARTAMENTO' %}selected{% endif %}>APARTAMENTO</option>
                <option value="KITNET" {% if request.GET.type_item == 'KITNET' %}selected{% endif %}>KITNET</option>
                <option value="CASA" {% if request.GET.type_item == 'CASA' %}selected{% endif %}>CASA</option>
            </select>
        </form> 
    </div>
    ```
    
    **Pesquisar pelo nome ou e-mail do cliente**
    
    Vamos utilizar essa biblioteca para filtros mais complexo. Nesse caso vamos usar apenas 2 parâmetros para filtrar Nome do cliente ou E-mail.
    
    `from django.db.models import Q`
    
    Nota que estamos filtrando pela tabela `Immobile`  E o campo **client** pertence a tabela `RegisterLocation` que é uma *foreignkey*. Bom para filtrar vamos usar o *related_name* que é `reg_location`. 
    
    ```python
    def reports(request): ## Relatórios   
        immobile = Immobile.objects.all() 
        client = request.GET.get('client') 
        type_item = request.GET.get('type_item')
        is_locate = request.GET.get('is_locate')
    
        if client: ## Filtra por nome e email do cliente
            immobile = Immobile.objects.filter(
    					Q(reg_location__client__name__icontains=client) | 
    					Q(reg_location__client__email__icontains=client))
    
        if type_item: ## Tipo de Imovel
            immobile = Immobile.objects.filter(type_item=type_item) 
        if is_locate: ## Imovel foi locado ou não
            immobile = Immobile.objects.filter(is_locate=is_locate) 
        return render(request, 'reports.html', {'immobiles':immobile})
    ```
    
    ```html
    <!-- Pesquisar pelo nome ou e-mail do cliente -->
    <div class="col-auto">  
        <label>Nome do Cliente ou E-mail</label>
        <form class="d-flex" action="{% url 'reports' %}">
            <input name="client" type="search" class="form-control me-2" placeholder="Pesquisar por cliente..." aria-label="Search">
            <button class="btn btn-success" type="submit"><i class="fas fa-search"></i></button>
        </form> 
    </div>
    ```
    
    **Filter por Intervalo de data**
    
    ```python
    def reports(request): ## Relatórios   
        immobile = Immobile.objects.all() 
        client = request.GET.get('client')
        dt_start = request.GET.get('dt_start')
        dt_end = request.GET.get('dt_end')
        type_item = request.GET.get('type_item')
        is_locate = request.GET.get('is_locate')
        if client: ## Filtra por nome e email do cliente
            immobile = Immobile.objects.filter(Q(reg_location__client__name__icontains=client) | Q(reg_location__client__email__icontains=client))
        if dt_start and dt_end: ## Por data
            immobile = Immobile.objects.filter(
    						reg_location__create_at__range=[dt_start,dt_end])
        if type_item: ## Tipo de Imovel
            immobile = Immobile.objects.filter(type_item=type_item) 
        if is_locate: ## Imovel foi locado ou não
            immobile = Immobile.objects.filter(is_locate=is_locate) 
        return render(request, 'reports.html', {'immobiles':immobile})
    ```
    
    ```html
    <!-- Filter por Intervalo de data -->
    <div class="col-auto">  
        <form class="d-flex align-items-end" action="{% url 'reports' %}"> 
            <div class="">
                <label for="">Inicio</label>
                <input name="dt_start" type="date" value="{{request.GET.dt_start}}" class="form-control me-2"> 
            </div>
            <div class="">
                <label for="">Final</label>
                <input name="dt_end" type="date" value="{{request.GET.dt_end}}" class="form-control me-2"> 
            </div>
            <div class="">
                <button class="btn btn-outline-dark" type="submit"><i class="fas fa-filter"></i></button> 
            </div>
        </form> 
    </div>
    ``` 

</details>
