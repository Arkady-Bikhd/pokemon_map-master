import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from PIL import Image
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)

MOSCOW_TIME_ZONE = 3  # Не знаю, как программно определить часовой пояс


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons = Pokemon.objects.all()
    current_time = localtime()
    for pokemon in pokemons:
        pokemon_entities = pokemon.entities.filter(
            appeared_at__lt=current_time, disappeared_at__gt=current_time)
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
                request.build_absolute_uri(
                    pokemon_entity.pokemon.image.url
                )
            )

    pokemons_on_page = list()
    for pokemon in pokemons:
        pokemons_on_page.append(form_pokemon_on_page(pokemon, request))

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    current_time = localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = pokemon.entities.filter(
        appeared_at__lt=current_time, disappeared_at__gt=current_time)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(
                pokemon_entity.pokemon.image.url
            )
        )
    pokemon_on_page = form_pokemon_on_page(pokemon, request, True)

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })


def form_pokemon_on_page(pokemon, request, pokemon_page=False):

    pokemon_properties = {
        'pokemon_id': pokemon.id,
        'img_url':  request.build_absolute_uri(
            pokemon.image.url),
        'title_ru': pokemon.title
    }
    if not pokemon_page:
        return pokemon_properties

    pokemon_properties['description'] = pokemon.description
    pokemon_properties['title_en'] = pokemon.title_en
    pokemon_properties['title_jp'] = pokemon.title_jp
    if pokemon.previous_evolution:
        pokemon_properties['previous_evolution'] = {
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url':  request.build_absolute_uri(
                pokemon.previous_evolution.image.url),
            'title_ru': pokemon.previous_evolution.title
        }
    next_evolutions = pokemon.next_evolutions.first()
    if next_evolutions:
        pokemon_properties['next_evolution'] = {
            'pokemon_id': next_evolutions.id,
            'img_url':  request.build_absolute_uri(
                next_evolutions.image.url),
            'title_ru': next_evolutions.title
        }

    return pokemon_properties
