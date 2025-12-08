from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User # Importer User 
from .models import Article,Commentaire
from .forms import ArticleForm,CommentaireForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
# Create your views here.
 


def inscription_view(request): 
   if request.method == 'POST': 
       form = UserCreationForm(request.POST) 
       if form.is_valid(): 
           user = form.save() # Sauvegarde le nouvel utilisateur 
           login(request, user) # Connecte l'utilisateur 
           return redirect('blogapp:accueil') # Redirige vers l'accueil 
   else: 
       form = UserCreationForm() 
   return render(request, 'blogapp/inscription.html', {'form': form})

def connexion_view(request): 
   if request.method == 'POST': 
       form = AuthenticationForm(request, data=request.POST) 
       if form.is_valid(): 
           user = form.get_user() 
           login(request, user) 
           # Rediriger vers la page d'accueil après la connexion 
           # Ou vers la page précédente si elle existe (plus avancé, on verra plus tard) 
           return redirect('blogapp:accueil') 
   else: 
       form = AuthenticationForm() 
   return render(request, 'blogapp/connexion.html', {'form': form}) 


def deconnexion_view(request): 
   if request.method == 'POST': # C'est une bonne pratique de faire la déconnexion sur un POST 
       logout(request) 
       return redirect('blogapp:accueil') 
   logout(request) # Pour une version ultra-simple accessible par un lien GET 
   return redirect('blogapp:accueil') 
   # Si ce n'est pas un POST, on pourrait afficher un bouton de confirmation 
   # ou simplement rediriger, mais pour la simplicité, on assume un POST 
   # Pour un vrai bouton dans base.html, il faudrait un petit formulaire 
   # Pour l'instant, on va faire en sorte que le lien dans base.html mène à une URL GET 
   # qui redirige vers une vue qui fait le POST ou on simplifie pour GET directement. 
   # Simplifions pour GET pour l'instant pour un débutant, bien que POST soit mieux.


@login_required # Seuls les utilisateurs connectés peuvent accéder à cette vue 
def creer_article_view(request): 
   if request.method == 'POST': 
       form = ArticleForm(request.POST) 
       if form.is_valid(): 
           nouvel_article = form.save(commit=False) # Ne sauvegarde pas encore en base de données 
           nouvel_article.auteur = request.user # Définit l'auteur comme l'utilisateur connecté 
           nouvel_article.save() # Sauvegarde l'article en base de données 
           # form.save_m2m() # Si vous aviez des champs ManyToMany dans le formulaire 
           return redirect('blogapp:detail_article', pk=nouvel_article.pk) # Redirige vers la page de détail de l'article créé 
   else: 
       form = ArticleForm() 
   return render(request, 'blogapp/creer_modifier_article.html', {'form': form, 'action': 'Créer'})    

def accueil_view(request): 
   tous_les_articles = Article.objects.all().order_by('-date_creation') 
 
   # Configuration de la pagination 
   paginator = Paginator(tous_les_articles, 5) # Affiche 5 articles par page 
 
   page_numero = request.GET.get('page') # Récupère le numéro de page depuis l'URL (ex: ?page=2) 
 
   try: 
       articles_pages = paginator.page(page_numero) 
   except PageNotAnInteger: 
       # Si 'page' n'est pas un entier, afficher la première page. 
       articles_pages = paginator.page(1) 
   except EmptyPage: 
       # Si 'page' est hors limites (ex: page 9999), afficher la dernière page de résultats. 
       articles_pages = paginator.page(paginator.num_pages) 
 
   context = { 
       'articles_a_afficher': articles_pages, # On passe l'objet Page au template 
   } 
   return render(request, 'blogapp/accueil.html', context)

def detail_article_view(request, pk): # 'pk' est la clé primaire (ID) de l'article 
    article = get_object_or_404(Article, pk=pk) # Récupère l'article ou renvoie une erreur 404 s'il n'existe pas 
    commentaire_form = CommentaireForm() 
    context = { 
    'article': article, 
    'commentaire_form': commentaire_form
    } 
    return render(request, 'blogapp/detail_article.html', context) 

@login_required 
def modifier_article_view(request, pk): 
   article = get_object_or_404(Article, pk=pk) 
 
   # Vérifier si l'utilisateur connecté est l'auteur de l'article 
   if article.auteur != request.user: 
       # Rediriger ou afficher une erreur "Permission non accordée" 
       # Pour la simplicité, on redirige vers le détail de l'article 
       return redirect('blogapp:detail_article', pk=article.pk) # Ou une page d'erreur 403 Forbidden 
 
   if request.method == 'POST': 
       form = ArticleForm(request.POST, instance=article) # Pré-remplit le formulaire avec les données de l'article existant 
       if form.is_valid(): 
           form.save() 
           return redirect('blogapp:detail_article', pk=article.pk) 
   else: 
       form = ArticleForm(instance=article) # Affiche le formulaire pré-rempli 
 
   context = { 
       'form': form, 
       'action': 'Modifier', # Pour le template 
       'article': article # Pour afficher le titre par exemple 
   } 
   return render(request, 'blogapp/creer_modifier_article.html', context)

@login_required 
def supprimer_article_view(request, pk): 
    article = get_object_or_404(Article, pk=pk) 
    if article.auteur != request.user: 
        return redirect('blogapp:detail_article', pk=article.pk) # Ou erreur 403 
    if request.method == 'POST': # Si l'utilisateur a confirmé la suppression 
        article.delete() 
        return redirect('blogapp:accueil') # Redirige vers l'accueil après suppression 
    # Si c'est une requête GET, on affiche la page de confirmation 
    context = { 
    'article': article 
    } 
    return render(request, 'blogapp/confirmer_suppression_article.html', context)


@login_required # Seuls les utilisateurs connectés peuvent commenter 
def ajouter_commentaire_view(request, article_pk): # article_pk est l'ID de l'article à commenter 
   article = get_object_or_404(Article, pk=article_pk) 
 
   # Règle : L'auteur de l'article ne peut pas commenter son propre article 
   # (Comme demandé : "seulement les autre utilisateurs peut commenter") 
   # Si vous voulez que l'auteur puisse commenter, retirez cette condition. 
   if article.auteur == request.user: 
       # On pourrait afficher un message d'erreur avec django.contrib.messages 
       # Pour la simplicité "bébé", on redirige simplement sans rien faire. 
       return redirect('blogapp:detail_article', pk=article.pk) 
 
   if request.method == 'POST': 
       form = CommentaireForm(request.POST) 
       if form.is_valid(): 
           commentaire = form.save(commit=False) 
           commentaire.article = article 
           commentaire.auteur = request.user # L'auteur du commentaire est l'utilisateur connecté 
           commentaire.save() 
           return redirect('blogapp:detail_article', pk=article.pk) # Redirige vers la page de l'article 
   else: 
       # Si ce n'est pas un POST, on pourrait rediriger ou ne rien faire, 
       # car le formulaire sera affiché sur la page de détail de l'article. 
       # Pour ce flux, la vue est principalement pour traiter le POST. 
       # Si on accède à cette URL en GET, on redirige simplement vers l'article. 
       return redirect('blogapp:detail_article', pk=article.pk)
   
def profil_utilisateur_view(request, username): 
    # Récupère l'utilisateur par son nom d'utilisateur ou renvoie une erreur 404 
    utilisateur_profil = get_object_or_404(User, username=username) 
    # Récupère tous les articles écrits par cet utilisateur, triés par date de création 
    articles_utilisateur = Article.objects.filter(auteur=utilisateur_profil).order_by('-date_creation') 
    context = { 
    'utilisateur_profil': utilisateur_profil, 
    'articles_utilisateur': articles_utilisateur, 
    } 
    return render(request, 'blogapp/profil_utilisateur.html', context)   